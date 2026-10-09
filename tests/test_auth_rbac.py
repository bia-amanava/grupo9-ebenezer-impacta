"""
Testes de Autenticação, Controle de Sessão e Matriz de Acesso RBAC (PRD v2.0 - Seção 8.3 / SEC-002).
"""

from fastapi.testclient import TestClient
from src.app import app
from src.core.auth import (
    authenticate_user,
    create_session_token,
    verify_session_token,
    check_route_permission,
    INSTITUTIONAL_USERS,
    SESSION_COOKIE_NAME
)

client = TestClient(app)

def test_user_authentication():
    # Credenciais válidas
    user = authenticate_user("coordenacao@institutoebenezer.org", "senha123")
    assert user is not None
    assert user["role"] == "COORDENACAO"

    # Credenciais inválidas
    invalid_user = authenticate_user("coordenacao@institutoebenezer.org", "senha_errada")
    assert invalid_user is None

def test_session_token_lifecycle():
    token = create_session_token("psicologia@institutoebenezer.org")
    assert token is not None
    assert "." in token

    payload = verify_session_token(token)
    assert payload is not None
    assert payload["role"] == "PSICOLOGA"
    assert payload["email"] == "psicologia@institutoebenezer.org"

def test_rbac_route_permissions():
    voluntario = INSTITUTIONAL_USERS["voluntario@institutoebenezer.org"]
    psicologa = INSTITUTIONAL_USERS["psicologia@institutoebenezer.org"]
    coordenacao = INSTITUTIONAL_USERS["coordenacao@institutoebenezer.org"]

    # Voluntário acessa apenas /campo
    assert check_route_permission(voluntario, "/campo") is True
    assert check_route_permission(voluntario, "/coordenacao") is False
    assert check_route_permission(voluntario, "/relatorios") is False

    # Psicóloga acessa apenas /psicologia
    assert check_route_permission(psicologa, "/psicologia") is True
    assert check_route_permission(psicologa, "/campo") is False

    # Coordenação acessa coordenação e campo
    assert check_route_permission(coordenacao, "/coordenacao") is True
    assert check_route_permission(coordenacao, "/campo") is True

    # Diretoria acessa relatórios, coordenação, triagem, campo (visão executiva ampla)
    diretoria = INSTITUTIONAL_USERS["diretoria@institutoebenezer.org"]
    assert check_route_permission(diretoria, "/relatorios") is True
    assert check_route_permission(diretoria, "/coordenacao") is True
    assert check_route_permission(diretoria, "/campo") is True
    assert check_route_permission(diretoria, "/triagem") is True
    assert check_route_permission(diretoria, "/psicologia") is False

def test_unauthenticated_access_redirects_to_login():
    res = client.get("/campo", follow_redirects=False)
    assert res.status_code == 303
    assert "/login" in res.headers["location"]

    res_root = client.get("/", follow_redirects=False)
    assert res_root.status_code == 303
    assert "/login" in res_root.headers["location"]

def test_api_login_endpoint():
    res = client.post("/api/auth/login", json={
        "email": "coordenacao@institutoebenezer.org",
        "password": "senha123"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "sucesso"
    assert data["usuario"]["role"] == "COORDENACAO"
    assert SESSION_COOKIE_NAME in res.cookies

def test_quick_login_endpoint():
    res = client.post("/api/auth/quick-login", json={"role": "VOLUNTARIO"})
    assert res.status_code == 200
    data = res.json()
    assert data["usuario"]["role"] == "VOLUNTARIO"
    assert data["redirect_url"] == "/campo"
    assert SESSION_COOKIE_NAME in res.cookies

def test_authenticated_access_flow():
    # Login como voluntário
    login_res = client.post("/api/auth/quick-login", json={"role": "VOLUNTARIO"})
    session_cookie = login_res.cookies.get(SESSION_COOKIE_NAME)

    # Acesso autorizado a /campo
    res_campo = client.get("/campo", cookies={SESSION_COOKIE_NAME: session_cookie})
    assert res_campo.status_code == 200
    assert "Chamada de Campo" in res_campo.text

    # Acesso negado a /coordenacao (403)
    res_bloqueado = client.get("/coordenacao", cookies={SESSION_COOKIE_NAME: session_cookie})
    assert res_bloqueado.status_code == 403
    assert "Acesso Não Autorizado" in res_bloqueado.text
