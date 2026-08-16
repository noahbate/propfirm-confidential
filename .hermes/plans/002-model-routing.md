# Model Routing Table

| Task Category | Recommended Model | Reasoning | Trigger / Hermes Delegate | Cost Profile |
|---|---|---|---|---|
| Architecture, Strategy, Planning | Grok 3 / Claude 3.5 Sonnet | High reasoning, long context, creative synthesis | Hermes main orchestrator | Premium |
| Research, Summarization | Claude 3.5 Sonnet / NotebookLM | Excellent at synthesis & RAG | MCP NotebookLM | Premium / Medium |
| Code Generation, Refactoring | Grok 3 / Gemini 2.5 Flash | Fast iteration, strong coding | Hermes Terminal + sub-agents | Low / Medium |
| Routine Scripting, Data Tasks | Gemini 2.5 Flash / Grok 3-mini | High throughput, cheap | Parallel sub-agents | Low |
| Content Writing (Web/X posts) | Grok 3-mini / Claude Haiku | Speed + personality consistency | X-engine / content pipeline | Very Low |
| Debugging / Error Recovery | Grok 3 | Strong tool-use & reasoning | Hermes self-healing | Medium |
| UI/Frontend Implementation | Grok 3 / Claude 3.5 Sonnet | Visual + component reasoning | Dedicated UI sub-agent | Medium |

## Routing Rules
- Default to cheapest capable model.
- Escalate to premium on failure or explicit reasoning-intensive flag.
- Track spend in `/projects/propfirm-confidential/docs/cost-log.md` (auto-appended via scripts).
