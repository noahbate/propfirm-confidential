from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "backend" / "prop_firms.json"

@app.get("/api/prop-firms")
def get_prop_firms():
    resolved = DATA_PATH.resolve()
    print("DATA_PATH", resolved, "exists", resolved.exists())
    if resolved.exists():
        with open(resolved, "r") as f:
            data = json.load(f)
        print("loaded_firms", len(data))
        return data if isinstance(data, list) else []
    return []
