"""
Aplicação Principal Ebenézer Impacta:
Servidor FastAPI integrando controle de acesso por papéis (RBAC),
autenticação segura e interfaces dos módulos operacionais e de governança.
"""

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.api.routes_volunteer import router as volunteer_router
from src.api.routes_coordination import router as coordination_router
from src.api.routes_therapy import router as therapy_router
from src.api.routes_reports import router as reports_router
from src.api.routes_triage import router as triage_router
from src.api.routes_auth import router as auth_router
from src.core.auth import (
    get_current_user_from_request,
    check_route_permission,
    SESSION_COOKIE_NAME
)

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Ebenézer Impacta",
    description="Plataforma de Acompanhamento Ético de Trajetórias e Prestação de Contas (PRD v2.0)",
    version="2.0.0"
)

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Registrar APIs REST
app.include_router(auth_router)
app.include_router(volunteer_router)
app.include_router(coordination_router)
app.include_router(therapy_router)
app.include_router(reports_router)
app.include_router(triage_router)

def render_secured_page(request: Request, template_name: str, active_page: str, extra_context: dict = None):
    """
    Garante autenticação prévia e controle de acesso RBAC (PRD v2.0 Seção 8.3).
    Redireciona para /login se não autenticado; exibe tela 403 se rota não autorizada ao perfil.
    """
    user = get_current_user_from_request(request)
    if not user:
        return RedirectResponse(url=f"/login?next={request.url.path}", status_code=303)
    
    if not check_route_permission(user, request.url.path):
        return templates.TemplateResponse(
            request=request,
            name="acesso_negado.html",
            context={"user": user, "path": request.url.path},
            status_code=403
        )
    
    ctx = {
        "user": user,
        "active_page": active_page,
        **(extra_context or {})
    }
    return templates.TemplateResponse(request=request, name=template_name, context=ctx)

# --------------------------------------------------------------------------
# Rotas de Autenticação e Entrada
# --------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    user = get_current_user_from_request(request)
    if user:
        return RedirectResponse(url=user["default_route"], status_code=303)
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def page_login(request: Request, force: bool = False):
    user = get_current_user_from_request(request)
    if user and not force:
        return RedirectResponse(url=user["default_route"], status_code=303)
    resp = templates.TemplateResponse(request=request, name="login.html", context={})
    if force:
        resp.delete_cookie(key=SESSION_COOKIE_NAME)
    return resp

@app.get("/logout")
def logout(response: Response):
    resp = RedirectResponse(url="/login?force=true", status_code=303)
    resp.delete_cookie(key=SESSION_COOKIE_NAME)
    return resp

@app.get("/acesso-negado", response_class=HTMLResponse)
def page_access_denied(request: Request):
    user = get_current_user_from_request(request)
    return templates.TemplateResponse(
        request=request,
        name="acesso_negado.html",
        context={"user": user, "path": request.url.path}
    )

@app.get("/perfis", response_class=HTMLResponse)
def page_profiles(request: Request):
    return render_secured_page(request, "selecao_perfil.html", "coordenacao")

# --------------------------------------------------------------------------
# Módulos Funcionais Protegidos por RBAC
# --------------------------------------------------------------------------

@app.get("/campo", response_class=HTMLResponse)
def page_volunteer(request: Request):
    return render_secured_page(request, "campo_voluntario.html", "campo")

@app.get("/campo/home", response_class=HTMLResponse)
def page_volunteer_home(request: Request):
    return render_secured_page(request, "home_voluntario.html", "campo")

@app.get("/campo/indicadores", response_class=HTMLResponse)
def page_indicators(request: Request):
    return render_secured_page(request, "indicadores_participacao.html", "campo")

@app.get("/campo/revisar", response_class=HTMLResponse)
def page_review_submission(request: Request):
    return render_secured_page(request, "revisar_envio.html", "campo")

@app.get("/campo/sucesso", response_class=HTMLResponse)
def page_volunteer_success(request: Request):
    return render_secured_page(request, "sucesso_voluntario.html", "campo")

@app.get("/coordenacao", response_class=HTMLResponse)
def page_coordination(request: Request):
    return render_secured_page(request, "coordenacao_d0.html", "coordenacao")

@app.get("/cadastro", response_class=HTMLResponse)
def page_master_data(request: Request):
    return render_secured_page(request, "cadastro_mestre.html", "coordenacao")

@app.get("/participante/{participant_id}", response_class=HTMLResponse)
def page_participant_details(participant_id: str, request: Request):
    return render_secured_page(request, "detalhes_participante.html", "coordenacao", {"participant_id": participant_id})

@app.get("/multiplas-matriculas", response_class=HTMLResponse)
def page_multiple_enrollments(request: Request):
    return render_secured_page(request, "multiplas_matriculas.html", "coordenacao")

@app.get("/pendencias", response_class=HTMLResponse)
def page_pendencias(request: Request):
    return render_secured_page(request, "pendencias_semana.html", "coordenacao")

@app.get("/psicologia", response_class=HTMLResponse)
def page_therapy(request: Request):
    return render_secured_page(request, "vivencia_psicologia.html", "psicologia")

@app.get("/psicologia/sucesso", response_class=HTMLResponse)
def page_therapy_success(request: Request):
    return render_secured_page(request, "sucesso_vivencia.html", "psicologia")

@app.get("/triagem", response_class=HTMLResponse)
def page_triage(request: Request):
    return render_secured_page(request, "triagem_escuta.html", "triagem")

@app.get("/relatorios", response_class=HTMLResponse)
def page_reports(request: Request):
    return render_secured_page(request, "relatorios_captacao.html", "relatorios")

@app.get("/relatorios/exportar", response_class=HTMLResponse)
def page_export_options(request: Request):
    return render_secured_page(request, "exportacao_relatorio.html", "relatorios")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)
