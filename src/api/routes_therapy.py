"""
Rotas de API para o Módulo de Vivência Terapêutica (Psicologia).
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from src.core.models import TherapySessionMetadata
from src.services.therapy_service import therapy_service

router = APIRouter(prefix="/api/psicologia", tags=["Psicologia"])

@router.get("/sessoes", response_model=List[Dict[str, Any]])
def get_sessions():
    return therapy_service.get_all_sessions()

@router.post("/submeter")
def record_session(session: TherapySessionMetadata):
    try:
        return therapy_service.record_session(session)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
