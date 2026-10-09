"""
Gerador de Datasets Sintéticos para o MVP Acadêmico da Plataforma Ebenézer Impacta.
Gera 130 educandos fictícios, matrículas cruzadas, 10 semanas de histórico de encontros,
avaliações socioemocionais (Autonomia, Convivência, Participação) e sessões de vivência.
"""

import json
import random
from datetime import date, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "synthetic"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)

# Nomes fictícios para o cadastro civil restrito (sem qualquer relação com menores reais)
PRIMEIROS_NOMES = [
    "Lucas", "Gabriel", "Mateus", "Enzo", "Guilherme", "Rafael", "Nicolas", "Arthur",
    "Sophia", "Alice", "Julia", "Isabella", "Manuela", "Laura", "Luiza", "Valentina",
    "Pedro", "Thiago", "Bernardo", "Davi", "Samuel", "Heitor", "Lorena", "Beatriz",
    "Mariana", "Lara", "Melissa", "Yasmin", "Cecilia", "Emanuelly", "Agatha", "Helena"
]

SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira",
    "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida", "Lopes",
    "Soares", "Fernandes", "Vieira", "Barbosa", "Rocha", "Dias", "Nascimento", "Andrade"
]

PROGRAMAS = ["PROG-SONHOS", "PROG-REFORCO", "PROG-INFANCIA"]

