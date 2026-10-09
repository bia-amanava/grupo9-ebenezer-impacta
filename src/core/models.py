"""
Modelos de domínio Pydantic para validação e blindagem de dados da plataforma Ebenézer Impacta.
"""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from src.core.config import ALLOWED_THERAPY_TOPICS, TRIAGE_STATUSES, MIN_INDICATOR_SCORE, MAX_INDICATOR_SCORE

class ParticipantMDM(BaseModel):
    participant_id: str = Field(..., pattern=r"^EBZ-\d{3,}$", description="Identificador único pseudonimizado")
    coorte_ano: int = Field(..., ge=2020, le=2030)
    faixa_etaria: str = Field(..., pattern=r"^(PRIMEIRA_INFANCIA|CRIANCA|ADOLESCENTE)$")
    matriculas_ativas: List[str]
    status: str = Field("ATIVO", pattern=r"^(ATIVO|INATIVO|EGRESSO)$")

class AttendanceScore(BaseModel):
    participant_id: str = Field(..., pattern=r"^EBZ-\d{3,}$")
    presenca: bool
    score_autonomia: Optional[int] = Field(None, ge=MIN_INDICATOR_SCORE, le=MAX_INDICATOR_SCORE)
    score_convivencia: Optional[int] = Field(None, ge=MIN_INDICATOR_SCORE, le=MAX_INDICATOR_SCORE)
    score_participacao: Optional[int] = Field(None, ge=MIN_INDICATOR_SCORE, le=MAX_INDICATOR_SCORE)

    @model_validator(mode="after")
    def validate_scores_consistency(self):
        if not self.presenca:
            if any([self.score_autonomia, self.score_convivencia, self.score_participacao]):
                raise ValueError("Participante ausente não pode receber notas nos indicadores.")
        else:
            if not all([self.score_autonomia, self.score_convivencia, self.score_participacao]):
                raise ValueError("Participante presente deve ter todas as 3 notas preenchidas (1 a 5).")
        return self

class BatchFieldCollection(BaseModel):
    encontro_id: str
    programa_id: str
    data_encontro: date
    educador_id: str
    tempo_preenchimento_segundos: Optional[int] = Field(None, description="Tempo cronometrado em campo")
    avaliacoes: List[AttendanceScore]

    model_config = ConfigDict(extra="forbid")  # Rejeita campos extras como texto aberto ou anexos

class TherapySessionMetadata(BaseModel):
    data_sessao: date
    psicologa_id: str
    duracao_minutos: int = Field(..., ge=15, le=240)
    total_presentes_agregado: int = Field(..., ge=1)
    topicos_pedagogicos: List[str]

    @field_validator("topicos_pedagogicos")
    @classmethod
    def validate_topics(cls, topics: List[str]):
        if not topics:
            raise ValueError("Ao menos um tópico pedagógico deve ser selecionado.")
        for t in topics:
            if t not in ALLOWED_THERAPY_TOPICS:
                raise ValueError(f"Tópico '{t}' não permitido pela taxonomia ética do CFP.")
        return topics

    model_config = ConfigDict(extra="forbid")  # Rejeição estrita de prontuários, notas clínicas ou diagnósticos

class OptionalFeedbackSubmission(BaseModel):
    feedback_id: str
    participant_id: str = Field(..., pattern=r"^EBZ-\d{3,}$")
    tipo_origem: str = Field(..., pattern=r"^(RESPONSAVEL_FAMILIAR|OFICINEIRO)$")
    tipo_midia: str = Field(..., pattern=r"^(TEXTO|AUDIO)$")
    conteudo_ou_referencia: str
    consentimento_registrado: bool = True
    data_recebimento: datetime = Field(default_factory=datetime.utcnow)

class TriageModerationAction(BaseModel):
    feedback_id: str
    coordenador_id: str
    decisao: str = Field(..., pattern=r"^(APROVEITADO_CATEGORIA_PEDAGOGICA|DESCARTADO|ENCAMINHADO_PROTOCOLO_EXTERNO)$")
    categoria_fechada: Optional[str] = None
    motivo_descarte_ou_encaminhamento: Optional[str] = None

    @model_validator(mode="after")
    def validate_moderation(self):
        if self.decisao == "APROVEITADO_CATEGORIA_PEDAGOGICA" and not self.categoria_fechada:
            raise ValueError("Categoria fechada é obrigatória para aprovação pedagógica.")
        return self
