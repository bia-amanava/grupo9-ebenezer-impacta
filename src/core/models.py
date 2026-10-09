"""
Modelos de domínio Pydantic para validação, integridade relacional e blindagem bioética (PRD v2.0).
Plataforma Ebenézer Impacta.
"""

from datetime import date, datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from src.core.config import (
    ALLOWED_THERAPY_TOPICS,
    PSYCHOLOGY_INFRA_CHECKLIST,
    REPORT_APPROVAL_STATUSES,
    TRIAGE_STATUSES,
    MIN_INDICATOR_SCORE,
    MAX_INDICATOR_SCORE
)

class ParticipantMDM(BaseModel):
    """Entidade mestre de participante pseudonimizado (Golden Record - Zona B)."""
    participant_id: str = Field(..., pattern=r"^EBZ-\d{3,}$", description="Identificador único pseudonimizado")
    coorte_ano: int = Field(..., ge=2020, le=2030)
    faixa_etaria: str = Field(..., pattern=r"^(PRIMEIRA_INFANCIA|CRIANCA|ADOLESCENTE)$")
    matriculas_ativas: List[str]
    status: str = Field("ATIVO", pattern=r"^(ATIVO|INATIVO|EGRESSO)$")

class AttendanceScore(BaseModel):
    """Marcação de presença e 3 indicadores em escalas fechadas (FR-010 / FR-011 - Zona B)."""
    participant_id: str = Field(..., pattern=r"^EBZ-\d{3,}$")
    presenca: bool
    score_autonomia: Optional[int] = Field(None, ge=MIN_INDICATOR_SCORE, le=MAX_INDICATOR_SCORE)
    score_convivencia: Optional[int] = Field(None, ge=MIN_INDICATOR_SCORE, le=MAX_INDICATOR_SCORE)
    score_participacao: Optional[int] = Field(None, ge=MIN_INDICATOR_SCORE, le=MAX_INDICATOR_SCORE)
    nao_observado: bool = False
    justificativa_nao_observado: Optional[str] = Field(None, pattern=r"^(ATIVIDADE_NAO_PROPICIA|SAIDA_ANTECIPADA|NAO_AVALIADO)$")

    @model_validator(mode="after")
    def validate_scores_consistency(self):
        if not self.presenca:
            if any([self.score_autonomia, self.score_convivencia, self.score_participacao]):
                raise ValueError("Participante ausente não pode receber notas nos indicadores.")
        else:
            if not self.nao_observado:
                if not all([self.score_autonomia, self.score_convivencia, self.score_participacao]):
                    raise ValueError("Participante presente deve ter todas as 3 notas preenchidas (1 a 5) ou marcar 'Não observado'.")
            else:
                # Se não observado, as notas individuais numéricas não devem ser exigidas
                pass
        return self

class BatchFieldCollection(BaseModel):
    """Lote de coleta rápida de campo do voluntário (< 3 min em regime / < 4 min no piloto)."""
    encontro_id: str
    programa_id: str
    data_encontro: date
    educador_id: str
    tempo_preenchimento_segundos: Optional[int] = Field(None, description="Tempo cronometrado em campo")
    avaliacoes: List[AttendanceScore]

    model_config = ConfigDict(extra="forbid")  # Rejeita campos extras de texto aberto ou mídias

class TherapySessionMetadata(BaseModel):
    """
    Metadados estritamente agregados de vivência terapêutica (FR-020 / US-05 - Zona B).
    Preserva a fronteira bioética (CFP/LGPD): PROIBIDO qualquer identificador individual, nota clínica ou CID.
    """
    realizada: bool = True
    data_sessao: date
    psicologa_id: str
    duracao_minutos: int = Field(..., ge=15, le=240)
    total_presentes_agregado: int = Field(..., ge=0)
    checklist_infra: List[str] = Field(default_factory=list)
    topicos_pedagogicos: Optional[List[str]] = Field(default_factory=list)

    @field_validator("checklist_infra")
    @classmethod
    def validate_infra(cls, items: List[str]):
        for it in items:
            if it not in PSYCHOLOGY_INFRA_CHECKLIST:
                raise ValueError(f"Item de infraestrutura '{it}' inválido.")
        return items

    @field_validator("topicos_pedagogicos")
    @classmethod
    def validate_topics(cls, topics: Optional[List[str]]):
        if topics:
            for t in topics:
                if t not in ALLOWED_THERAPY_TOPICS:
                    raise ValueError(f"Tópico '{t}' não permitido pela taxonomia ética.")
        return topics

    model_config = ConfigDict(extra="forbid")  # Rejeição intransigente de prontuários ou notas clínicas

class RelatorioVersao(BaseModel):
    """Controle de versão e aprovação humana para publicação estática (Zona D - FR-033 a FR-036)."""
    relatorio_id: str
    periodo: str
    versao: str
    status_aprovacao: str = Field("GERADO", pattern=r"^(GERADO|REVISADO_COORDENACAO|APROVADO_DIRETORIA|ARQUIVADO)$")
    aprovador_nome: Optional[str] = None
    data_aprovacao: Optional[datetime] = None
    arquivo_hash: Optional[str] = None
    possui_limitacoes_metodologicas: bool = True
    amostras_suprimidas_menores_10: bool = True

class OptionalFeedbackSubmission(BaseModel):
    """Módulo Opcional E (Fora do MVP / Portão G5) — Fila de Recepção em Quarentena Isolada."""
    feedback_id: str
    participant_id: str = Field(..., pattern=r"^EBZ-\d{3,}$")
    tipo_origem: str = Field(..., pattern=r"^(RESPONSAVEL_FAMILIAR|OFICINEIRO)$")
    tipo_midia: str = Field(..., pattern=r"^(TEXTO|AUDIO)$")
    conteudo_ou_referencia: str
    consentimento_registrado: bool = True
    data_recebimento: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TriageModerationAction(BaseModel):
    """Módulo Opcional E (Fora do MVP / Portão G5) — Ação de Moderação Humana."""
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
