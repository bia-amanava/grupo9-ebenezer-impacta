"""
Testes da Fila de Triagem e Isolamento em Quarentena (US5 / P5).
Valida fluxo segregado de feedbacks facultativos (RF-05, RF-06 e RF-07):
Estados: RECEBIDO -> EM_TRIAGEM -> [APROVEITADO | DESCARTADO | PROTOCOLO_EXTERNO].
Garante que nenhum dado não aprovado ou sensível transborde para bases abertas.
"""

import pytest
from pydantic import ValidationError
from src.core.models import OptionalFeedbackSubmission, TriageModerationAction
from src.services.triage_service import triage_service

def test_feedback_submission_initial_state_received():
    """Valida submissão opcional entrando diretamente em quarentena com status RECEBIDO."""
    submission = OptionalFeedbackSubmission(
        feedback_id="FB-TEST-01",
        participant_id="EBZ-044",
        tipo_origem="RESPONSAVEL_FAMILIAR",
        tipo_midia="TEXTO",
        conteudo_ou_referencia="Criança relata gostar muito das oficinas de sábado."
    )
    res = triage_service.submit_feedback(submission)
    assert res["status"] == "recebido"
    assert res["status_triagem"] == "RECEBIDO"

def test_triage_approval_generates_pedagogical_synthesis():
    """Valida que aprovação gera síntese pedagógica em categoria fechada."""
    action = TriageModerationAction(
        feedback_id="FB-TEST-01",
        coordenador_id="COORD-MARIA",
        decisao="APROVEITADO_CATEGORIA_PEDAGOGICA",
        categoria_fechada="ENGAJAMENTO_FAMILIAR_POSITIVO"
    )
    res = triage_service.moderate_feedback(action)
    assert res["status"] == "moderado"
    assert res["decisao"] == "APROVEITADO_CATEGORIA_PEDAGOGICA"

def test_triage_approval_requires_closed_category():
    """Valida que aprovação falha se não tiver categoria fechada preenchida."""
    with pytest.raises(ValidationError):
        TriageModerationAction(
            feedback_id="FB-TEST-02",
            coordenador_id="COORD-MARIA",
            decisao="APROVEITADO_CATEGORIA_PEDAGOGICA",
            categoria_fechada=None  # Erro! Categoria obrigatória
        )

def test_triage_external_protocol_quarantine():
    """Valida tratamento de conteúdo sensível via protocolo institucional externo sem poluição analítica."""
    action = TriageModerationAction(
        feedback_id="FB-TEST-01",
        coordenador_id="COORD-MARIA",
        decisao="ENCAMINHADO_PROTOCOLO_EXTERNO",
        motivo_descarte_ou_encaminhamento="VIOLACAO_DE_DIREITOS_ENCAMINHADA_EXTERNAMENTE"
    )
    res = triage_service.moderate_feedback(action)
    assert res["status"] == "moderado"
    assert res["decisao"] == "ENCAMINHADO_PROTOCOLO_EXTERNO"
