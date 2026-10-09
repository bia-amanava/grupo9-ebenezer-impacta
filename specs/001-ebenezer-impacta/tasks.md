# Implementation Tasks: Ebenézer Impacta

**Feature**: `001-ebenezer-impacta`
**Date**: 2026-10-05
**Plan**: [plan.md](file:///c:/Users/serra/OneDrive/%C3%81rea%20de%20Trabalho/0%20-%20amanava/G9%20-%20Instituto%20Eben%C3%A9zer/specs/001-ebenezer-impacta/plan.md)
**Spec**: [spec.md](file:///c:/Users/serra/OneDrive/%C3%81rea%20de%20Trabalho/0%20-%20amanava/G9%20-%20Instituto%20Eben%C3%A9zer/specs/001-ebenezer-impacta/spec.md)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, directory structure and shared dependencies.

- [X] T001 Create project directories for schemas, synthetic data, services, templates and tests in `src/` and `data/`
- [X] T002 Initialize project dependencies in `requirements.txt` with FastAPI, Uvicorn, Pydantic, Pandas and Jinja2
- [X] T003 [P] Configure environment settings and constants in `src/core/config.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data schemas, domain entities and synthetic data generation required by all user stories.

- [X] T004 Setup Google Sheets / AppSheet relational schema definitions and data dictionary in `data/schemas/dictionary.json`
- [X] T005 [P] Implement core Pydantic data models for participants, attendance, sessions and triage in `src/core/models.py`
- [X] T006 [P] Implement MDM service managing Golden Record pseudonimization (EBZ-xxx) and civil data segregation in `src/core/mdm.py`
- [X] T007 Implement synthetic data generator producing 120+ students, 4 programs, classes and 10 weeks of historical records in `data/synthetic/generate_data.py`
- [X] T008 [P] Configure base responsive HTML template with mobile viewport and Tailwind CSS in `src/templates/base.html`

---

## Phase 3: User Story 1 - Coleta de Chamada e Avaliação Mobile em Campo (<3 min) (Priority: P1) 🎯 MVP

**Goal**: Permitir que voluntários em campo realizem chamada e pontuem 3 indicadores socioemocionais (Autonomia, Convivência, Participação) de até 15 alunos em < 3 minutos via celular com suporte offline.

**Independent Test**: Simular envio de lote de 15 alunos com medição de tempo < 180s e assertividade de gravação.

### Tests for User Story 1
- [X] T009 [P] [US1] Create automated contract and benchmark test for 15-student batch collection and <180s telemetry in `tests/test_field_collection.py`

### Implementation for User Story 1
- [X] T010 [P] [US1] Implement attendance and socioemotional evaluation service in `src/services/collection_service.py`
- [X] T011 [US1] Implement mobile-first volunteer collection interface with offline LocalStorage support in `src/templates/campo_voluntario.html`
- [X] T012 [US1] Implement API endpoints for volunteer class loading and batch attendance submission in `src/api/routes_volunteer.py`

---

## Phase 4: User Story 2 - Cadastro Mestre (MDM) e Painel de Saneamento D0 da Coordenação (Priority: P2)

**Goal**: Fornecer painel em tempo real para a coordenação identificar turmas faltantes em D0 com 1 clique e manter o Golden Record unificado entre programas.

**Independent Test**: Verificar se turmas sem envio no sábado são listadas no painel com ação de cobrança em 1 clique e se duplicidades de cadastro são impedidas.

### Tests for User Story 2
- [X] T013 [P] [US2] Create test for MDM multi-program deduplication and D0 pending detection in `tests/test_coordination_d0.py`

### Implementation for User Story 2
- [X] T014 [P] [US2] Implement coordination monitoring service for D0 pending sessions and weekly reconciliation in `src/services/coordination_service.py`
- [X] T015 [US2] Implement coordination D0 dashboard and MDM registry view in `src/templates/coordenacao_d0.html`
- [X] T016 [US2] Implement API endpoints for coordination dashboard and MDM reconciliation in `src/api/routes_coordination.py`

---

## Phase 5: User Story 3 - Módulo Operacional Blindado da Vivência Terapêutica (Priority: P3)

**Goal**: Garantir interface exclusiva para a psicóloga registrar apenas metadados agregados de sessões (duração, participantes presentes, temas), bloqueando prontuários e diagnósticos individuais.

**Independent Test**: Submeter registro com metadados e verificar rejeição programática de campos nominais ou notas clínicas.

### Tests for User Story 3
- [X] T017 [P] [US3] Create test for clinical privacy gate asserting rejection of clinical notes and acceptance of aggregated metadata in `tests/test_therapy_privacy.py`

### Implementation for User Story 3
- [X] T018 [P] [US3] Implement therapy session service validating CFP/LGPD metadata rules in `src/services/therapy_service.py`
- [X] T019 [US3] Implement restricted psychology session logging interface in `src/templates/vivencia_psicologia.html`
- [X] T020 [US3] Implement API endpoint for therapy session submission in `src/api/routes_therapy.py`

---

## Phase 6: User Story 4 - Emissão de Relatórios de Transparência, Captação e Dossiês Fiscais (Priority: P4)

**Goal**: Gerar em 1 clique curvas longitudinais por coorte, caderno de evidências para Lei Rouanet / Lucro Real e relatório de 2 páginas ("Impacto do Seu Investimento" / Donor Success).

**Independent Test**: Executar motor de cálculo sobre 10 semanas de histórico e validar emissão das curvas e demonstrativos em PDF/HTML.

### Tests for User Story 4
- [X] T021 [P] [US4] Create test for longitudinal curve calculations and fiscal evidence metrics in `tests/test_reports_metrics.py`

### Implementation for User Story 4
- [X] T022 [P] [US4] Implement metrics and reporting engine in `src/core/metrics.py`
- [X] T023 [US4] Implement interactive reporting interface with charts, Rouanet/Lucro Real dossier and Donor Success 2-page print in `src/templates/relatorios_captacao.html`
- [X] T024 [US4] Implement API endpoints for report data export in `src/api/routes_reports.py`

---

## Phase 7: User Story 5 - Canais Opcionais Segregados de Escuta e Fila de Triagem Humana (Priority: P5)

**Goal**: Oferecer canal de escuta para famílias e educadores com fila privada de triagem da coordenação, impedindo exposição de dados sensíveis e garantindo encaminhamento institucional externo quando necessário.

**Independent Test**: Submeter mensagem de teste, verificar status `RECEBIDO` e testar transições para `APROVEITADO`, `DESCARTADO` e `PROTOCOLO_EXTERNO`.

### Tests for User Story 5
- [X] T025 [P] [US5] Create test for feedback triage state machine and quarantine isolation in `tests/test_triage_quarantine.py`

### Implementation for User Story 5
- [X] T026 [P] [US5] Implement isolated triage and pedagogical synthesis service in `src/services/triage_service.py`
- [X] T027 [US5] Implement private coordination triage interface and feedback submission form in `src/templates/triagem_escuta.html`
- [X] T028 [US5] Implement API endpoints for optional feedback submission and moderation actions in `src/api/routes_triage.py`

---

## Phase 8: Polish, Integration & System Assembly

**Purpose**: Montagem final da aplicação integrada, testes ponta a ponta e documentação executável.

- [X] T029 Assemble FastAPI main application integrating all routes and static assets in `src/app.py`
- [X] T030 [P] Create full end-to-end integration test running through all personas in `tests/test_e2e_flow.py`
- [X] T031 [P] Create standalone launcher script and execution guide in `README.md`

---

## Dependencies & Execution Order

- **Phase 1 (Setup)**: Concluída com sucesso.
- **Phase 2 (Foundational)**: Concluída com sucesso.
- **Phase 3 (US1 - MVP)**: Concluída e testada.
- **Phase 4 (US2)**: Concluída e testada.
- **Phase 5 (US3)**: Concluída e testada.
- **Phase 6 (US4)**: Concluída e testada.
- **Phase 7 (US5)**: Concluída e testada.
- **Phase 8 (Polish & Assembly)**: Concluída com 100% de cobertura nos testes E2E.
