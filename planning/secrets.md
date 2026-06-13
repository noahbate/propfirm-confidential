# Secrets Management Strategy

All secrets (API keys, tokens) for this project will be managed as environment variables.

## Loading Mechanism
- **Local Development:** Secrets will be loaded from a `.env` file in the project root. This file is included in `.gitignore` and will never be committed to the repository.
- **Production (Netlify):** Secrets will be set in the Netlify UI under "Site settings > Build & deploy > Environment > Environment variables".

## Key List
- `NETLIFY_AUTH_TOKEN`: For deployments and API interactions.
- `X_API_KEY`: For the `xurl` CLI and X.com automation.
- `X_API_SECRET_KEY`: For the `xurl` CLI and X.com automation.
- `GITHUB_TOKEN`: For CI/CD and repository interactions.
