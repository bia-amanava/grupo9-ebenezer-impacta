"""
Configurações globais e limites de conformidade ética da plataforma Ebenézer Impacta.
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

# Parâmetros e Limiares Constitucionais
MAX_COLLECTION_TIME_SECONDS = 180  # Meta de 3 minutos (<180s)
MAX_STUDENTS_PER_CLASS = 20
MIN_INDICATOR_SCORE = 1
MAX_INDICATOR_SCORE = 5

# Programas Institucionais
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
        "eixo": "Suporte Psicossocial em Grupo (Restrito CFP)"
    }
]

# Tópicos Permitidos no Módulo de Psicologia (Taxonomia Fechada)
ALLOWED_THERAPY_TOPICS = [
    "AUTOCUIDADO_E_HIGIENE",
    "REGULACAO_EMOCIONAL",
    "CONVIVENCIA_E_VINCULO",
    "RESOLUCAO_PACIFICA_DE_CONFLITOS",
    "PROJETO_DE_VIDA_E_SONHOS",
    "ESCUTA_E_EXPRESSAO_DE_SENTIMENTOS"
]

# Estados da Fila de Triagem
TRIAGE_STATUSES = [
    "RECEBIDO",
    "EM_TRIAGEM",
    "APROVEITADO",
    "DESCARTADO",
    "PROTOCOLO_EXTERNO"
]
