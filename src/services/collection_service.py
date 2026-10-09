"""
Serviço de Coleta de Campo do Voluntário:
Processa chamadas e avaliações socioemocionais em escalas fechadas, com validação de performance (<3 min).
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
from src.core.config import SYNTHETIC_DIR
from src.core.models import BatchFieldCollection
from src.core.mdm import mdm_service

class CollectionService:
    def __init__(self, data_path: Path = SYNTHETIC_DIR):
        self.data_path = data_path
        self.evaluations_file = self.data_path / "avaliacoes_socioemocionais.json"
        self.encounters_file = self.data_path / "encontros_operacionais.json"

    def get_class_roster(self, program_id: str) -> List[Dict[str, Any]]:
        """Retorna os alunos ativos matriculados na oficina com formato pseudonimizado e seguro."""
        participants = mdm_service.get_participants_for_program(program_id)
        # Ordenar por ID para interface mobile previsível
        participants.sort(key=lambda p: p.participant_id)
        return [
            {
                "participant_id": p.participant_id,
                "coorte_ano": p.coorte_ano,
                "faixa_etaria": p.faixa_etaria
            }
            for p in participants
        ]

    def submit_batch_collection(self, batch: BatchFieldCollection) -> Dict[str, Any]:
        """Processa a submissão da chamada e persiste os registros."""
        # Carregar registros existentes
        avaliacoes = []
        if self.evaluations_file.exists():
            with open(self.evaluations_file, "r", encoding="utf-8") as f:
                avaliacoes = json.load(f)

        now_str = datetime.now(timezone.utc).isoformat()
        total_presentes = 0

        for item in batch.avaliacoes:
            if item.presenca:
                total_presentes += 1
            avaliacoes.append({
                "avaliacao_id": f"AV-{batch.encontro_id}-{item.participant_id}",
                "encontro_id": batch.encontro_id,
                "participant_id": item.participant_id,
                "presenca": item.presenca,
                "score_autonomia": item.score_autonomia,
                "score_convivencia": item.score_convivencia,
                "score_participacao": item.score_participacao,
                "timestamp_registro": now_str
            })

        # Salvar registros
        with open(self.evaluations_file, "w", encoding="utf-8") as f:
            json.dump(avaliacoes, f, indent=2, ensure_ascii=False)

        # Atualizar status do encontro
        encontros = []
        if self.encounters_file.exists():
            with open(self.encounters_file, "r", encoding="utf-8") as f:
                encontros = json.load(f)

        encontro_existente = next((e for e in encontros if e["encontro_id"] == batch.encontro_id), None)
        if encontro_existente:
            encontro_existente["status_lancamento"] = "D0_NO_PRAZO"
            encontro_existente["data_envio_registro"] = now_str
        else:
            encontros.append({
                "encontro_id": batch.encontro_id,
                "programa_id": batch.programa_id,
                "data_encontro": str(batch.data_encontro),
                "horario_inicio": "09:00",
                "horario_fim": "11:00",
                "educador_id": batch.educador_id,
                "data_envio_registro": now_str,
                "status_lancamento": "D0_NO_PRAZO"
            })

        with open(self.encounters_file, "w", encoding="utf-8") as f:
            json.dump(encontros, f, indent=2, ensure_ascii=False)

        return {
            "status": "sucesso",
            "encontro_id": batch.encontro_id,
            "total_alunos_avaliados": len(batch.avaliacoes),
            "total_presentes": total_presentes,
            "tempo_segundos": batch.tempo_preenchimento_segundos,
            "dentro_da_meta_3min": (batch.tempo_preenchimento_segundos or 0) <= 180,
            "mensagem": "Chamada e avaliação socioemocional registradas com sucesso em D0."
        }

collection_service = CollectionService()
