# Implementation Plan: Ebenézer Impacta

**Branch**: `001-ebenezer-impacta` | **Date**: 2026-10-05 | **Spec**: [spec.md](file:///c:/Users/serra/OneDrive/%C3%81rea%20de%20Trabalho/0%20-%20amanava/G9%20-%20Instituto%20Eben%C3%A9zer/specs/001-ebenezer-impacta/spec.md)

**Input**: Feature specification from `/specs/001-ebenezer-impacta/spec.md`

## Summary

O projeto **Ebenézer Impacta** é uma plataforma de governança e monitoramento socioemocional para o Instituto Social Ebenézer no Jardim Ângela (SP). A solução implementa um modelo de dados unificado (MDM) pseudonimizado (Golden Record), aplicativo de campo mobile-first com coleta de chamada e 3 indicadores socioemocionais em menos de 3 minutos, módulo blindado da vivência terapêutica restrito a metadados, painel gerencial de pendências em D0 para a coordenação (<= 1h/sem), gerador automatizado de Relatório de Transparência e Captação (Lei Rouanet/Lucro Real e Donor Success de 2 páginas), além de canal segregado de triagem com moderação humana para feedbacks opcionais de responsáveis e oficineiros.
Toda a arquitetura é fundamentada em custo zero de licenças (Google Workspace for Nonprofits, AppSheet e Looker Studio) e suportada por um protótipo de demonstração acadêmica 100% autônomo com dados sintéticos.

## Technical Context

**Language/Version**: Python 3.10+ (scripts de geração sintética, validação contratual e backend leve de demonstração) / HTML5 + Vanilla JS + Tailwind CSS (protótipo mobile-first e dashboard).

**Primary Dependencies**: FastAPI / Uvicorn (API local de prototipagem), Pydantic (validação rigorosa de esquemas e contratos), Pandas (geração e agregação estatística de coortes).

**Storage**: Arquivos CSV/JSON com esquemas compatíveis com Google Sheets / AppSheet e armazenamento de sessão seguro em quarentena local.

**Testing**: Pytest (testes de validação de esquemas, restrições bioéticas do CFP/LGPD, assertividade de anonimização e cálculo de indicadores).

**Target Platform**: Web responsivo (Mobile-First para telas de smartphone dos voluntários e Desktop/Tablet para Coordenação e Diretoria).

**Project Type**: Web Application + Data Infrastructure Toolkit (gerador de bases para Google Sheets + protótipo operacional completo).

**Performance Goals**:
- Ciclo de preenchimento de chamada e 3 indicadores de 15 alunos < 180 segundos (<3 minutos).
- Tempo de consolidação e emissão do Relatório Anual < 24 horas.
- Saneamento semanal da coordenação <= 1 hora.

**Constraints**:
- Custo de licença direto garantido de R$ 0,00.
- Blindagem total: proibição de prontuários clínicos e dados abertos sensíveis.
- Segregação estrita entre base civil e base analítica de indicadores.
- Modo de demonstração acadêmica operando com 100% de dados sintéticos.

**Scale/Scope**:
- 120+ crianças atendidas, 4 programas centrais, turmas de até 15-20 alunos, 10 semanas de histórico no piloto.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Princípio Constitucional | Status | Mecanismo de Conformidade no Design |
|--------------------------|--------|-------------------------------------|
| **I. Blindagem Ética, Privacidade e Não Estigmatização** | PASS | Dados civis fisicamente apartados; ID alfanumérico único (`EBZ-xxx`); formulários de campo restritos a escalas fechadas de 1 a 5; módulo da psicóloga coleta exclusivamente metadados agregados. |
| **II. Custo de Licença Zero e Sustentabilidade** | PASS | Especificações e estruturas projetadas para Google Workspace for Nonprofits e AppSheet Free/Core; protótipo autônomo sem dependência de serviços pagos. |
| **III. Interface Mobile-First de Baixo Atrito (< 3 min)** | PASS | Interface operacional simplificada com botões grandes, cards rápidos, sem digitação de texto; suporte a cache offline com flush automático. |
| **IV. Evidências Auditáveis e Captação** | PASS | Geração automatizada de curvas evolutivas por coorte, dossiê com carimbo temporal para Lei Rouanet/Lucro Real e relatório executivo "Donor Success" de 2 páginas. |
| **V. Governança Segregada, Triagem e Dados Sintéticos** | PASS | Fila de triagem privada com estados controlados; isolamento de mídias de áudio/texto fora do Looker Studio; 100% dados sintéticos no ambiente de demonstração acadêmico. |

## Project Structure

### Documentation (this feature)

```text
specs/001-ebenezer-impacta/
├── plan.md              # Este plano de implementação
├── research.md          # Decisões técnicas e arquiteturais (Phase 0)
├── data-model.md        # Esquema de dados das 8 entidades centrais (Phase 1)
├── quickstart.md        # Guia de execução e cenários de validação (Phase 1)
├── contracts/           # Contratos formais das interfaces operacionais (Phase 1)
│   ├── field_collection.md
│   ├── therapy_session.md
│   └── triage_workflow.md
├── checklists/
│   └── requirements.md  # Checklist de qualidade de requisitos
└── tasks.md             # Tarefas ordenadas de implementação (Phase 2)
```

### Source Code (repository root)

```text
data/
├── schemas/             # Dicionário de dados e esquemas para Google Sheets / AppSheet
└── synthetic/           # Datasets sintéticos gerados para o MVP acadêmico (120+ educandos)

src/
├── app.py               # Servidor do protótipo integrado (FastAPI)
├── core/
│   ├── config.py        # Configurações do projeto e flags de ambiente
│   ├── models.py        # Modelos de dados e validações Pydantic
│   ├── mdm.py           # Lógica do Golden Record e segregação civil
│   └── metrics.py       # Motor de cálculo de curvas longitudinais e dossiê fiscal
├── static/              # Estilos e scripts client-side (com suporte offline/IndexedDB)
└── templates/           # Interfaces responsivas:
    ├── base.html
    ├── campo_voluntario.html   # Interface Mobile-First (<3 min)
    ├── vivencia_psicologia.html # Módulo operacional blindado da psicóloga
    ├── coordenacao_d0.html     # Painel de pendências e rituais semanais
    ├── triagem_escuta.html     # Fila de moderação de áudio/texto
    └── relatorios_captacao.html# Emissão de transparência, Rouanet e Donor Success

tests/
├── test_contracts.py    # Validação dos contratos de API e JSON schemas
├── test_ethics_gates.py # Testes de não vazamento de dados civis e ausência de prontuários
└── test_longitudinal.py # Validação matemática das curvas de evolução socioemocional
```

**Structure Decision**: Web application com stack Python/FastAPI e front-end mobile-first leve, associada a scripts de engenharia de dados e esquemas tabulares exportáveis para Google Sheets / AppSheet. Esta estrutura permite ao mesmo tempo a entrega dos requisitos operacionais no Google Workspace e a demonstração acadêmica interativa imediata no computador de qualquer avaliador.

## Complexity Tracking

Nenhuma violação constitucional identificada. Arquitetura mantida estritamente dentro dos limites de custo zero, simplicidade e privacidade por design.
