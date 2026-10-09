"""
Testes do Motor de Métricas, Curvas Longitudinais e Dossiê Fiscal (US4 / P4).
Valida cálculo de evolução socioemocional, taxas de permanência e estrutura para Lei Rouanet / Lucro Real.
"""

from src.core.metrics import metrics_engine

def test_longitudinal_curves_calculation():
    """Valida cálculo de médias por coorte e programa ao longo das semanas."""
    curves = metrics_engine.calculate_longitudinal_curves()
    assert "semanas" in curves
    assert len(curves["semanas"]) > 0
    assert "autonomia" in curves
    assert "convivencia" in curves
    assert "participacao" in curves

    # Médias devem estar estritamente entre 1.0 e 5.0
    for score in curves["autonomia"]:
        assert 1.0 <= score <= 5.0

def test_fiscal_dossier_structure():
    """Valida dossier de prestação de contas fiscais com carga horária e permanência."""
    dossier = metrics_engine.generate_fiscal_dossier()
    assert "total_carga_horaria_horas" in dossier
    assert "taxa_permanencia_media_percentual" in dossier
    assert "programas_executados" in dossier
    assert dossier["total_carga_horaria_horas"] > 0
    assert 50.0 <= dossier["taxa_permanencia_media_percentual"] <= 100.0

def test_donor_success_summary():
    """Valida resumo executivo de 2 páginas para retenção de doadores (mitigação de R$ 16k/ano)."""
    donor_report = metrics_engine.generate_donor_success_report(programa_id="PROG-SONHOS")
    assert "nome_programa" in donor_report
    assert "total_atendidos" in donor_report
    assert "evolucao_pontos_percentuais" in donor_report
    assert "retencao_doadores_impacto" in donor_report
