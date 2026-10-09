"""
Serviço de Master Data Management (MDM):
Gerencia o Golden Record pseudonimizado (EBZ-xxx) e a segregação física dos dados civis.
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
from src.core.config import DATA_DIR, SYNTHETIC_DIR
from src.core.models import ParticipantMDM

class MDMService:
    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path or SYNTHETIC_DIR
        self._participants: Dict[str, ParticipantMDM] = {}
        self._civil_registry: Dict[str, dict] = {}
        self.load_data()

    def load_data(self):
        mdm_file = self.data_path / "mdm_participantes.json"
        civil_file = self.data_path / "cadastro_civil_segregado.json"

        if mdm_file.exists():
            with open(mdm_file, "r", encoding="utf-8") as f:
                items = json.load(f)
                self._participants = {item["participant_id"]: ParticipantMDM(**item) for item in items}

        if civil_file.exists():
            with open(civil_file, "r", encoding="utf-8") as f:
                items = json.load(f)
                self._civil_registry = {item["participant_id"]: item for item in items}

    def get_participants_for_program(self, program_id: str) -> List[ParticipantMDM]:
        """Retorna lista de educandos matriculados no programa em formato puramente pseudonimizado."""
        return [
            p for p in self._participants.values()
            if program_id in p.matriculas_ativas and p.status == "ATIVO"
        ]

    def get_participant_by_id(self, participant_id: str) -> Optional[ParticipantMDM]:
        return self._participants.get(participant_id)

    def get_all_participants(self) -> List[ParticipantMDM]:
        return list(self._participants.values())

    def get_civil_record_restricted(self, participant_id: str, requester_role: str) -> Optional[dict]:
        """Acesso restrito estrito: Somente perfis autorizados de coordenação/diretoria podem consultar dados civis."""
        if requester_role not in ["COORDENACAO", "COORDENACAO_GERAL", "DIRETORIA", "ADMIN"]:
            raise PermissionError("Acesso negado: Perfil não autorizado a consultar dados civis identificáveis.")
        return self._civil_registry.get(participant_id)

    def get_all_civil_records_restricted(self, requester_role: str) -> List[dict]:
        """Acesso restrito estrito: Somente COORDENACAO, DIRETORIA ou ADMIN podem consultar lista civil."""
        if requester_role not in ["COORDENACAO", "COORDENACAO_GERAL", "DIRETORIA", "ADMIN"]:
            raise PermissionError("Acesso negado: Perfil não autorizado a consultar dados civis identificáveis.")
        return list(self._civil_registry.values())

    def register_or_update(self, participant: ParticipantMDM):
        self._participants[participant.participant_id] = participant

    def update_participant_status(self, participant_id: str, new_status: str) -> bool:
        if participant_id in self._participants:
            part = self._participants[participant_id]
            self._participants[participant_id] = ParticipantMDM(
                participant_id=part.participant_id,
                coorte_ano=part.coorte_ano,
                faixa_etaria=part.faixa_etaria,
                matriculas_ativas=part.matriculas_ativas,
                status=new_status
            )
            return True
        return False

    def update_participant_programs(self, participant_id: str, new_programs: List[str]) -> bool:
        if participant_id in self._participants:
            part = self._participants[participant_id]
            self._participants[participant_id] = ParticipantMDM(
                participant_id=part.participant_id,
                coorte_ano=part.coorte_ano,
                faixa_etaria=part.faixa_etaria,
                matriculas_ativas=new_programs,
                status=part.status
            )
            return True
        return False

# Instância singleton
mdm_service = MDMService()
