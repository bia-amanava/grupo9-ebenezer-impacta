<!--
Sync Impact Report:
- Version change: 1.0.0 -> 2.0.0
- List of modified principles:
  - Ratification of the 10 Inegociable Principles of PRD v2.0 (Ebenézer Impacta):
    - I. Melhor Interesse da Criança (prevalece sobre qualquer métrica, relatório ou meta de captação)
    - II. Minimização (coleta estrita com finalidade documentada no dicionário de dados)
    - III. Fronteira Clínica (zero dado clínico no sistema; psicóloga como guardiã ética; apenas metadados e checklist de infraestrutura)
    - IV. Pseudonimização ≠ Anonimização (ID não torna o dado anônimo; acesso restrito mesmo a pseudonimizados)
    - V. Separação por Zonas de Sensibilidade (A: restrita civil, B: operacional, C: analítica agregada com supressão, D: publicação estática aprovada, E: módulo opcional isolado)
    - VI. Revisão Humana Antes de Qualquer Publicação (proibição de publicação viva ou automática a partir da base operacional)
    - VII. Afirmações com Evidência (linguagem de hipótese; rejeição de valores e promessas sem base como R$ 16k, R$ 15-35k ou conformidade fiscal garantida)
    - VIII. Simplicidade Proporcional (rotina da coordenação planejada para <= 1 h/semana, a validar no piloto)
    - IX. Saída Possível (portabilidade em formato aberto CSV; sem aprisionamento tecnológico)
    - X. Dados Sintéticos Obrigatórios até o Portão G2 (nenhum dado real de menor manipulado antes de parecer jurídico e homologação)
- Added sections:
  - Portões de Decisão (G0 a G5)
  - Zonas Físicas de Sensibilidade (A, B, C, D, E)
  - Módulo E Isolado como Fora do MVP
- Removed sections:
  - Afirmações de "Custo de Licença Zero Garantido" e números desprovidos de base (R$ 16k, R$ 15-35k, 180h poupadas) convertidos em hipóteses de teste
-->

# Ebenézer Impacta Constitution (v2.0)

## Core Principles (Os 10 Princípios Inegociáveis)

### I. Melhor Interesse da Criança
O bem-estar, a dignidade e a integridade de crianças e adolescentes prevalecem sobre qualquer métrica pedagógica, relatório institucional ou meta de captação de recursos. Nenhum dado é coletado ou exposto se representar risco ou constrangimento ao educando.

### II. Minimização
Coleta-se unicamente o que possui finalidade explícita e documentada no dicionário de dados. É vedada a captação de dados secundários, cadastros excessivos ou campos que não sustentem diretamente a rotina pedagógica ou a prestação de contas agregada.

### III. Fronteira Clínica
Nenhum dado clínico entra no produto. O sistema NUNCA coletará, armazenará ou processará prontuários psicológicos ou médicos, hipóteses diagnósticas, histórico de saúde ou narrativas íntimas de acolhimento. A profissional de psicologia é a guardiã ética dessa fronteira, e o módulo de vivências registra exclusivamente metadados agregados (ocorrência, duração, volume total de presentes e checklist de infraestrutura).

### IV. Pseudonimização ≠ Anonimização
O identificador pseudonimizado (Golden Record `EBZ-###`) não torna o dado anônimo. O risco de reidentificação persiste, razão pela qual o acesso a registros pseudonimizados é estritamente controlado e restrito aos perfis operacionais pertinentes.

### V. Separação por Zonas de Sensibilidade
Como as permissões em ecossistemas de planilhas/arquivos operam por arquivo (abrir o arquivo expõe todas as abas), a separação é física (arquivos e repositórios apartados), organizada em 5 zonas:
- **Zona A (Restrita)**: Dados civis identificáveis (nome completo, filiação, contatos). Acesso mínimo e exclusivo à coordenação designada com MFA.
- **Zona B (Operacional)**: IDs pseudonimizados, matrículas, presenças, indicadores em escalas fechadas e metadados de vivência. Acesso via app por perfil.
- **Zona C (Analítica)**: Camada de dados agregados com aplicação obrigatória de regras de supressão ($n < 10$). Fonte exclusiva para relatórios internos e dashboards.
- **Zona D (Publicada)**: Arquivos estáticos imutáveis (PDFs/imagens) com aprovação humana formalizada e versionamento registrado.
- **Zona E (Opcional - Fora do MVP)**: Relatos facultativos de famílias e oficineiros. Armazenamento fisicamente isolado e condicionado ao Portão G5.

