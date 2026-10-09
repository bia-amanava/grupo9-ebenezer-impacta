"""
Rotas de API para Relatórios de Transparência, Captação e Dossiês Fiscais.
"""

from fastapi import APIRouter, Query, Response
from src.core.metrics import metrics_engine
import json

router = APIRouter(prefix="/api/relatorios", tags=["Relatórios & Captação"])

@router.get("/curvas")
def get_longitudinal_curves(programa_id: str = Query(None)):
    return metrics_engine.calculate_longitudinal_curves(programa_id)

@router.get("/dossie-fiscal")
def get_fiscal_dossier():
    return metrics_engine.generate_fiscal_dossier()

@router.get("/donor-success")
def get_donor_success(programa_id: str = Query("PROG-SONHOS")):
    return metrics_engine.generate_donor_success_report(programa_id)

@router.get("/exportar-csv")
def export_csv():
    """Exporta histórico agregado em CSV para integração com Looker Studio / Excel."""
    curves = metrics_engine.calculate_longitudinal_curves()
    lines = ["Semana,Data,Autonomia_Media,Convivencia_Media,Participacao_Media,Taxa_Presenca_Pct"]
    for i in range(len(curves["semanas"])):
        lines.append(
            f"{curves['semanas'][i]},{curves['datas'][i]},{curves['autonomia'][i]},{curves['convivencia'][i]},{curves['participacao'][i]},{curves['taxa_presenca'][i]}"
        )
    csv_content = "\ufeff" + "\n".join(lines)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ebenezer_impacta_indicadores.csv"}
    )
