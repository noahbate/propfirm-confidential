#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$PROJECT_ROOT/docs/cost-log.md"
ENV_FILE="$PROJECT_ROOT/.env.cost"

# Thresholds
SPIKE_MULTIPLIER="${COST_SPIKE_MULTIPLIER:-2.0}"
CHEAPER_MODEL="${COST_CHEAPER_MODEL:-user/gpt-4o-mini}"

# --- helpers ---
today=$(date +%Y-%m-%d)
now=$(date +%Y-%m-%dT%H:%M:%S%:z)

ensure_log() {
  if [[ ! -f "$LOG" ]]; then
    mkdir -p "$(dirname "$LOG")"
    cat > "$LOG" <<'EOF'
# Cost Log

| Date | Provider | Model | Tokens In | Tokens Out | Cost (USD) | Notes |
|------|----------|-------|-----------|------------|------------|-------|
EOF
  fi
}

# --- gather usage ---
usage_json="${COST_USAGE_JSON:-}" # optional external input
if [[ -z "$usage_json" ]]; then
  # Default: placeholder stub. Replace with provider API calls (OpenAI/Anthropic/Google/etc).
  usage_json='[
    {"provider":"openai","model":"gpt-4o","tokens_in":0,"tokens_out":0,"cost_usd":0.00},
    {"provider":"anthropic","model":"claude-sonnet-4-20250514","tokens_in":0,"tokens_out":0,"cost_usd":0.00},
    {"provider":"google-gemini","model":"gemini-2.0-flash","tokens_in":0,"tokens_out":0,"cost_usd":0.00}
  ]'
fi

# --- compute totals per day (approximate) ---
# If today already has entries, compute current total
if [[ -f "$LOG" ]]; then
  today_total=$(awk -F'|' -v d="$today" '$2 ~ d {gsub(/ /,"",$7); total+=$7} END{printf "%.2f", total+0}' "$LOG" 2>/dev/null || echo 0)
else
  today_total=0
fi

# --- append new rows ---
append_row() {
  local provider="$1" model="$2" tin="$3" tout="$4" cost="$5" notes="$6"
  printf "| %s | %s | %s | %s | %s | %s | %s |\n" \
    "$today" "$provider" "$model" "$tin" "$tout" "$cost" "$notes" >> "$LOG"
}

# Parse usage_json and append (requires jq)
if command -v jq >/dev/null 2>&1; then
  echo "$usage_json" | jq -r '.[] | [.provider, .model, (.tokens_in|tostring), (.tokens_out|tostring), (.cost_usd|tostring), "auto-logged"] | @tsv' \
    | while IFS=$'\t' read -r provider model tin tout cost notes; do
        append_row "$provider" "$model" "$tin" "$tout" "$cost" "$notes"
      done
else
  echo "jq not installed; append disabled. Install jq or set COST_USAGE_JSON with a parser." >&2
fi

# --- alert on spike ---
latest_day_total=$(awk -F'|' -v d="$today" '$2 ~ d {gsub(/ /,"",$7); total+=$7} END{printf "%.2f", total+0}' "$LOG")
if (( $(echo "$latest_day_total > 0" | bc -l 2>/dev/null || echo 0) )); then
  baseline=$(awk -F'|' 'NR>2{gsub(/ /,"",$7); hist[$2]+=$7} END{for(d in hist){print d,hist[d]}}' "$LOG" | sort | tail -n 7 | awk '{s+=$2; c++} END{if(c>0) printf "%.2f", s/c; else print "0.00"}')
  if [[ -n "$baseline" ]] && command -v bc >/dev/null 2>&1; then
    if (( $(echo "$latest_day_total > $baseline * $SPIKE_MULTIPLIER" | bc -l) )); then
      echo "COST SPIKE ALERT: today total $latest_day_total exceeds ${SPIKE_MULTIPLIER}x baseline ($baseline)" >&2
      echo "Suggested cheaper model: $CHEAPER_MODEL" >&2
      # Optional: export to env for downstream scripts
      echo "COST_CHEAPER_MODEL=$CHEAPER_MODEL" > "$PROJECT_ROOT/.cost.env"
    fi
  fi
fi

echo "Logged costs to $LOG. Today total: $latest_day_total USD"
cat "$LOG"
