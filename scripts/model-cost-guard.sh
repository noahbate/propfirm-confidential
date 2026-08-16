#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$PROJECT_ROOT/docs/cost-log.md"
CHEAPER_MODEL="${COST_CHEAPER_MODEL:-gemini-2.0-flash}"
THRESHOLD="${COST_THRESHOLD_USD:-0.50}"

if [[ ! -f "$LOG" ]]; then
  exit 0
fi

today=$(date +%Y-%m-%d)
# Sum today's USD spend from the last column
today_total=$(awk -F'|' -v d="$today" '
  $2 ~ d {
    gsub(/ |\r/, "", $7);
    if ($7 ~ /^[0-9]+(\.[0-9]+)?$/) total += $7
  }
  END { printf "%.2f", total+0 }
' "$LOG")

if [[ -z "$today_total" ]]; then today_total="0.00"; fi

if (( $(echo "$today_total > $THRESHOLD" | bc -l 2>/dev/null || echo 0) )); then
  echo "$CHEAPER_MODEL"
else
  echo ""
fi