def generate_synthetic_data(num_students=130, num_weeks=10):
    participantes_mdm = []
    cadastros_civis = []

    # 1. Gerar Participantes (Golden Record + Base Civil Segregada)
    for i in range(1, num_students + 1):
        p_id = f"EBZ-{i:03d}"
        coorte = random.choice([2024, 2025, 2026])
        faixa = random.choice(["PRIMEIRA_INFANCIA", "CRIANCA", "CRIANCA", "ADOLESCENTE"])

        if faixa == "PRIMEIRA_INFANCIA":
            matriculas = ["PROG-INFANCIA"]
        elif faixa == "ADOLESCENTE":
            matriculas = ["PROG-SONHOS"]
            if random.random() < 0.4:
                matriculas.append("PROG-REFORCO")
        else:
            matriculas = ["PROG-REFORCO"]
            if random.random() < 0.6:
                matriculas.append("PROG-SONHOS")

        participantes_mdm.append({
            "participant_id": p_id,
            "coorte_ano": coorte,
            "faixa_etaria": faixa,
            "matriculas_ativas": matriculas,
            "status": "ATIVO"
        })

        cadastros_civis.append({
            "civil_id": f"civ-{i:04d}",
            "participant_id": p_id,
            "nome_completo_crianca": f"{random.choice(PRIMEIROS_NOMES)} {random.choice(SOBRENOMES)} {random.choice(SOBRENOMES)}",
            "data_nascimento": str(date(2026 - (5 if faixa == 'PRIMEIRA_INFANCIA' else (9 if faixa == 'CRIANCA' else 14)), random.randint(1, 12), random.randint(1, 28))),
            "nome_responsavel": f"{random.choice(PRIMEIROS_NOMES)} {random.choice(SOBRENOMES)}",
            "parentesco": random.choice(["MAE", "MAE", "PAI", "AVO", "TUTOR_LEGAL"]),
            "telefone_contato": f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            "endereco_bairro": "Jardim Ângela",
            "termo_consentimento_lgpd": True
        })

    # 2. Gerar Encontros e Avaliações Socioemocionais (10 Sábados)
    encontros = []
    avaliacoes = []
    start_saturday = date(2026, 7, 25)

    for week in range(num_weeks):
        saturday = start_saturday + timedelta(weeks=week)
        for prog in PROGRAMAS:
            encontro_id = f"ENC-{prog}-{saturday.strftime('%Y%m%d')}"
            alunos_prog = [p for p in participantes_mdm if prog in p["matriculas_ativas"]]

            # Status de envio da chamada (maioria em D0)
            is_d0 = random.random() < 0.92
            status_lancamento = "D0_NO_PRAZO" if is_d0 else "ATRASADO"

            encontros.append({
                "encontro_id": encontro_id,
                "programa_id": prog,
                "data_encontro": str(saturday),
                "horario_inicio": "09:00",
                "horario_fim": "11:00",
                "educador_id": f"VOL-{prog[-3:]}-01",
                "data_envio_registro": f"{saturday}T11:45:00" if is_d0 else f"{saturday + timedelta(days=2)}T18:00:00",
                "status_lancamento": status_lancamento
            })

            # Avaliações para cada educando da turma
            for p in alunos_prog:
                presente = random.random() < 0.88  # 88% de frequência média
                if presente:
                    # Trajetória longitudinal de evolução: melhora ligeira ao longo das 10 semanas
                    base_progress = min(4, 2 + int(week * 0.25))
                    score_autonomia = min(5, max(1, random.randint(base_progress, base_progress + 2)))
                    score_convivencia = min(5, max(1, random.randint(base_progress, base_progress + 2)))
                    score_participacao = min(5, max(1, random.randint(base_progress, base_progress + 2)))
                else:
                    score_autonomia = None
                    score_convivencia = None
                    score_participacao = None

                avaliacoes.append({
                    "avaliacao_id": f"AV-{encontro_id}-{p['participant_id']}",
                    "encontro_id": encontro_id,
                    "participant_id": p["participant_id"],
                    "presenca": presente,
                    "score_autonomia": score_autonomia,
                    "score_convivencia": score_convivencia,
                    "score_participacao": score_participacao,
                    "timestamp_registro": f"{saturday}T11:45:00"
                })

    # 3. Gerar Sessões de Vivência Terapêutica (Metadados Agregados - Sigilo CFP)
    vivencias = []
    topicos_disponiveis = [
        "AUTOCUIDADO_E_HIGIENE", "REGULACAO_EMOCIONAL", "CONVIVENCIA_E_VINCULO",
        "RESOLUCAO_PACIFICA_DE_CONFLITOS", "PROJETO_DE_VIDA_E_SONHOS", "ESCUTA_E_EXPRESSAO_DE_SENTIMENTOS"
    ]
    for week in range(num_weeks):
        saturday = start_saturday + timedelta(weeks=week)
        vivencias.append({
            "vivencia_id": f"VIV-{saturday.strftime('%Y%m%d')}",
            "data": str(saturday),
            "psicologa_responsavel": "CRP-06/98765-SP",
            "duracao_minutos": random.choice([60, 90, 120]),
            "total_presentes_agregado": random.randint(18, 26),
            "topicos_pedagogicos": random.sample(topicos_disponiveis, k=random.randint(2, 3))
        })

    # 4. Fila de Triagem Inicial de Feedbacks Opcionais (Quarentena Segregada)
    fila_triagem = [
        {
            "feedback_id": "FB-001",
            "participant_id": "EBZ-012",
            "tipo_origem": "RESPONSAVEL_FAMILIAR",
            "tipo_midia": "TEXTO",
            "conteudo_ou_referencia": "A mãe relatou que a criança começou a organizar seus brinquedos em casa espontaneamente.",
            "consentimento_registrado": True,
            "data_recebimento": "2026-09-12T14:20:00",
            "status_triagem": "APROVEITADO",
            "categoria_fechada": "AUTONOMIA_NO_COTIDIANO",
            "coordenador_aprovador_id": "COORD-MARIA"
        },
        {
            "feedback_id": "FB-002",
            "participant_id": "EBZ-034",
            "tipo_origem": "OFICINEIRO",
            "tipo_midia": "AUDIO",
            "conteudo_ou_referencia": "audio_quarantine_ebz034_w07.wav",
            "consentimento_registrado": True,
            "data_recebimento": "2026-09-19T12:05:00",
            "status_triagem": "RECEBIDO",
            "categoria_fechada": None,
            "coordenador_aprovador_id": None
        },
        {
            "feedback_id": "FB-003",
            "participant_id": "EBZ-089",
            "tipo_origem": "RESPONSAVEL_FAMILIAR",
            "tipo_midia": "TEXTO",
            "conteudo_ou_referencia": "Relato mencionando necessidade urgente de cesta básica e suporte de saúde externa.",
            "consentimento_registrado": True,
            "data_recebimento": "2026-09-26T15:10:00",
            "status_triagem": "PROTOCOLO_EXTERNO",
            "categoria_fechada": None,
            "coordenador_aprovador_id": "COORD-MARIA"
        }
    ]

    # Salvar todos os arquivos sintéticos
    with open(OUTPUT_DIR / "mdm_participantes.json", "w", encoding="utf-8") as f:
        json.dump(participantes_mdm, f, indent=2, ensure_ascii=False)

    with open(OUTPUT_DIR / "cadastro_civil_segregado.json", "w", encoding="utf-8") as f:
        json.dump(cadastros_civis, f, indent=2, ensure_ascii=False)

    with open(OUTPUT_DIR / "encontros_operacionais.json", "w", encoding="utf-8") as f:
        json.dump(encontros, f, indent=2, ensure_ascii=False)

    with open(OUTPUT_DIR / "avaliacoes_socioemocionais.json", "w", encoding="utf-8") as f:
        json.dump(avaliacoes, f, indent=2, ensure_ascii=False)

    with open(OUTPUT_DIR / "vivencias_terapeuticas.json", "w", encoding="utf-8") as f:
        json.dump(vivencias, f, indent=2, ensure_ascii=False)

    with open(OUTPUT_DIR / "fila_triagem_feedbacks.json", "w", encoding="utf-8") as f:
        json.dump(fila_triagem, f, indent=2, ensure_ascii=False)

    print(f"Sucesso: {len(participantes_mdm)} participantes gerados.")
    print(f"Sucesso: {len(encontros)} encontros e {len(avaliacoes)} avaliações geradas.")
    print(f"Sucesso: {len(vivencias)} sessões de vivência geradas.")

if __name__ == "__main__":
    generate_synthetic_data()
