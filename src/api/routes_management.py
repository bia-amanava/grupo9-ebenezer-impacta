"""
Rotas de API para Gestão e Controle de Acessos (Diretoria e Coordenação Geral).
Permite administrar:
1. Usuários e Perfis RBAC (Voluntários, Psicólogos, Coordenação, Diretoria)
2. Controle de Acesso e Matrículas das Crianças (Zona A / Zona B)
3. Atividades, Oficinas e Atribuições
"""

from fastapi import APIRouter, Request, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from src.core.auth import (
    get_current_user_from_request,
    get_all_users,
    save_or_update_user,
    update_user_status,
    INSTITUTIONAL_USERS
)
from src.core.mdm import mdm_service
from src.core.config import PROGRAMS

router = APIRouter(prefix="/api/gestao", tags=["Gestão e Controle de Acessos"])

def ensure_management_role(request: Request) -> Dict[str, Any]:
    """Valida se o usuário autenticado possui perfil de DIRETORIA, COORDENACAO ou ADMIN."""
    user = get_current_user_from_request(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação exigida para acessar este recurso."
        )
    if user.get("role") not in ["DIRETORIA", "COORDENACAO", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Somente Diretoria e Coordenação podem gerenciar acessos."
        )
    return user

# --------------------------------------------------------------------------
# Modelos de Requisição
# --------------------------------------------------------------------------

class UserCreateOrUpdateRequest(BaseModel):
    email: str
    nome: str
    role: str
    cargo: Optional[str] = None
    senha: Optional[str] = "senha123"
    status: Optional[str] = "ATIVO"
    atividades_atribuidas: Optional[List[str]] = []

class UserStatusUpdateRequest(BaseModel):
    email: str
    status: str

class ChildStatusUpdateRequest(BaseModel):
    participant_id: str
    status: str

class ChildProgramsUpdateRequest(BaseModel):
    participant_id: str
    matriculas_ativas: List[str]

class UserActivityAssignmentRequest(BaseModel):
    email: str
    atividades: List[str]

# --------------------------------------------------------------------------
# Endpoints de Gestão de Usuários
# --------------------------------------------------------------------------

@router.get("/usuarios")
def list_users(request: Request):
    """Lista todos os voluntários, psicólogos e gestores cadastrados."""
    ensure_management_role(request)
    return {
        "usuarios": get_all_users(),
        "total": len(INSTITUTIONAL_USERS)
    }

@router.post("/usuarios")
def save_user(payload: UserCreateOrUpdateRequest, request: Request):
    """Cadastra ou atualiza um usuário com suas respectivas permissões."""
    operator = ensure_management_role(request)
    saved = save_or_update_user(payload.model_dump())
    return {
        "status": "sucesso",
        "mensagem": f"Usuário {saved['nome']} ({saved['email']}) salvo com sucesso.",
        "usuario": saved,
        "operador": operator["nome"]
    }

@router.patch("/usuarios/status")
def toggle_user_status(payload: UserStatusUpdateRequest, request: Request):
    """Ativa ou inativa o acesso de um usuário ao sistema."""
    ensure_management_role(request)
    success = update_user_status(str(payload.email), payload.status.upper())
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    return {
        "status": "sucesso",
        "mensagem": f"Status de {payload.email} alterado para {payload.status.upper()}."
    }

@router.post("/usuarios/atribuir-atividades")
def assign_activities_to_user(payload: UserActivityAssignmentRequest, request: Request):
    """Atribui oficinas e turmas de atuação para voluntários ou psicólogos."""
    ensure_management_role(request)
    email = str(payload.email).lower().strip()
    if email not in INSTITUTIONAL_USERS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    
    INSTITUTIONAL_USERS[email]["atividades_atribuidas"] = payload.atividades
    return {
        "status": "sucesso",
        "mensagem": f"Atividades atualizadas para {email}.",
        "atividades": payload.atividades
    }

