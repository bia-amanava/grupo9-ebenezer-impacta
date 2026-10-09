# Implementation Plan: Ebenézer Impacta (v2.0)

**Feature**: `001-ebenezer-impacta` | **PRD Reference**: PRD v2.0 (revisado)  
**Date**: 2026-10-09 | **Spec**: [spec.md](file:///c:/Users/serra/OneDrive/%C3%81rea%20de%20Trabalho/0%20-%20amanava/G9%20-%20Instituto%20Eben%C3%A9zer/specs/001-ebenezer-impacta/spec.md)

---

## 1. Sumário Executivo da Solução

O **Ebenézer Impacta** é uma solução de governança pedagógica e consolidação analítica para o Instituto Social Ebenézer (Jardim Ângela, SP). O produto viabiliza o acompanhamento sistemático de trajetórias formativas e a prestação de contas periódica através de:
- Identificador pseudonimizado único (`EBZ-###`) com isolamento físico de dados civis;
- Coleta rápida mobile-first em campo (< 4 min no piloto, < 3 min em regime) com suporte offline nativo e 0 campos de texto livre no fluxo do voluntário;
- Módulo da psicologia estritamente restrito a metadados agregados e checklist de infraestrutura, preservando o sigilo do CFP;
- Painel D0 para saneamento ágil pela coordenação em rotina planejada para <= 1 h/semana;
- Camada analítica agregada com supressão mandatória de grupos pequenos ($n < 10$);
- Emissão de relatórios estáticos em PDF revisados e aprovados por humanos antes de qualquer difusão externa;
- Módulo Opcional E (escuta de famílias e observações por voz) expressamente isolado fora do MVP, condicionado ao Portão G5.

---

## 2. Princípios e Zonas de Sensibilidade

### 2.1 Zonas Físicas de Dados
Como em ferramentas de planilhas/arquivos a concessão de acesso expõe todo o arquivo, a separação deve ser física entre repositórios:

```
[Voluntário - AppSheet]  ---> [Zona B: Operacional Pseudonimizada]
[Psicóloga - Restrito]   ---> [Zona B: Metadados Vivência (Sem ID de Criança)]
[Coordenação - MFA]      ---> [Zona A: Dados Civis Restritos] (Acesso Mínimo)
             
[Zona B] ---> (Rotina de Agregação + Supressão n<10) ---> [Zona C: Analítica Agregada]
                                                               |
                                                  [Looker Studio Interno]
                                                               |
                                                  [Relatório Piloto PDF]
                                                               |
                                                   (Aprovação Humana)
                                                               |
                                                  [Zona D: Publicação Estática]
```

- **Zona A (Restrita)**: Nome civil, responsáveis, endereço e contatos. Arquivo isolado com MFA, restrito à coordenação designada.
- **Zona B (Operacional)**: IDs pseudonimizados (`EBZ-###`), presenças binárias, 3 indicadores em escalas fechadas (1 a 5) e metadados de sessões.
- **Zona C (Analítica)**: Indicadores agregados por turma, programa e ciclo, com aplicação automática de supressão para $n < 10$.
- **Zona D (Publicada)**: Arquivos estáticos imutáveis (PDFs) devidamente aprovados por humanos, acompanhados de carimbo de versão e limitações metodológicas.
- **Zona E (Opcional - Quarentena)**: Mensagens de texto/áudio e histórico de triagem (fora do MVP, após G5).

---

## 3. Decisões Arquiteturais Registradas (ADR-lite)

| ADR | Decisão | Alternativas Avaliadas | Justificativa e Trade-offs | Gatilhos de Migração Futura |
|---|---|---|---|---|
| **ADR-001** | Google Sheets como repositório base no MVP | Banco relacional gerenciado (Cloud SQL, Supabase), AppSheet Database | Custo de licença direto R$ 0 no ecossistema sem fins lucrativos e familiaridade da equipe. Trade-off: menor robustez em concorrência. | Migrar para banco gerenciado se: volume > 50.000 linhas, conflitos frequentes de escrita ou exigência de controle por coluna. |
| **ADR-002** | AppSheet como interface mobile de campo | Google Forms, Progressive Web App próprio | Rápida implementação mobile-first, suporte offline nativo e controle granular de telas por perfil. | Migrar para PWA caso haja limitação de usuários no plano sem fins lucrativos. |
| **ADR-003** | Looker Studio exclusivamente interno lendo Zona C | Painel web customizado ou Dashboard público vivo | Evita vazamento acidental de dados operacionais e reidentificação de crianças. O Looker lê apenas agregações suprimidas da Zona C. | N/A (regra de segurança permanente). |
| **ADR-004** | Publicação externa unicamente por PDF estático imutável | Links interativos públicos ou embeds web | Garante que nenhuma informação seja publicada sem tripla checagem humana (coordenação e diretoria). | N/A (regra de governança permanente). |
| **ADR-005** | Manter áudio e relatos livres fora do MVP (Módulo E) | Coletar gravações de voz desde o início | Blindagem da equipe contra sobrecarga de triagem e proteção da privacidade das famílias. | Ativar apenas após atendimento integral dos critérios do Portão G5. |
| **ADR-006** | Rotina de agregação com Apps Script e fórmulas controladas | Consolidação manual pela coordenação | Repetibilidade do cálculo de médias e aplicação estrita das regras de supressão ($n < 10$). | Reavaliar periodicamente a manutenção dos scripts. |

---

## 4. Planejamento por Portões de Decisão (Gate System)

```
[G0: Fundação] ---> [G1: Piloto Sintético] ---> [G2: Piloto Real Controlado] ---> [G3: Expansão] ---> [G4: Publicação] ---> [G5: Módulo E]
```

1. **Portão G0 — Fundação Técnica e Metodológica (Semana 11)**:
   - Registro formal de ADR-001 a ADR-006;
   - PoC técnica offline e simulação de concorrência com AppSheet/Sheets;
   - Verificação de elegibilidade e limites do Google Workspace for Nonprofits (H-03);
   - Rubricas v0 dos 3 indicadores e Dicionário de Dados v0.
2. **Portão G1 — Piloto Sintético e Simulação de Campo (Semana 12)**:
   - Validação da arquitetura com 100% de dados sintéticos (120+ crianças, 4 programas);
   - Teste cronometrado de usabilidade de campo (< 4 min no piloto / < 3 min em regime);
   - Teste da matriz de permissões por perfil (voluntário, coordenação, psicologia);
   - Ensaio de rotina de backup (RPO <= 24h) e restauração (RTO <= 5 dias úteis).
3. **Portão G2 — Piloto Real Controlado (Semanas 13 a 17)**:
   - Parecer jurídico/ético sobre privacidade (LGPD/ECA);
   - Autorização institucional e termo de comunicação aos responsáveis;
   - Definição da política de retenção e descarte;
   - Teste de permissão e vazamento aprovado;
   - Treinamento presencial de 30 minutos dos voluntários pilotos.
4. **Portão G3 — Expansão Programática (Semanas 19 a 22)**:
   - Metas do piloto atingidas (registro D0 > 80%, esforço coordenação <= 1 h/semana);
   - Calibração de rubricas entre avaliadores consolidada.
5. **Portão G4 — Publicação e Prestação de Contas Externa (Semana 23 / D+90)**:
   - Regras de supressão ($n < 10$) validadas;
   - Inclusão mandatória do disclaimer "O que este relatório não afirma";
   - Aprovação formal e assinatura digital da diretoria no PDF estático.
6. **Portão G5 — Módulo Opcional E (Escuta e Voz)**:
   - Parecer específico, orçamento para transcrição e capacidade operacional de triagem demonstrada.

---

## 5. Estrutura do Repositório e Artefatos

```text
├── data/
│   ├── schemas/
│   │   └── dictionary.json          # Dicionário de dados com classificação por Zonas A-D
│   └── synthetic/                   # Datasets sintéticos 100% livres de dados reais
├── src/
│   ├── app.py                       # Servidor local de prototipagem e validação interativa
│   ├── core/
│   │   ├── config.py                # Limites constitucionais, supressão (n<10) e zonas
│   │   ├── models.py                # Modelos Pydantic aderentes ao PRD v2.0
│   │   ├── mdm.py                   # Gestão do Golden Record EBZ-### e separação civil
│   │   └── metrics.py               # Motor analítico com supressão de pequenas células
│   ├── services/
│   │   ├── collection_service.py    # Coleta de campo com escalas fechadas
│   │   ├── coordination_service.py  # Painel de pendências D0
│   │   ├── therapy_service.py       # Registro restrito de metadados da psicologia
│   │   └── triage_service.py        # Módulo E (isolado fora do MVP)
│   ├── api/                         # Rotas da aplicação
│   └── templates/                   # Interfaces com alertas de governança e disclaimers
└── tests/                           # Bateria de testes automatizados de regras éticas e contratos
```
