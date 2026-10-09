"""
Testes Automatizados para os novos módulos de Tutorial e Gestão de Acessos.
Valida:
1. Acesso à página /tutorial para todos os perfis autenticados.
2. Acesso à página /gestao-acessos exclusivo para Coordenação, Diretoria e Admin.
3. Bloqueio de voluntários e psicólogos em /gestao-acessos (403 Forbidden).
4. Operações de API da Gestão de Acessos:
   - Listar usuários
   - Cadastrar/atualizar usuário
   - Alterar status de usuário
   - Atribuir atividades
   - Listar crianças (Zona B e Zona A restrita)
   - Atualizar status e matrículas de crianças
   - Listar atividades e vínculos
"""

from fastapi.testclient import TestClient
from src.app import app
from src.core.auth import (
    create_session_token,
    SESSION_COOKIE_NAME,
    INSTITUTIONAL_USERS
)

client = TestClient(app)

def test_tutorial_page_accessible_by_all_authenticated_users():
    for role in ["VOLUNTARIO", "PSICOLOGA", "COORDENACAO", "DIRETORIA"]:
        login_res = client.post("/api/auth/quick-login", json={"role": role})
        assert login_res.status_code == 200
        cookie = login_res.cookies.get(SESSION_COOKIE_NAME)
        
        res = client.get("/tutorial", cookies={SESSION_COOKIE_NAME: cookie})
        assert res.status_code == 200
        assert "Tutorial &amp; Capacita&#231;&#227;o Interativa" in res.text or "Tutorial" in res.text

def test_access_management_page_permissions():
    # Voluntário bloqueado (403)
    login_vol = client.post("/api/auth/quick-login", json={"role": "VOLUNTARIO"})
    cookie_vol = login_vol.cookies.get(SESSION_COOKIE_NAME)
    res_vol = client.get("/gestao-acessos", cookies={SESSION_COOKIE_NAME: cookie_vol})
    assert res_vol.status_code == 403

    # Psicóloga bloqueada (403)
    login_psi = client.post("/api/auth/quick-login", json={"role": "PSICOLOGA"})
    cookie_psi = login_psi.cookies.get(SESSION_COOKIE_NAME)
    res_psi = client.get("/gestao-acessos", cookies={SESSION_COOKIE_NAME: cookie_psi})
    assert res_psi.status_code == 403

    # Coordenação autorizada (200)
    login_coord = client.post("/api/auth/quick-login", json={"role": "COORDENACAO"})
    cookie_coord = login_coord.cookies.get(SESSION_COOKIE_NAME)
    res_coord = client.get("/gestao-acessos", cookies={SESSION_COOKIE_NAME: cookie_coord})
    assert res_coord.status_code == 200
    assert "Controle de Acessos" in res_coord.text

    # Diretoria autorizada (200)
    login_dir = client.post("/api/auth/quick-login", json={"role": "DIRETORIA"})
    cookie_dir = login_dir.cookies.get(SESSION_COOKIE_NAME)
    res_dir = client.get("/gestao-acessos", cookies={SESSION_COOKIE_NAME: cookie_dir})
    assert res_dir.status_code == 200

def test_management_api_users_crud():
    login_coord = client.post("/api/auth/quick-login", json={"role": "COORDENACAO"})
    cookie_coord = login_coord.cookies.get(SESSION_COOKIE_NAME)

    # 1. Listar usuários
    res_list = client.get("/api/gestao/usuarios", cookies={SESSION_COOKIE_NAME: cookie_coord})
    assert res_list.status_code == 200
    data = res_list.json()
    assert "usuarios" in data
    assert data["total"] >= 4

    # 2. Cadastrar novo voluntário
    new_user = {
        "email": "voluntario.novo@institutoebenezer.org",
        "nome": "Carlos Educador",
        "role": "VOLUNTARIO",
        "cargo": "Educador de Oficinas",
        "status": "ATIVO",
        "atividades_atribuidas": ["PROG-SONHOS"]
    }
    res_create = client.post("/api/gestao/usuarios", json=new_user, cookies={SESSION_COOKIE_NAME: cookie_coord})
    assert res_create.status_code == 200
    assert res_create.json()["usuario"]["nome"] == "Carlos Educador"

    # 3. Alterar status do usuário
    res_status = client.patch(
        "/api/gestao/usuarios/status",
        json={"email": "voluntario.novo@institutoebenezer.org", "status": "INATIVO"},
        cookies={SESSION_COOKIE_NAME: cookie_coord}
    )
    assert res_status.status_code == 200

    # 4. Atribuir atividades
    res_assign = client.post(
        "/api/gestao/usuarios/atribuir-atividades",
        json={"email": "voluntario.novo@institutoebenezer.org", "atividades": ["PROG-SONHOS", "PROG-REFORCO"]},
        cookies={SESSION_COOKIE_NAME: cookie_coord}
    )
    assert res_assign.status_code == 200
    assert "PROG-REFORCO" in res_assign.json()["atividades"]

def test_management_api_children_and_activities():
    login_coord = client.post("/api/auth/quick-login", json={"role": "COORDENACAO"})
    cookie_coord = login_coord.cookies.get(SESSION_COOKIE_NAME)

    # 1. Listar crianças pseudonimizadas
    res_children = client.get("/api/gestao/criancas?include_civil=false", cookies={SESSION_COOKIE_NAME: cookie_coord})
    assert res_children.status_code == 200
    data = res_children.json()
    assert data["total"] > 0
    primeira = data["participantes"][0]
    assert "participant_id" in primeira
    assert "nome_completo" not in primeira  # Zona B não vaza dados civis

    # 2. Listar crianças com dados civis autorizados (Zona A)
    res_civil = client.get("/api/gestao/criancas?include_civil=true", cookies={SESSION_COOKIE_NAME: cookie_coord})
    assert res_civil.status_code == 200
    data_civil = res_civil.json()
    primeira_civil = data_civil["participantes"][0]
    assert "nome_completo" in primeira_civil

    # 3. Alterar status de uma criança
    res_child_status = client.patch(
        "/api/gestao/criancas/status",
        json={"participant_id": "EBZ-001", "status": "INATIVO"},
        cookies={SESSION_COOKIE_NAME: cookie_coord}
    )
    assert res_child_status.status_code == 200

    # 4. Alterar matrículas de uma criança
    res_child_progs = client.patch(
        "/api/gestao/criancas/matriculas",
        json={"participant_id": "EBZ-001", "matriculas_ativas": ["PROG-SONHOS", "PROG-REFORCO"]},
        cookies={SESSION_COOKIE_NAME: cookie_coord}
    )
    assert res_child_progs.status_code == 200
    assert "PROG-REFORCO" in res_child_progs.json()["matriculas_ativas"]

    # 5. Listar atividades com vínculos
    res_acts = client.get("/api/gestao/atividades", cookies={SESSION_COOKIE_NAME: cookie_coord})
    assert res_acts.status_code == 200
    acts_data = res_acts.json()
    assert acts_data["total"] >= 4
