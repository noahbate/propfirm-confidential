from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
from pathlib import Path
import os
from auth_routes import router as auth_router

app = FastAPI()
app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).resolve().parents[1] / "prop_firms.json"


@app.get("/api/prop-firms")
def get_prop_firms(request: Request):
    try:
        resolved = DATA_PATH.resolve()
        print(f"[prop-firm-api] data_path={resolved} exists={resolved.exists()}")
        if not resolved.exists():
            return JSONResponse({"error": "data file missing", "path": str(resolved)}, status_code=500)
        with open(resolved, "r") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return JSONResponse({"error": "data not a list"}, status_code=500)
        print(f"[prop-firm-api] loaded_firms={len(data)}")
        return data
    except Exception as e:
        print(f"[prop-firm-api] error fetching firms: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/health")
def health():
    return {"status": "ok"}
