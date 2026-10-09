"""
Testes do Motor de Métricas, Curvas Longitudinais e Relatórios Agregados (PRD v2.0 / FR-033 / FR-034).
Valida cálculo de evolução socioemocional, taxas de permanência, supressão de pequenas amostras (n < 10)
e presença mandatória de limitações metodológicas.
"""

from src.core.metrics import metrics_engine
from src.core.config import SUPPRESSION_MIN_N

def test_longitudinal_curves_calculation():
    """Valida cálculo de médias por coorte e programa ao longo das semanas com supressão para n < 10."""
    curves = metrics_engine.calculate_longitudinal_curves()
    assert "semanas" in curves
    assert len(curves["semanas"]) > 0
    assert "autonomia" in curves
    assert "convivencia" in curves
    assert "participacao" in curves
    assert "suprimido" in curves
    assert curves["limiar_supressao"] == SUPPRESSION_MIN_N

    # Médias não nulas devem estar estritamente entre 1.0 e 5.0
    for score in curves["autonomia"]:
        if score is not None:
            assert 1.0 <= score <= 5.0

def test_fiscal_dossier_structure():
    """Valida dossier de prestação de contas com carga horária, permanência e limitações metodológicas."""
    dossier = metrics_engine.generate_fiscal_dossier()
    assert "total_carga_horaria_horas" in dossier
    assert "taxa_permanencia_media_percentual" in dossier
    assert "programas_executados" in dossier
    assert "limitacoes_metodologicas" in dossier
    assert len(dossier["limitacoes_metodologicas"]) > 0
    assert dossier["total_carga_horaria_horas"] > 0
    assert 50.0 <= dossier["taxa_permanencia_media_percentual"] <= 100.0

def test_donor_success_summary():
    """Valida resumo executivo com limitações metodológicas, status de aprovação e ausência de falsas promessas."""
    donor_report = metrics_engine.generate_donor_success_report(programa_id="PROG-SONHOS")
    assert "nome_programa" in donor_report
    assert "total_atendidos" in donor_report
    assert "evolucao_pontos_percentuais" in donor_report
    assert "o_que_este_relatorio_nao_afirma" in donor_report
    assert "status_aprovacao" in donor_report
    assert donor_report["status_aprovacao"] in ["GERADO", "REVISADO_COORDENACAO", "APROVADO_DIRETORIA"]
    assert len(donor_report["o_que_este_relatorio_nao_afirma"]) >= 3
