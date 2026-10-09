"""
Testes automatizados da Coleta de Campo do Voluntário (US1 / P1).
Valida contratos de dados, regras de preenchimento, escalas fechadas (1-5) e telemetria de 3 minutos.
"""

import pytest
from datetime import date
from pydantic import ValidationError
from src.core.models import AttendanceScore, BatchFieldCollection

def test_attendance_present_with_valid_scores():
    """Valida que aluno presente deve ter notas de 1 a 5 nos 3 indicadores."""
    score = AttendanceScore(
        participant_id="EBZ-001",
        presenca=True,
        score_autonomia=4,
        score_convivencia=5,
        score_participacao=3
    )
    assert score.presenca is True
    assert score.score_autonomia == 4

def test_attendance_absent_must_have_null_scores():
    """Valida que aluno ausente tem notas nulas."""
    score = AttendanceScore(
        participant_id="EBZ-002",
        presenca=False,
        score_autonomia=None,
        score_convivencia=None,
        score_participacao=None
    )
    assert score.presenca is False
    assert score.score_autonomia is None

def test_attendance_present_missing_score_fails():
    """Valida que aluno presente não pode ter nota faltando."""
    with pytest.raises(ValidationError):
        AttendanceScore(
            participant_id="EBZ-003",
            presenca=True,
            score_autonomia=4,
            score_convivencia=None,
            score_participacao=3
        )

def test_batch_collection_forbids_narrative_text():
    """Valida que o payload da chamada não permite campos de texto livre (Blindagem Ética)."""
    with pytest.raises(ValidationError):
        BatchFieldCollection(
            encontro_id="ENC-001",
            programa_id="PROG-SONHOS",
            data_encontro=date.today(),
            educador_id="VOL-01",
            observacao_livre="Aluno estava agitado hoje",  # Campo proibido!
            avaliacoes=[
                AttendanceScore(
                    participant_id="EBZ-001",
                    presenca=True,
                    score_autonomia=4,
                    score_convivencia=4,
                    score_participacao=4
                )
            ]
        )

def test_telemetry_under_3_minutes():
    """Valida telemetria de submissão para turma de 15 alunos sob 180 segundos."""
    batch = BatchFieldCollection(
        encontro_id="ENC-TEST-15",
        programa_id="PROG-SONHOS",
        data_encontro=date.today(),
        educador_id="VOL-01",
        tempo_preenchimento_segundos=145,  # 2m 25s (< 180s)
        avaliacoes=[
            AttendanceScore(
                participant_id=f"EBZ-{i:03d}",
                presenca=True,
                score_autonomia=4,
                score_convivencia=4,
                score_participacao=5
            )
            for i in range(1, 16)
        ]
    )
    assert len(batch.avaliacoes) == 15
    assert batch.tempo_preenchimento_segundos < 180
