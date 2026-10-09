"""
Teste de Integração Ponta a Ponta (E2E) da Plataforma Ebenézer Impacta.
Percorre a jornada de todas as personas do PRD invocando os serviços e rotas integradas:
1. Voluntário de Sábado (Chamada < 3 min com 3 indicadores).
2. Coordenadora Geral (Painel D0 & MDM Golden Record).
3. Psicóloga Institucional (Metadados agregados CFP).
4. Captador / Investidor ESG (Dossiê Lei Rouanet & Donor Success).
5. Família / Responsável (Canal opcional em quarentena).
6. Coordenadora em Triagem (Moderação humana e encaminhamento).
"""

from datetime import date
from src.core.models import (
    BatchFieldCollection,
    AttendanceScore,
    TherapySessionMetadata,
    OptionalFeedbackSubmission,
    TriageModerationAction
)
from src.api.routes_volunteer import get_class_roster, submit_attendance
from src.api.routes_coordination import get_d0_dashboard, get_mdm_summary, notify_educator
from src.api.routes_therapy import get_sessions, record_session
from src.api.routes_reports import get_longitudinal_curves, get_fiscal_dossier, get_donor_success, export_csv
from src.api.routes_triage import get_triage_queue, submit_optional_feedback, moderate_feedback

def test_e2e_complete_flow():
    # 1. Voluntário de Campo: Carregar turma e submeter chamada
    roster = get_class_roster(programa_id="PROG-SONHOS")
    assert len(roster) > 0
    assert "participant_id" in roster[0]

    batch = BatchFieldCollection(
        encontro_id="ENC-E2E-TEST",
        programa_id="PROG-SONHOS",
        data_encontro=date(2026, 10, 3),
        educador_id="VOL-SABADO-01",
        tempo_preenchimento_segundos=115,  # 1m 55s (< 180s)
        avaliacoes=[
            AttendanceScore(
                participant_id=s["participant_id"],
                presenca=True,
                score_autonomia=4,
                score_convivencia=5,
                score_participacao=4
            )
            for s in roster[:15]
        ]
    )
    res_vol = submit_attendance(batch)
    assert res_vol["status"] == "sucesso"
    assert res_vol["dentro_da_meta_3min"] is True
    assert res_vol["total_alunos_avaliados"] == 15

    # 2. Coordenação Geral: Painel D0 e Golden Record
    d0_data = get_d0_dashboard()
    assert "taxa_conformidade_d0_percentual" in d0_data
    assert d0_data["total_oficinas_dia"] > 0

    reminder_res = notify_educator("ENC-E2E-TEST")
    assert reminder_res["status"] == "notificado"

    mdm_data = get_mdm_summary()
    assert mdm_data["total_educandos_ativos"] >= 120

    # 3. Psicologia: Submeter sessão com metadados agregados (CFP)
    therapy_meta = TherapySessionMetadata(
        data_sessao=date(2026, 10, 3),
        psicologa_id="CRP-06/98765-SP",
        duracao_minutos=90,
        total_presentes_agregado=21,
        topicos_pedagogicos=["AUTOCUIDADO_E_HIGIENE", "REGULACAO_EMOCIONAL"]
    )
    res_psic = record_session(therapy_meta)
    assert res_psic["status"] == "sucesso"
    assert res_psic["total_presentes_agregado"] == 21

    sessions = get_sessions()
    assert len(sessions) > 0

    # 4. Captação & Transparência: Curvas Longitudinais, Dossiê Fiscal e Donor Success
    curves = get_longitudinal_curves(programa_id="PROG-SONHOS")
    assert len(curves["autonomia"]) > 0
    assert len(curves["convivencia"]) > 0
    assert len(curves["participacao"]) > 0

    fiscal = get_fiscal_dossier()
    assert fiscal["total_carga_horaria_horas"] > 0
    assert fiscal["taxa_permanencia_media_percentual"] > 50

    donor = get_donor_success("PROG-SONHOS")
    assert "destaques" in donor
    assert donor["evolucao_pontos_percentuais"] > 0

    csv_res = export_csv()
    assert csv_res.media_type == "text/csv"

    # 5. Família / Responsável: Enviar relato opcional para quarentena
    fb_sub = OptionalFeedbackSubmission(
        feedback_id="FB-E2E-001",
        participant_id="EBZ-026",
        tipo_origem="RESPONSAVEL_FAMILIAR",
        tipo_midia="TEXTO",
        conteudo_ou_referencia="A criança demonstra muito entusiasmo aos sábados.",
        consentimento_registrado=True
    )
    res_fb = submit_optional_feedback(fb_sub)
    assert res_fb["status"] == "recebido"
    assert res_fb["status_triagem"] == "RECEBIDO"

    # 6. Coordenação em Triagem: Moderar relato
    triage_queue = get_triage_queue()
    assert len(triage_queue) > 0

    mod_action = TriageModerationAction(
        feedback_id="FB-E2E-001",
        coordenador_id="COORD-MARIA",
        decisao="APROVEITADO_CATEGORIA_PEDAGOGICA",
        categoria_fechada="ENGAJAMENTO_FAMILIAR_POSITIVO"
    )
    res_mod = moderate_feedback(mod_action)
    assert res_mod["status"] == "moderado"
    assert res_mod["decisao"] == "APROVEITADO_CATEGORIA_PEDAGOGICA"
