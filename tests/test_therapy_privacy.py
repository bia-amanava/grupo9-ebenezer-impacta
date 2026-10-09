"""
Testes de Blindagem Ética do Módulo de Psicologia (US3 / P3).
Valida cumprimento rigoroso do Código de Ética do CFP e LGPD:
Rejeição estrita de prontuários individuais, notas clínicas, CID e garantia de metadados agregados.
"""

import pytest
from datetime import date
from pydantic import ValidationError
from src.core.models import TherapySessionMetadata
from src.services.therapy_service import therapy_service

def test_therapy_session_valid_metadata():
    """Valida registro com metadados agregados permitidos."""
    session = TherapySessionMetadata(
        data_sessao=date.today(),
        psicologa_id="CRP-06/98765-SP",
        duracao_minutos=90,
        total_presentes_agregado=22,
        topicos_pedagogicos=["AUTOCUIDADO_E_HIGIENE", "REGULACAO_EMOCIONAL"]
    )
    assert session.duracao_minutos == 90
    assert session.total_presentes_agregado == 22

def test_therapy_session_forbids_clinical_notes_or_names():
    """Valida rejeição imediata se qualquer campo de prontuário, diagnóstico ou nome de aluno for injetado."""
    with pytest.raises(ValidationError):
        TherapySessionMetadata(
            data_sessao=date.today(),
            psicologa_id="CRP-06/98765-SP",
            duracao_minutos=60,
            total_presentes_agregado=15,
            topicos_pedagogicos=["REGULACAO_EMOCIONAL"],
            prontuario_clinico="Paciente relatou ansiedade severa",  # PROIBIDO!
            cid_diagnostico="F41.1"  # PROIBIDO!
        )

def test_therapy_session_forbids_invalid_topic():
    """Valida que apenas tópicos da taxonomia ética pré-aprovada são aceitos."""
    with pytest.raises(ValidationError):
        TherapySessionMetadata(
            data_sessao=date.today(),
            psicologa_id="CRP-06/98765-SP",
            duracao_minutos=60,
            total_presentes_agregado=15,
            topicos_pedagogicos=["TOPICO_INVALIDO_NAO_HOMOLOGADO"]
        )

def test_therapy_service_persistence():
    """Valida persistência e recuperação segura dos metadados das sessões."""
    session = TherapySessionMetadata(
        data_sessao=date.today(),
        psicologa_id="CRP-06/98765-SP",
        duracao_minutos=120,
        total_presentes_agregado=25,
        topicos_pedagogicos=["CONVIVENCIA_E_VINCULO", "RESOLUCAO_PACIFICA_DE_CONFLITOS"]
    )
    result = therapy_service.record_session(session)
    assert result["status"] == "sucesso"
    assert result["total_presentes_agregado"] == 25