# --------------------------------------------------------------------------
# Endpoints de Gestão do Cadastro das Crianças (Zonas A e B)
# --------------------------------------------------------------------------

@router.get("/criancas")
def list_children(request: Request, include_civil: bool = False):
    """
    Retorna a lista de crianças registradas no MDM.
    Se include_civil for True, traz o cadastro civil segregado (Zona A),
    restrito à governança.
    """
    operator = ensure_management_role(request)
    participants = mdm_service.get_all_participants()
    
    civil_lookup = {}
    if include_civil:
        civil_records = mdm_service.get_all_civil_records_restricted(operator["role"])
        civil_lookup = {c["participant_id"]: c for c in civil_records}
    
    result = []
    for p in participants:
        item = {
            "participant_id": p.participant_id,
            "faixa_etaria": p.faixa_etaria,
            "coorte_ano": p.coorte_ano,
            "matriculas_ativas": p.matriculas_ativas,
            "status": p.status
        }
        if include_civil and p.participant_id in civil_lookup:
            c = civil_lookup[p.participant_id]
            item["nome_completo"] = c.get("nome_completo", "Não informado")
            item["nome_responsavel"] = c.get("nome_responsavel", "Não informado")
            item["telefone_contato"] = c.get("telefone_contato", "Não informado")
        result.append(item)
        
    return {
        "total": len(result),
        "participantes": result,
        "zona_consultada": "Zona A + B" if include_civil else "Zona B (Pseudonimizada)"
    }

@router.patch("/criancas/status")
def toggle_child_status(payload: ChildStatusUpdateRequest, request: Request):
    """Ativa, inativa ou marca como egresso o cadastro de uma criança."""
    ensure_management_role(request)
    success = mdm_service.update_participant_status(payload.participant_id, payload.status.upper())
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Criança não encontrada no MDM.")
    return {
        "status": "sucesso",
        "mensagem": f"Status do participante {payload.participant_id} atualizado para {payload.status.upper()}."
    }

@router.patch("/criancas/matriculas")
def update_child_programs(payload: ChildProgramsUpdateRequest, request: Request):
    """Atualiza as oficinas/programas em que a criança está matriculada."""
    ensure_management_role(request)
    success = mdm_service.update_participant_programs(payload.participant_id, payload.matriculas_ativas)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Criança não encontrada no MDM.")
    return {
        "status": "sucesso",
        "mensagem": f"Matrículas de {payload.participant_id} atualizadas com sucesso.",
        "matriculas_ativas": payload.matriculas_ativas
    }

# --------------------------------------------------------------------------
# Endpoints de Gestão de Atividades & Oficinas
# --------------------------------------------------------------------------

@router.get("/atividades")
def list_activities(request: Request):
    """Lista as oficinas do Instituto Ebenézer com seus dados e voluntários vinculados."""
    ensure_management_role(request)
    
    # Mapear educadores por atividade
    educators_by_activity = {}
    for email, u in INSTITUTIONAL_USERS.items():
        for act in u.get("atividades_atribuidas", []):
            if act not in educators_by_activity:
                educators_by_activity[act] = []
            educators_by_activity[act].append({
                "nome": u["nome"],
                "email": u["email"],
                "role": u["role"],
                "cargo": u["cargo"]
            })
            
    activities_summary = []
    all_participants = mdm_service.get_all_participants()
    
    for prog in PROGRAMS:
        enrolled_count = len([p for p in all_participants if prog["id"] in p.matriculas_ativas and p.status == "ATIVO"])
        activities_summary.append({
            "id": prog["id"],
            "nome": prog["nome"],
            "dia": prog["dia"],
            "carga_horaria_minutos": prog["carga_horaria_minutos"],
            "eixo": prog["eixo"],
            "total_matriculados": enrolled_count,
            "educadores_vinculados": educators_by_activity.get(prog["id"], [])
        })
        
    return {
        "total": len(activities_summary),
        "atividades": activities_summary
    }
