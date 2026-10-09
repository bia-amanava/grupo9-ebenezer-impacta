"""
Testes de Blindagem Ética do Módulo de Psicologia (PRD v2.0 / FR-020 / US-05).
Valida cumprimento rigoroso do Código de Ética do CFP e LGPD:
Rejeição estrita de prontuários individuais, notas clínicas, CID e garantia de metadados agregados e checklist.
"""

import pytest
from datetime import date
from pydantic import ValidationError
from src.core.models import TherapySessionMetadata
from src.services.therapy_service import therapy_service

def test_therapy_session_valid_metadata():
    """Valida registro com metadados agregados permitidos e checklist de infraestrutura."""
    session = TherapySessionMetadata(
        realizada=True,
        data_sessao=date.today(),
        psicologa_id="CRP-06/98765-SP",
        duracao_minutos=90,
        total_presentes_agregado=22,
        checklist_infra=["SALA_COM_PRIVACIDADE_ACUSTICA", "MATERIAIS_LUDICOS_E_EXPRESSIVOS"],
        topicos_pedagogicos=["AUTOCUIDADO_E_HIGIENE", "REGULACAO_EMOCIONAL"]
    )
    assert session.realizada is True
    assert session.duracao_minutos == 90
    assert session.total_presentes_agregado == 22
    assert "SALA_COM_PRIVACIDADE_ACUSTICA" in session.checklist_infra

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
        realizada=True,
        data_sessao=date.today(),
        psicologa_id="CRP-06/98765-SP",
        duracao_minutos=120,
        total_presentes_agregado=25,
        checklist_infra=["VENTILACAO_E_AGUA_POTAVEL"],
        topicos_pedagogicos=["CONVIVENCIA_E_VINCULO", "RESOLUCAO_PACIFICA_DE_CONFLITOS"]
    )
    result = therapy_service.record_session(session)
    assert result["status"] == "sucesso"
    assert result["total_presentes_agregado"] == 25
    assert result["realizada"] is True
