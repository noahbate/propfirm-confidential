from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path
from datetime import datetime

from pydantic import BaseModel
import hashlib

from auth_routes_helpers import _load_preferences, _save_preferences, PREFERENCES_PATH
from user_store import (
    load_users,
    save_users,
    create_session,
    invalidate_session,
    user_id_from_token,
)


class RegisterPayload(BaseModel):
    email: str
    password: str
    name: str | None = None


class LoginPayload(BaseModel):
    email: str
    password: str


class FavoritePayload(BaseModel):
    firm_id: str


router = APIRouter(prefix="/auth", tags=["auth"])

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def _normalize_favorites(existing) -> list[str]:
    if not existing:
        return []
    if isinstance(existing, list):
        return existing
    return [existing] if isinstance(existing, str) else list(existing)

@router.post("/register")
async def register(payload: RegisterPayload):
    users = load_users()
    if payload.email in users:
        raise HTTPException(status_code=400, detail="Email already registered")
    users[payload.email] = {
        "email": payload.email,
        "name": payload.name or payload.email,
        "password_hash": _hash_password(payload.password),
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    save_users(users)
    token = create_session(payload.email)
    return {"user_id": payload.email, "name": payload.name or payload.email, "token": token}


@router.post("/login")
async def login(payload: LoginPayload):
    users = load_users()
    user = users.get(payload.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.get("password_hash") != _hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_session(payload.email)
    return {
        "user_id": payload.email,
        "name": user.get("name", payload.email),
        "token": token,
    }


@router.post("/logout")
async def logout(request: Request):
    auth = request.headers.get("authorization")
    token = None
    if auth and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1]
    if token:
        invalidate_session(token)
    return {"ok": True}


@router.get("/me")
async def me(request: Request):
    auth = request.headers.get("authorization")
    token = None
    if auth and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1]
    user_id = user_id_from_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    users = load_users()
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"user_id": user_id, "name": user.get("name", user_id)}


@router.post("/favorites/{user_id}")
async def save_favorite(user_id: str, payload: FavoritePayload, request: Request):
    auth = request.headers.get("authorization")
    token = None
    if auth and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1]
    caller = user_id_from_token(token)
    if not caller or caller != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    data = _load_preferences()
    user = data.setdefault("users", {}).setdefault(user_id, {"favorites": [], "updated_at": None})
    favorites = _normalize_favorites(user.get("favorites")) if isinstance(user.get("favorites"), (list, str)) else []
    if payload.firm_id not in favorites:
        favorites.append(payload.firm_id)
    user["favorites"] = favorites
    user["updated_at"] = datetime.utcnow().isoformat() + "Z"
    _save_preferences(data)
    return {"user_id": user_id, "favorites": favorites}


@router.delete("/favorites/{user_id}/{firm_id}")
async def remove_favorite(user_id: str, firm_id: str, request: Request):
    auth = request.headers.get("authorization")
    token = None
    if auth and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1]
    caller = user_id_from_token(token)
    if not caller or caller != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    data = _load_preferences()
    user = data.get("users", {}).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    favorites = user.get("favorites") or []
    user["favorites"] = [fav for fav in favorites if fav != firm_id]
    user["updated_at"] = datetime.utcnow().isoformat() + "Z"
    _save_preferences(data)
    return {"user_id": user_id, "favorites": user["favorites"]}


@router.get("/favorites/{user_id}")
async def list_favorites(user_id: str, request: Request):
    auth = request.headers.get("authorization")
    token = None
    if auth and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1]
    caller = user_id_from_token(token)
    if not caller or caller != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    data = _load_preferences()
    user = data.get("users", {}).get(user_id)
    if not user:
        return {"user_id": user_id, "favorites": []}
    return {"user_id": user_id, "favorites": user.get("favorites", [])}


@router.get("/debug")
async def debug_auth():
    return {"status": "ok", "preferences_path": str(PREFERENCES_PATH)}
