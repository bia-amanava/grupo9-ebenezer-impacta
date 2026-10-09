# Research & Technical Decisions: Ebenézer Impacta

**Feature**: `001-ebenezer-impacta`
**Date**: 2026-10-05

## 1. Technical Context Decisions

### Decision 1: Custo de Licença Zero & Stack Tecnológica
- **Decisão**: Arquitetura híbrida baseada em Google Workspace for Nonprofits (Google Sheets como base relacional / MDM + Looker Studio para visualização) com implementação de protótipo interativo web/mobile autônomo (Python FastAPI + HTML5/Tailwind Mobile-First) para testes locais, validação acadêmica e homologação de fluxos antes do deploy no AppSheet.
- **Racional**: O PRD exige conformidade estrita com custo de licença zero (RNF-01) e suporte a plano sem fins lucrativos. Ao fornecer tanto as especificações de esquemas tabulares do Google Sheets/AppSheet quanto uma aplicação web autônoma completa de demonstração com dados sintéticos, a equipe do MBA Inteli pode validar a experiência de uso de ponta a ponta sem barreiras de credenciais corporativas.
- **Alternativas consideradas**:
  - *Apenas planilhas manuais*: Rejeitado porque não atende ao requisito de teste de usabilidade em campo de < 3 minutos e nem à blindagem ética.
  - *SaaS proprietário pago (Salesforce Nonprofit Cloud, Power BI Pro)*: Rejeitado por violar RNF-01 (Custo zero).

### Decision 2: Segregação de Dados Civis vs. Golden Record Pseudonimizado (MDM)
- **Decisão**: Segregação física de tabelas: `MDM_PARTICIPANTES` utiliza identificadores alfanuméricos únicos imutáveis (`EBZ-001`, `EBZ-002`, ...). Os dados civis identificáveis residem em tabela estritamente apartada (`CADASTRO_CIVIL_RESTRITO`), cujo acesso é restrito unicamente à coordenação com controle de permissões. Nenhuma view analítica ou de campo do voluntário tem acesso a nomes civis ou dados de contato.
- **Racional**: Atende ao Princípio I da Constituição e aos requisitos RF-01 e RNF-04 (LGPD/ECA). A pseudonimização permite rastrear trajetórias longitudinais multi-programa sem expor a identidade dos menores.
- **Alternativas consideradas**:
  - *Tabela única com colunas ocultas*: Rejeitado por risco severo de vazamento acidental em exportações ou consultas do Looker Studio / AppSheet.

### Decision 3: Interface de Campo do Voluntário (< 3 min & Offline-First)
- **Decisão**: Formulário mobile de alta usabilidade com cards por participante, botões rápidos de presença e seletores fechados de 1 a 5 para os 3 indicadores (Autonomia, Convivência em Grupo, Participação Ativa). Armazenamento local imediato (Web LocalStorage / Cache) com disparo assíncrono para a base na presença de conectividade.
- **Racional**: Atende ao RNF-02 e RF-02. Elimina digitação de texto ou sobrecarga cognitiva para o voluntário de sábado.
- **Alternativas consideradas**:
  - *Campo de observação aberta por texto*: Rejeitado expressamente pelo PRD (RF-03) para evitar rótulos subjetivos pejorativos ou estigmatizantes.

### Decision 4: Módulo de Vivência Terapêutica da Psicologia (Sigilo CFP)
- **Decisão**: Formulário restrito que coleta unicamente 4 metadados: Data, Duração em Minutos, Total Agregado de Presentes e Tópicos Pedagógicos Abordados (seleção múltipla em taxonomia fechada). Bloqueio programático total de campos de prontuário, CID ou observações individuais.
- **Racional**: Atende ao Código de Ética Profissional do Psicólogo (CFP) e RF-03. Preserva a comprovação de carga horária para editais sem violar o sigilo terapêutico.
- **Alternativas consideradas**:
  - *Permitir notas clínicas protegidas por senha dentro do sistema*: Rejeitado categoricamente pelo PRD e Constituição por elevar o risco regulatório e institucional.

### Decision 5: Governança dos Canais Opcionais e Fila de Triagem (RF-05, RF-06, RF-07)
- **Decisão**: Repositório de arquivos brutos e tabela `ENTRADA_FEEDBACK_RESTRITA` mantidos em quarentena. Fila de triagem com máquina de estados finita: `RECEBIDO` → `EM_TRIAGEM` → [`APROVEITADO_CATEGORIA_PEDAGOGICA` | `DESCARTADO` | `ENCAMINHADO_PROTOCOLO_EXTERNO`]. Somente registros com síntese pedagógica fechada aprovada pela coordenação geram registros na tabela `SINTESE_PEDAGOGICA`. Nenhum áudio ou transcrição é indexado para dashboards.
- **Racional**: Atende aos requisitos RF-07, RNF-04 e RNF-05. Protege a instituição contra passivos jurídicos e garante resposta ética a relatos que envolvam violação de direitos (encaminhamento externo).
- **Alternativas consideradas**:
  - *Transcrição automática direta com LLM exibida no painel*: Rejeitado categoricamente pelo PRD (a IA pode alucinar ou reidentificar dados sensíveis sem supervisão).

### Decision 6: Motor de Relatórios & Evidências de Captação
- **Decisão**: Módulo automatizado de geração de relatórios com:
  1. *Curvas Longitudinais por Coorte*: Evolução média trimestral nos 3 eixos socioemocionais.
  2. *Dossiê de Execução Fiscal*: Tabela de evidências com carimbo de data/hora, frequência percentual e horas executadas (Lei Rouanet / Lucro Real).
  3. *Donor Success (2 Páginas)*: Resumo executivo de impacto de investimento e retenção de doadores.
  4. *Dataset Público*: Dados sintéticos agregados prontos para publicação em portal web sem risco de reidentificação.
