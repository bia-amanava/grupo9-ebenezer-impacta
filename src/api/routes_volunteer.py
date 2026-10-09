"""
Rotas da API para a interface de campo do voluntário.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from src.core.models import BatchFieldCollection
from src.services.collection_service import collection_service

router = APIRouter(prefix="/api/voluntario", tags=["Voluntário"])

@router.get("/turma", response_model=List[Dict[str, Any]])
def get_class_roster(programa_id: str = Query(..., description="ID do programa, ex: PROG-SONHOS")):
    roster = collection_service.get_class_roster(programa_id)
    if not roster:
        raise HTTPException(status_code=404, detail="Nenhum participante encontrado para este programa.")
    return roster

@router.post("/submeter")
def submit_attendance(batch: BatchFieldCollection):
    try:
        resultado = collection_service.submit_batch_collection(batch)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
