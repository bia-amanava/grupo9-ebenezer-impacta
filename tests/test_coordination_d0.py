"""
Testes automatizados do Painel de Coordenação D0 e MDM (US2 / P2).
Valida detecção de pendências no mesmo dia, deduplicação de matrículas e restrição de dados civis.
"""

import pytest
from src.core.mdm import mdm_service
from src.services.coordination_service import coordination_service

def test_mdm_golden_record_uniqueness():
    """Valida que cada participante possui ID único e pode ter múltiplas matrículas ativas."""
    all_students = mdm_service.get_all_participants()
    assert len(all_students) >= 120

    ids = [p.participant_id for p in all_students]
    assert len(ids) == len(set(ids)), "IDs pseudonimizados não podem ter duplicidade."

    # Verifica aluno com múltiplas matrículas
    multi_matricula = [p for p in all_students if len(p.matriculas_ativas) > 1]
    assert len(multi_matricula) > 0

def test_civil_registry_access_restriction():
    """Valida que voluntários ou terceiros NÃO podem acessar dados civis, apenas COORDENACAO_GERAL."""
    p_id = "EBZ-001"

    # Perfil voluntário deve ser bloqueado
    with pytest.raises(PermissionError):
        mdm_service.get_civil_record_restricted(p_id, requester_role="VOLUNTARIO")

    # Perfil coordenação geral deve ter acesso
    civil = mdm_service.get_civil_record_restricted(p_id, requester_role="COORDENACAO_GERAL")
    assert civil is not None
    assert "nome_completo_crianca" in civil

def test_coordination_d0_pending_detection():
    """Valida identificação de oficinas do dia e taxa de conformidade D0."""
    status_d0 = coordination_service.get_d0_dashboard_summary()
    assert "total_oficinas_dia" in status_d0
    assert "taxa_conformidade_d0_percentual" in status_d0
    assert "pendencias" in status_d0
