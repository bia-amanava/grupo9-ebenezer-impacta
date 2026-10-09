"""
Rotas de API para o Painel de Coordenação D0 e MDM.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any
from src.services.coordination_service import coordination_service

router = APIRouter(prefix="/api/coordenacao", tags=["Coordenação"])

@router.get("/d0")
def get_d0_dashboard():
    return coordination_service.get_d0_dashboard_summary()

@router.get("/mdm")
def get_mdm_summary():
    return coordination_service.get_mdm_summary()

@router.post("/cobrar")
def notify_educator(encontro_id: str = Query(...)):
    return coordination_service.trigger_educator_reminder(encontro_id)