### VI. Revisão Humana Antes de Qualquer Publicação
Nenhum relatório externo é gerado diretamente da base operacional, e é terminantemente vedada a publicação de links vivos ou dinâmicos conectados à base de dados. Todo relatório exige fluxo formal de aprovação: gerado → revisão da coordenação → aprovação da diretoria → arquivo estático imutável.

### VII. Afirmações com Evidência
O produto e seus relatórios não afirmam mais do que os dados sustentam:
- Benefícios financeiros, retenção de doadores e conformidade com leis de incentivo são **hipóteses**, não promessas do produto.
- Ficam expressamente **rejeitados do discurso técnico os números sem base do passado** (ex.: "retenção de R$ 16.000/ano", "captação de R$ 15–35 mil", "180 h poupadas", "relatório em < 24 h", "atende integralmente à Lei Rouanet").
- Todos os relatórios externos devem conter seção obrigatória de **limitações metodológicas** ("O que este relatório não afirma"), vedando qualquer atribuição causal direta às oficinas.

### VIII. Simplicidade Proporcional
A solução precisa ser operável pela coordenação com esforço sustentável (estimativa de até 1 h/semana em regime regular, a ser cronometrada no piloto). Complexidade técnica desnecessária que aumente o custo de manutenção deve ser rejeitada.

### IX. Saída Possível (Sem Aprisionamento)
Todos os dados pertencem ao Instituto Social Ebenézer e devem ser integralmente exportáveis em formatos abertos (CSV/JSON). Nenhuma decisão arquitetural pode aprisionar a instituição a um fornecedor ou ferramenta proprietária.

### X. Dados Sintéticos Obrigatórios até o Portão G2
Até a homologação formal do **Portão G2** (piloto real controlado com parecer jurídico, autorização institucional, consentimento de responsáveis e política de descarte), o ambiente de desenvolvimento e testes operará estritamente com dados 100% sintéticos.

---

## Portões de Decisão e Ciclo de Entrega

1. **Portão G0 (Fundação)**: ADR-001 a ADR-006 formalizados, PoC técnica offline validada, confirmação de elegibilidade de licenças (H-03), rubricas v0 e dicionário de dados v0.
2. **Portão G1 (Piloto Sintético)**: Validação com dados sintéticos, teste de usabilidade mobile (< 4 min piloto / < 3 min regime), matriz de permissões testada, ensaio de backup/restauração.
3. **Portão G2 (Piloto Real Controlado)**: Parecer jurídico LGPD/ECA aprovado, comunicação aos responsáveis, autorização da diretoria, política de retenção, teste de vazamento e treinamento.
4. **Portão G3 (Expansão)**: Metas do piloto atingidas, carga da coordenação <= 1 h/sem comprovada, rubricas calibradas entre avaliadores.
5. **Portão G4 (Publicação Externa)**: Regras de supressão ($n < 10$) aprovadas, parecer contra reidentificação, aprovação formal da diretoria, inserção de limitações metodológicas.
6. **Portão G5 (Módulo Opcional E - Voz/Escuta)**: Critérios específicos: parecer jurídico, orçamento próprio para transcrição, capacidade de triagem comprovada fora da 1 h/sem.

---

## Governança

- Esta Constituição prevalece sobre quaisquer documentos técnicos, PRDs legados, especificações ou tarefas.
- Quaisquer emendas exigem justificativa formal, análise de impacto e registro de versão semântica.
- Todos os artefatos do Spec Kit (`spec.md`, `plan.md`, `tasks.md`, `data-model.md`) devem respeitar integralmente os 10 princípios acima.

**Version**: 2.0.0 | **Ratified**: 2026-10-09 | **Status**: Active
