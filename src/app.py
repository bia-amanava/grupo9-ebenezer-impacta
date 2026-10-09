"""
Aplicação Principal Ebenézer Impacta:
Servidor FastAPI integrando todas as rotas de API e interfaces dos 4 módulos + Fila de Triagem.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.api.routes_volunteer import router as volunteer_router
from src.api.routes_coordination import router as coordination_router
from src.api.routes_therapy import router as therapy_router
from src.api.routes_reports import router as reports_router
from src.api.routes_triage import router as triage_router

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Ebenézer Impacta",
    description="Plataforma de Monitoramento Ético e Emissão do Relatório de Transparência e Captação",
    version="1.1.0"
)

# Montar arquivos estáticos se necessário
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Registrar APIs
app.include_router(volunteer_router)
app.include_router(coordination_router)
app.include_router(therapy_router)
app.include_router(reports_router)
app.include_router(triage_router)

# Rotas de Frontend (Templates HTML)
@app.get("/", response_class=HTMLResponse)
def index():
    return RedirectResponse(url="/campo")

@app.get("/campo", response_class=HTMLResponse)
def page_volunteer(request: Request):
    return templates.TemplateResponse(request=request, name="campo_voluntario.html", context={"active_page": "campo"})

@app.get("/coordenacao", response_class=HTMLResponse)
def page_coordination(request: Request):
    return templates.TemplateResponse(request=request, name="coordenacao_d0.html", context={"active_page": "coordenacao"})

@app.get("/psicologia", response_class=HTMLResponse)
def page_therapy(request: Request):
    return templates.TemplateResponse(request=request, name="vivencia_psicologia.html", context={"active_page": "psicologia"})

@app.get("/triagem", response_class=HTMLResponse)
def page_triage(request: Request):
    return templates.TemplateResponse(request=request, name="triagem_escuta.html", context={"active_page": "triagem"})

@app.get("/login", response_class=HTMLResponse)
def page_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})

@app.get("/cadastro", response_class=HTMLResponse)
def page_master_data(request: Request):
    return templates.TemplateResponse(request=request, name="cadastro_mestre.html", context={"active_page": "coordenacao"})

@app.get("/participante/{participant_id}", response_class=HTMLResponse)
def page_participant_details(participant_id: str, request: Request):
    return templates.TemplateResponse(request=request, name="detalhes_participante.html", context={"participant_id": participant_id, "active_page": "coordenacao"})

@app.get("/multiplas-matriculas", response_class=HTMLResponse)
def page_multiple_enrollments(request: Request):
    return templates.TemplateResponse(request=request, name="multiplas_matriculas.html", context={"active_page": "coordenacao"})

@app.get("/relatorios", response_class=HTMLResponse)
def page_reports(request: Request):
    return templates.TemplateResponse(request=request, name="relatorios_captacao.html", context={"active_page": "relatorios"})

@app.get("/perfis", response_class=HTMLResponse)
def page_profiles(request: Request):
    return templates.TemplateResponse(request=request, name="selecao_perfil.html", context={})

@app.get("/campo/indicadores", response_class=HTMLResponse)
def page_indicators(request: Request):
    return templates.TemplateResponse(request=request, name="indicadores_participacao.html", context={"active_page": "campo"})

@app.get("/campo/revisar", response_class=HTMLResponse)
def page_review_submission(request: Request):
    return templates.TemplateResponse(request=request, name="revisar_envio.html", context={"active_page": "campo"})

@app.get("/pendencias", response_class=HTMLResponse)
def page_pendencias(request: Request):
    return templates.TemplateResponse(request=request, name="pendencias_semana.html", context={"active_page": "coordenacao"})

@app.get("/campo/home", response_class=HTMLResponse)
def page_volunteer_home(request: Request):
    return templates.TemplateResponse(request=request, name="home_voluntario.html", context={"active_page": "campo"})

@app.get("/campo/sucesso", response_class=HTMLResponse)
def page_volunteer_success(request: Request):
    return templates.TemplateResponse(request=request, name="sucesso_voluntario.html", context={"active_page": "campo"})

@app.get("/psicologia/sucesso", response_class=HTMLResponse)
def page_therapy_success(request: Request):
    return templates.TemplateResponse(request=request, name="sucesso_vivencia.html", context={"active_page": "psicologia"})

@app.get("/relatorios/exportar", response_class=HTMLResponse)
def page_export_options(request: Request):
    return templates.TemplateResponse(request=request, name="exportacao_relatorio.html", context={"active_page": "relatorios"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)
