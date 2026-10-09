"""
Serviço do Módulo de Vivência Terapêutica (Psicologia):
Assegura que apenas metadados agregados sejam salvos, sem qualquer anotação clínica individual.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from src.core.config import SYNTHETIC_DIR
from src.core.models import TherapySessionMetadata

class TherapyService:
    def __init__(self, data_path: Path = SYNTHETIC_DIR):
        self.data_path = data_path
        self.therapy_file = self.data_path / "vivencias_terapeuticas.json"

    def get_all_sessions(self) -> List[Dict[str, Any]]:
        if not self.therapy_file.exists():
            return []
        with open(self.therapy_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def record_session(self, session: TherapySessionMetadata) -> Dict[str, Any]:
        sessions = self.get_all_sessions()
        session_id = f"VIV-{session.data_sessao.strftime('%Y%m%d')}"

        record = {
            "vivencia_id": session_id,
            "data": str(session.data_sessao),
            "psicologa_responsavel": session.psicologa_id,
            "duracao_minutos": session.duracao_minutos,
            "total_presentes_agregado": session.total_presentes_agregado,
            "topicos_pedagogicos": session.topicos_pedagogicos
        }
        sessions.append(record)

        with open(self.therapy_file, "w", encoding="utf-8") as f:
            json.dump(sessions, f, indent=2, ensure_ascii=False)

        return {
            "status": "sucesso",
            "vivencia_id": session_id,
            "total_presentes_agregado": session.total_presentes_agregado,
            "duracao_minutos": session.duracao_minutos,
            "mensagem": "Sessão registrada com sucesso em estrita conformidade com o Código de Ética do CFP."
        }

therapy_service = TherapyService()
