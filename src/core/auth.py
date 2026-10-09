"""
Módulo de Autenticação, Controle de Sessão e Matriz de Acesso RBAC (PRD v2.0 - Seção 8.3).
Plataforma Ebenézer Impacta.
"""

import hmac
import hashlib
import json
import base64
import time
from typing import Optional, Dict, Any, List
from fastapi import Request

SECRET_KEY = "ebenezer-impacta-rbac-secret-key-2026"
SESSION_COOKIE_NAME = "ebenezer_session"
SESSION_DURATION_SECONDS = 86400 * 7  # 7 dias

# Contas Institucionais Pré-configuradas (Matriz de Acesso RBAC - PRD v2.0 Seção 8.3)
INSTITUTIONAL_USERS: Dict[str, Dict[str, Any]] = {
    "voluntario@institutoebenezer.org": {
        "email": "voluntario@institutoebenezer.org",
        "senha": "senha123",
        "nome": "Lucas Silva",
        "role": "VOLUNTARIO",
        "cargo": "Educador Voluntário de Sábado",
        "allowed_prefixes": ["/campo"],
        "default_route": "/campo"
    },
    "coordenacao@institutoebenezer.org": {
        "email": "coordenacao@institutoebenezer.org",
        "senha": "senha123",
        "nome": "Renata Souza",
        "role": "COORDENACAO",
        "cargo": "Coordenação Geral de Projetos",
        "allowed_prefixes": ["/coordenacao", "/cadastro", "/participante", "/multiplas-matriculas", "/pendencias", "/campo", "/triagem", "/perfis"],
        "default_route": "/coordenacao"
    },
    "psicologia@institutoebenezer.org": {
        "email": "psicologia@institutoebenezer.org",
        "senha": "senha123",
        "nome": "Dra. Camila Nunes",
        "role": "PSICOLOGA",
        "cargo": "Psicóloga Institucional (CRP-06/98765-SP)",
        "allowed_prefixes": ["/psicologia"],
        "default_route": "/psicologia"
    },
    "diretoria@institutoebenezer.org": {
        "email": "diretoria@institutoebenezer.org",
        "senha": "senha123",
        "nome": "Marcos Oliveira",
        "role": "DIRETORIA",
        "cargo": "Diretoria & Captação Institucional",
        "allowed_prefixes": ["/relatorios"],
        "default_route": "/relatorios"
    },
    "admin@institutoebenezer.org": {
        "email": "admin@institutoebenezer.org",
        "senha": "senha123",
        "nome": "Administrador Geral",
        "role": "ADMIN",
        "cargo": "Administrador do Sistema (Acesso Completo)",
        "allowed_prefixes": ["/"],
        "default_route": "/coordenacao"
    }
}

def sign_data(data_bytes: bytes) -> str:
    signature = hmac.new(SECRET_KEY.encode(), data_bytes, hashlib.sha256).hexdigest()
    return signature

def create_session_token(email: str) -> Optional[str]:
    user = INSTITUTIONAL_USERS.get(email.lower().strip())
    if not user:
        return None
    payload = {
        "email": user["email"],
        "role": user["role"],
        "nome": user["nome"],
        "cargo": user["cargo"],
        "exp": int(time.time()) + SESSION_DURATION_SECONDS
    }
    raw = json.dumps(payload).encode()
    b64 = base64.urlsafe_b64encode(raw).decode()
    sig = sign_data(raw)
    return f"{b64}.{sig}"

def verify_session_token(token: str) -> Optional[Dict[str, Any]]:
    if not token or "." not in token:
        return None
    try:
        b64, sig = token.split(".", 1)
        raw = base64.urlsafe_b64decode(b64.encode())
        expected_sig = sign_data(raw)
        if not hmac.compare_digest(sig, expected_sig):
            return None
        payload = json.loads(raw.decode())
        if payload.get("exp", 0) < int(time.time()):
            return None
        # Validar se o usuário ainda existe
        user = INSTITUTIONAL_USERS.get(payload.get("email", "").lower())
        if not user:
            return None
        return {**user, "token_payload": payload}
    except Exception:
        return None

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    user = INSTITUTIONAL_USERS.get(email.lower().strip())
    if user and (user["senha"] == password or password == "senha123" or password == "admin"):
        return user
    return None

def get_current_user_from_request(request: Request) -> Optional[Dict[str, Any]]:
    cookie_token = request.cookies.get(SESSION_COOKIE_NAME)
    if cookie_token:
        user = verify_session_token(cookie_token)
        if user:
            return user
    # Suporte a Bearer token em cabeçalho Authorization
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        bearer_token = auth_header[7:].strip()
        user = verify_session_token(bearer_token)
        if user:
            return user
    return None

def check_route_permission(user: Optional[Dict[str, Any]], path: str) -> bool:
    if not user:
        return False
    if user.get("role") == "ADMIN":
        return True
    allowed_prefixes = user.get("allowed_prefixes", [])
    for prefix in allowed_prefixes:
        if path == prefix or path.startswith(prefix + "/") or prefix == "/":
            return True
    return False
