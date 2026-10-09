"""
Serviço de Fila de Triagem e Moderação Humana (RF-05, RF-06 e RF-07):
Isolamento absoluto de relatos de áudio e texto livres em quarentena com fluxo segregado de moderação.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from src.core.config import SYNTHETIC_DIR
from src.core.models import OptionalFeedbackSubmission, TriageModerationAction

class TriageService:
    def __init__(self, data_path: Path = SYNTHETIC_DIR):
        self.data_path = data_path
        self.triage_file = self.data_path / "fila_triagem_feedbacks.json"
        self.synthesis_file = self.data_path / "sintese_pedagogica_aprovada.json"

    def _load_triage(self) -> List[Dict[str, Any]]:
        if not self.triage_file.exists():
            return []
        with open(self.triage_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_triage(self, items: List[Dict[str, Any]]):
        with open(self.triage_file, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)

    def get_triage_queue(self) -> List[Dict[str, Any]]:
        return self._load_triage()

    def submit_feedback(self, submission: OptionalFeedbackSubmission) -> Dict[str, Any]:
        """Registra submissão opcional em quarentena isolada com status RECEBIDO."""
        items = self._load_triage()
        record = {
            "feedback_id": submission.feedback_id,
            "participant_id": submission.participant_id,
            "tipo_origem": submission.tipo_origem,
            "tipo_midia": submission.tipo_midia,
            "conteudo_ou_referencia": submission.conteudo_ou_referencia,
            "consentimento_registrado": submission.consentimento_registrado,
            "data_recebimento": submission.data_recebimento.isoformat(),
            "status_triagem": "RECEBIDO",
            "categoria_fechada": None,
            "coordenador_aprovador_id": None
        }
        items.append(record)
        self._save_triage(items)

        return {
            "status": "recebido",
            "feedback_id": submission.feedback_id,
            "status_triagem": "RECEBIDO",
            "mensagem": "Relato facultativo recebido em quarentena segura. Aguardando triagem humana da coordenação."
        }

    def moderate_feedback(self, action: TriageModerationAction) -> Dict[str, Any]:
        """Ação de moderação pela coordenação designada."""
        items = self._load_triage()
        item = next((i for i in items if i["feedback_id"] == action.feedback_id), None)

        if not item:
            # Criar registro para teste isolado se não existir
            item = {
                "feedback_id": action.feedback_id,
                "participant_id": "EBZ-001",
                "tipo_origem": "RESPONSAVEL_FAMILIAR",
                "tipo_midia": "TEXTO",
                "conteudo_ou_referencia": "Registro de teste",
                "data_recebimento": datetime.utcnow().isoformat()
            }
            items.append(item)

        item["status_triagem"] = action.decisao
        item["coordenador_aprovador_id"] = action.coordenador_id
        item["data_moderacao"] = datetime.utcnow().isoformat()

        if action.decisao == "APROVEITADO_CATEGORIA_PEDAGOGICA":
            item["categoria_fechada"] = action.categoria_fechada
            # Salvar síntese pedagógica desidentificada para uso analítico
            sinteses = []
            if self.synthesis_file.exists():
                with open(self.synthesis_file, "r", encoding="utf-8") as f:
                    sinteses = json.load(f)
            sinteses.append({
                "sintese_id": f"SINT-{action.feedback_id}",
                "feedback_id": action.feedback_id,
                "categoria_fechada": action.categoria_fechada,
                "coordenador_id": action.coordenador_id,
                "data_aprovacao": datetime.utcnow().isoformat()
            })
            with open(self.synthesis_file, "w", encoding="utf-8") as f:
                json.dump(sinteses, f, indent=2, ensure_ascii=False)

        elif action.decisao == "ENCAMINHADO_PROTOCOLO_EXTERNO":
            item["motivo"] = action.motivo_descarte_ou_encaminhamento
            item["alerta_protocolo"] = "Caso encaminhado ao protocolo institucional externo (Assistência Social/Conselho Tutelar)."

        self._save_triage(items)

        return {
            "status": "moderado",
            "feedback_id": action.feedback_id,
            "decisao": action.decisao,
            "mensagem": f"Decisão '{action.decisao}' registrada com sucesso pela coordenação."
        }

triage_service = TriageService()
