"""
Rotas de API para a Fila de Triagem e Moderação Humana (RF-05, RF-06 e RF-07).
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from src.core.models import OptionalFeedbackSubmission, TriageModerationAction
from src.services.triage_service import triage_service

router = APIRouter(prefix="/api/triagem", tags=["Triagem"])

@router.get("/fila", response_model=List[Dict[str, Any]])
def get_triage_queue():
    return triage_service.get_triage_queue()

@router.post("/submeter")
def submit_optional_feedback(submission: OptionalFeedbackSubmission):
    try:
        return triage_service.submit_feedback(submission)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/moderar")
def moderate_feedback(action: TriageModerationAction):
    try:
        return triage_service.moderate_feedback(action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
