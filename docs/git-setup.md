# Git Setup — reusable

Use these commands for each new project.

## Initialize
```
git init
git add -A
git commit -m "Initial project scaffold"
```

## Branch model
- `main` = production-ready
- feature branches off `main`
- merge via PR

## Commit style
- Use verbs: Add, Update, Fix, Remove
- Scope if helpful: `API(...)`, `UI(...)`, `Docs(...)`

## Useful ignores
Keep `.gitignore` minimal. If needed:
- dependency dirs: `node_modules`, `.venv`, `dist`
- secrets: `.env`, `*.pem`, `*.key`
- OS/editor junk
