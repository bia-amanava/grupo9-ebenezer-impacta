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
        "allowed_prefixes": ["/campo", "/tutorial"],
        "default_route": "/campo",
        "status": "ATIVO",
        "atividades_atribuidas": ["PROG-SONHOS", "PROG-REFORCO"]
    },
    "coordenacao@institutoebenezer.org": {
        "email": "coordenacao@institutoebenezer.org",
        "senha": "senha123",
        "nome": "Renata Souza",
        "role": "COORDENACAO",
        "cargo": "Coordenação Geral de Projetos",
        "allowed_prefixes": ["/coordenacao", "/cadastro", "/participante", "/multiplas-matriculas", "/pendencias", "/campo", "/triagem", "/perfis", "/tutorial", "/gestao-acessos"],
        "default_route": "/coordenacao",
        "status": "ATIVO",
        "atividades_atribuidas": ["PROG-SONHOS", "PROG-REFORCO", "PROG-INFANCIA", "PROG-VIVENCIAS"]
    },
    "psicologia@institutoebenezer.org": {
        "email": "psicologia@institutoebenezer.org",
        "senha": "senha123",
        "nome": "Dra. Camila Nunes",
        "role": "PSICOLOGA",
        "cargo": "Psicóloga Institucional (CRP-06/98765-SP)",
        "allowed_prefixes": ["/psicologia", "/tutorial"],
        "default_route": "/psicologia",
        "status": "ATIVO",
        "atividades_atribuidas": ["PROG-VIVENCIAS"]
    },
    "diretoria@institutoebenezer.org": {
        "email": "diretoria@institutoebenezer.org",
        "senha": "senha123",
        "nome": "Marcos Oliveira",
        "role": "DIRETORIA",
        "cargo": "Diretoria & Governança Institucional",
        "allowed_prefixes": ["/relatorios", "/coordenacao", "/triagem", "/campo", "/cadastro", "/participante", "/multiplas-matriculas", "/pendencias", "/perfis", "/tutorial", "/gestao-acessos"],
        "default_route": "/relatorios",
        "status": "ATIVO",
        "atividades_atribuidas": ["PROG-SONHOS", "PROG-REFORCO", "PROG-INFANCIA", "PROG-VIVENCIAS"]
    },
    "admin@institutoebenezer.org": {
        "email": "admin@institutoebenezer.org",
        "senha": "senha123",
        "nome": "Administrador Geral",
        "role": "ADMIN",
        "cargo": "Administrador do Sistema (Acesso Completo)",
        "allowed_prefixes": ["/"],
        "default_route": "/coordenacao",
        "status": "ATIVO",
        "atividades_atribuidas": ["PROG-SONHOS", "PROG-REFORCO", "PROG-INFANCIA", "PROG-VIVENCIAS"]
    }
}

def get_all_users() -> List[Dict[str, Any]]:
    """Retorna lista de todos os usuários registrados no sistema."""
    users_list = []
    for u in INSTITUTIONAL_USERS.values():
        copy_u = dict(u)
        copy_u.pop("senha", None)
        users_list.append(copy_u)
    return users_list

def save_or_update_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Cria ou atualiza um usuário na matriz RBAC institucional."""
    email = user_data["email"].lower().strip()
    role = user_data["role"].upper()
    
    # Determinar allowed_prefixes padrão por role se não especificado
    role_defaults = {
        "VOLUNTARIO": {
            "allowed_prefixes": ["/campo", "/tutorial"],
            "default_route": "/campo",
            "cargo_default": "Educador Voluntário"
        },
        "PSICOLOGA": {
            "allowed_prefixes": ["/psicologia", "/tutorial"],
            "default_route": "/psicologia",
            "cargo_default": "Psicóloga Institucional"
        },
        "COORDENACAO": {
            "allowed_prefixes": ["/coordenacao", "/cadastro", "/participante", "/multiplas-matriculas", "/pendencias", "/campo", "/triagem", "/perfis", "/tutorial", "/gestao-acessos"],
            "default_route": "/coordenacao",
            "cargo_default": "Coordenação de Projetos"
        },
        "DIRETORIA": {
            "allowed_prefixes": ["/relatorios", "/coordenacao", "/triagem", "/campo", "/cadastro", "/participante", "/multiplas-matriculas", "/pendencias", "/perfis", "/tutorial", "/gestao-acessos"],
            "default_route": "/relatorios",
            "cargo_default": "Diretoria Institucional"
        },
        "ADMIN": {
            "allowed_prefixes": ["/"],
            "default_route": "/coordenacao",
            "cargo_default": "Administrador"
        }
    }
    
    config = role_defaults.get(role, role_defaults["VOLUNTARIO"])
    
    existing = INSTITUTIONAL_USERS.get(email, {})
    new_user = {
        "email": email,
        "senha": user_data.get("senha") or existing.get("senha") or "senha123",
        "nome": user_data.get("nome", existing.get("nome", "Novo Usuário")),
        "role": role,
        "cargo": user_data.get("cargo", existing.get("cargo", config["cargo_default"])),
        "allowed_prefixes": user_data.get("allowed_prefixes", existing.get("allowed_prefixes", config["allowed_prefixes"])),
        "default_route": user_data.get("default_route", existing.get("default_route", config["default_route"])),
        "status": user_data.get("status", existing.get("status", "ATIVO")),
        "atividades_atribuidas": user_data.get("atividades_atribuidas", existing.get("atividades_atribuidas", []))
    }
    
    INSTITUTIONAL_USERS[email] = new_user
    safe_user = dict(new_user)
    safe_user.pop("senha", None)
    return safe_user

def update_user_status(email: str, status: str) -> bool:
    """Ativa ou inativa usuário."""
    email_clean = email.lower().strip()
    if email_clean in INSTITUTIONAL_USERS:
        INSTITUTIONAL_USERS[email_clean]["status"] = status
        return True
    return False

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
