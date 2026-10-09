# Implementation Tasks: Ebenézer Impacta (v2.0)

**Feature**: `001-ebenezer-impacta` | **PRD Reference**: PRD v2.0 (revisado)  
**Date**: 2026-10-09  
**Plan**: [plan.md](file:///c:/Users/serra/OneDrive/%C3%81rea%20de%20Trabalho/0%20-%20amanava/G9%20-%20Instituto%20Eben%C3%A9zer/specs/001-ebenezer-impacta/plan.md)  
**Spec**: [spec.md](file:///c:/Users/serra/OneDrive/%C3%81rea%20de%20Trabalho/0%20-%20amanava/G9%20-%20Instituto%20Eben%C3%A9zer/specs/001-ebenezer-impacta/spec.md)

---

## Estrutura de Entrega Orientada a Portões de Decisão (Decision Gates)

```
[Portão G0: Fundação] ──► [Portão G1: Piloto Sintético] ──► [Portão G2: Piloto Real] ──► [Portão G3: Expansão] ──► [Portão G4: Publicação] ──► [Portão G5: Módulo E]
```

---

## Portão G0: Fundação Técnica e Metodológica (Semana 11)

**Objetivo**: Estabelecer a arquitetura de dados com custo zero de licença sob o Google Workspace for Nonprofits / AppSheet, registrar ADRs, definir esquemas tabulares por zonas físicas e elaborar rubricas iniciais.

- [X] **T001 [G0]** Registrar formalmente as Decisões Arquiteturais **ADR-001 a ADR-006** (Google Sheets, AppSheet, Looker Interno, PDF Estático, Exclusão de Áudio no MVP, Scripts de Agregação).
- [X] **T002 [G0]** Mapear as 5 Zonas de Sensibilidade Físicas (A: Restrita, B: Operacional, C: Analítica, D: Publicada, E: Quarentena) no arquivo `data/schemas/dictionary.json`.
- [X] **T003 [G0]** [P] Definir parâmetros constitucionais de supressão ($n < 10$), metas de tempo (< 4 min piloto / < 3 min regime) e constantes éticas em `src/core/config.py`.
- [X] **T004 [G0]** [P] Implementar modelos Pydantic com validação estrita de fronteira clínica (CFP/LGPD), suporte a "Não observado" e bloqueio de campos livres em `src/core/models.py`.
- [X] **T005 [G0]** Documentar as rubricas v0 dos 3 indicadores observáveis (Autonomia, Convivência em Grupo e Participação Ativa) e escalas fechadas em `specs/001-ebenezer-impacta/contracts/field_collection.md`.

---

## Portão G1: Piloto Sintético e Simulação de Campo (Semana 12)

**Objetivo**: Validar todo o fluxo técnico e a experiência do usuário com 100% de dados sintéticos (120+ crianças, 4 programas, 10 semanas simuladas), sem expor qualquer dado real.

- [X] **T006 [G1]** Gerar base 100% sintética aderente às Zonas A e B em `data/synthetic/generate_data.py`.
- [X] **T007 [G1]** [P] Implementar serviço mestre de participantes (MDM) com ID pseudonimizado (`EBZ-###`) e isolamento civil em `src/core/mdm.py`.
- [X] **T008 [G1]** [P] Implementar serviço de coleta de campo com escalas fechadas e medição de telemetria em `src/services/collection_service.py`.
- [X] **T009 [G1]** Implementar interface mobile-first do voluntário com suporte offline nativo em `src/templates/campo_voluntario.html` e rotas em `src/api/routes_volunteer.py`.
- [X] **T010 [G1]** Implementar painel D0 da coordenação para identificação de pendências em < 1 minuto em `src/templates/coordenacao_d0.html` e `src/services/coordination_service.py`.
- [X] **T011 [G1]** Implementar módulo restrito da psicologia com metadados agregados e checklist de infraestrutura em `src/templates/vivencia_psicologia.html` e `src/services/therapy_service.py`.
- [X] **T012 [G1]** [P] Criar bateria de testes automatizados com pytest (`test_field_collection.py`, `test_coordination_d0.py`, `test_therapy_privacy.py`, `test_e2e_flow.py`).

---

## Portão G2: Piloto Real Controlado (Semanas 13 a 17)

**Objetivo**: Habilitar comitê de ética e validação jurídica (LGPD/ECA) antes de qualquer coleta de dados de crianças reais em 1 turma piloto (15–20 crianças no Laboratório de Sonhos).

- [ ] **T013 [G2]** Elaborar parecer preliminar de privacidade e minuta de termo de consentimento/informação aos responsáveis legais.
- [ ] **T014 [G2]** Formalizar política de retenção e cronograma de descarte de registros para as Zonas A e B.
- [ ] **T015 [G2]** Realizar teste de penetração/vazamento verificando que voluntários não têm acesso à Zona A sob nenhuma circunstância.
- [ ] **T016 [G2]** Conduzir workshop prático de 30 minutos com voluntários da turma piloto e entrega do runbook de contingência (lista de papel para casos de falha).
- [ ] **T017 [G2]** Cronometrar em campo a rotina semanal da coordenação (meta: <= 1 hora/semana) para validar a Hipótese H-06.

---

## Portão G3: Expansão Programática (Semanas 19 a 22)

**Objetivo**: Expandir a coleta para as demais oficinas (Reforço Escolar, Primeira Infância e Vivências) após confirmação dos indicadores de adoção do piloto.

- [ ] **T018 [G3]** Avaliar métricas do piloto (taxa de registro D0 > 80%, tempo por turma < 4 min, CSAT > 4,0/5).
- [ ] **T019 [G3]** Realizar sessão de calibração entre avaliadores das rubricas dos 3 indicadores para assegurar consistência da série longitudinal.
- [ ] **T020 [G3]** Expandir o onboarding para o conjunto dos 12 voluntários das 4 oficinas ativas.

---

## Portão G4: Publicação e Prestação de Contas Externa (Semana 23 / D+90)

**Objetivo**: Gerar artefatos analíticos agregados e relatórios de prestação de contas com revisão e aprovação humana registrada, sem links vivos à base.

- [X] **T021 [G4]** [P] Implementar no motor de métricas (`src/core/metrics.py`) a regra mandatória de **supressão de pequenas células ($n < 10$)** para mitigar riscos de reidentificação.
- [X] **T022 [G4]** [P] Inserir seção obrigatória de **Limitações Metodológicas** ("O que este relatório não afirma") e expurgar do código afirmações monetárias/fiscais desprovidas de base (rejeitar R$ 16k/ano, conformidade automática Rouanet).
- [X] **T023 [G4]** Implementar fluxo formal de aprovação (`GERADO` → `REVISADO_COORDENACAO` → `APROVADO_DIRETORIA` → `ARQUIVADO`) na emissão do relatório estático em `src/templates/relatorios_captacao.html`.
- [X] **T024 [G4]** Validar rotina de exportação completa em formato aberto (CSV) garantindo o princípio de Saída Possível (portabilidade).

---

## Portão G5: Módulo Opcional E — Escuta de Famílias e Voz (Pós-MVP)

**Objetivo**: Canal opcional condicionado a parecer jurídico independente, teste de segurança, orçamento específico para custos de mídia/transcrição e equipe capacitada de triagem.

- [X] **T025 [G5]** Isolar componentes de quarentena e fila de triagem de áudio/texto fora do fluxo padrão do MVP (`src/templates/triagem_escuta.html` e `src/services/triage_service.py`), sinalizando o status "Fora do MVP / Portão G5".
- [ ] **T026 [G5]** Elaborar estudo de impacto à proteção de dados (RIPD) específico para coleta de manifestações por voz de responsáveis.
- [ ] **T027 [G5]** Dimensionar orçamento dedicado para eventuais custos de transcrição e armazenamento criptografado de mídias.
