"""
Configurações globais, zonas de sensibilidade e limites de conformidade ética (PRD v2.0).
Plataforma Ebenézer Impacta.
"""

from pathlib import Path

# Caminhos base
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
SCHEMAS_DIR = DATA_DIR / "schemas"
SYNTHETIC_DIR = DATA_DIR / "synthetic"
QUARANTINE_DIR = DATA_DIR / "quarantine"

# Garantir existência de diretórios
for path in [DATA_DIR, SCHEMAS_DIR, SYNTHETIC_DIR, QUARANTINE_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Parâmetros Constitucionais e Metas Operacionais (PRD v2.0)
MAX_COLLECTION_TIME_SECONDS = 180       # Meta de regime: < 3 minutos (<180s)
PILOT_MAX_COLLECTION_TIME_SECONDS = 240 # Meta de piloto: < 4 minutos (<240s)
MAX_STUDENTS_PER_CLASS = 20
MIN_INDICATOR_SCORE = 1
MAX_INDICATOR_SCORE = 5

# Regra Mandatória de Supressão para Salvaguarda de Privacidade (FR-034 / Seção 8.2)
# Não exibir agregações com amostras inferiores a este limite para mitigar reidentificação
SUPPRESSION_MIN_N = 10

# Programas Institucionais do Instituto Social Ebenézer
PROGRAMS = [
    {
        "id": "PROG-SONHOS",
        "nome": "Laboratório de Sonhos",
        "dia": "Sábado",
        "carga_horaria_minutos": 120,
        "eixo": "Socioemocional, Criatividade e Projeto de Vida"
    },
    {
        "id": "PROG-REFORCO",
        "nome": "Reforço Escolar",
        "dia": "Sábado",
        "carga_horaria_minutos": 90,
        "eixo": "Alfabetização e Raciocínio Lógico"
    },
    {
        "id": "PROG-INFANCIA",
        "nome": "Primeira Infância",
        "dia": "Sábado",
        "carga_horaria_minutos": 90,
        "eixo": "Desenvolvimento Motor e Vínculos Afetivos"
    },
    {
        "id": "PROG-VIVENCIAS",
        "nome": "Vivências Terapêuticas",
        "dia": "Sábado",
        "carga_horaria_minutos": 60,
        "eixo": "Suporte Psicossocial em Grupo (Restrito CFP - Somente Metadados)"
    }
]

# Checklist de Infraestrutura para Módulo de Vivência Terapêutica (FR-020 / US-05)
PSYCHOLOGY_INFRA_CHECKLIST = [
    "SALA_COM_PRIVACIDADE_ACUSTICA",
    "MATERIAIS_LUDICOS_E_EXPRESSIVOS",
    "VENTILACAO_E_AGUA_POTAVEL",
    "DISPOSICAO_EM_RODA_ADEQUADA"
]

# Tópicos Socioeducativos Fechados para Módulo de Psicologia (Opcional - Taxonomia Estrita)
ALLOWED_THERAPY_TOPICS = [
    "AUTOCUIDADO_E_HIGIENE",
    "REGULACAO_EMOCIONAL",
    "CONVIVENCIA_E_VINCULO",
    "RESOLUCAO_PACIFICA_DE_CONFLITOS",
    "PROJETO_DE_VIDA_E_SONHOS",
    "ESCUTA_E_EXPRESSAO_DE_SENTIMENTOS"
]

# Estados de Aprovação de Relatórios (Zona D - FR-035)
REPORT_APPROVAL_STATUSES = [
    "GERADO",
    "REVISADO_COORDENACAO",
    "APROVADO_DIRETORIA",
    "ARQUIVADO"
]

# Estados da Fila de Triagem (Módulo Opcional E - Fora do MVP / Portão G5)
TRIAGE_STATUSES = [
    "RECEBIDO",
    "EM_TRIAGEM",
    "APROVEITADO",
    "DESCARTADO",
    "PROTOCOLO_EXTERNO"
]
