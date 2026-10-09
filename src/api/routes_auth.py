"""
Rotas de Autenticação e Controle de Sessão (API).
Plataforma Ebenézer Impacta.
"""

from fastapi import APIRouter, Request, Response, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
from src.core.auth import (
    authenticate_user,
    create_session_token,
    get_current_user_from_request,
    INSTITUTIONAL_USERS,
    SESSION_COOKIE_NAME,
    SESSION_DURATION_SECONDS
)

router = APIRouter(prefix="/api/auth", tags=["Autenticação & Segurança"])

class LoginRequest(BaseModel):
    email: str
    password: str

class QuickLoginRequest(BaseModel):
    role: str

@router.post("/login")
def login(payload: LoginRequest, response: Response):
    user = authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha institucional incorretos."
        )
    token = create_session_token(user["email"])
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        max_age=SESSION_DURATION_SECONDS,
        httponly=True,
        samesite="lax",
        secure=False  # Em ambiente local HTTP
    )
    return {
        "status": "sucesso",
        "usuario": {
            "nome": user["nome"],
            "email": user["email"],
            "role": user["role"],
            "cargo": user["cargo"]
        },
        "redirect_url": user["default_route"]
    }

@router.post("/quick-login")
def quick_login(payload: QuickLoginRequest, response: Response):
    """Permite alternância rápida de personas para demonstração acadêmica e homologação."""
    target_user = next((u for u in INSTITUTIONAL_USERS.values() if u["role"] == payload.role.upper()), None)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Perfil '{payload.role}' não encontrado."
        )
    token = create_session_token(target_user["email"])
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        max_age=SESSION_DURATION_SECONDS,
        httponly=True,
        samesite="lax",
        secure=False
    )
    return {
        "status": "sucesso",
        "usuario": {
            "nome": target_user["nome"],
            "email": target_user["email"],
            "role": target_user["role"],
            "cargo": target_user["cargo"]
        },
        "redirect_url": target_user["default_route"]
    }

@router.post("/logout")
def api_logout(response: Response):
    response.delete_cookie(key=SESSION_COOKIE_NAME)
    return {"status": "desconectado"}

@router.get("/me")
def get_me(request: Request):
    user = get_current_user_from_request(request)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado.")
    return {
        "nome": user["nome"],
        "email": user["email"],
        "role": user["role"],
        "cargo": user["cargo"],
        "allowed_prefixes": user["allowed_prefixes"],
        "default_route": user["default_route"]
    }
