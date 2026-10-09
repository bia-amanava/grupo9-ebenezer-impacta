# Feature Specification: Ebenézer Impacta — Plataforma de Acompanhamento Ético e Prestação de Contas Agregada

**Feature Identifier**: `001-ebenezer-impacta`  
**PRD Reference**: PRD v2.0 (revisado)  
**Created**: 2026-10-05 | **Updated**: 2026-10-09  
**Status**: Revised Specification (Draft para Spec Kit)  
**Instituição**: Instituto Social Ebenézer (Jardim Ângela, São Paulo)  
**Contexto**: MBA em IA & Dados para Negócios (Inteli) — Módulo 3  

---

## 1. Visão Geral e Fronteiras do Produto

### 1.1 Visão do Produto
> Transformar registros rápidos e não clínicos de oficinas em **trajetórias programáticas agregadas, verificáveis e protegidas**, para apoiar a gestão pedagógica e a prestação de contas do Instituto, sem expor a vida clínica das crianças.

*Alinhamento com o PRD v2.0:* Benefícios de retenção de doadores, atração de investimentos ou conformidade fiscal integral passam a ser **hipóteses de benefício**, e não promessas do software. O produto entrega dados de execução e observação pedagógica agregados, sem alegações de causalidade.

### 1.2 Fora de Escopo Explícito
1. **Dados Clínicos:** Prontuários, hipóteses diagnósticas, histórico de saúde, narrativas de acolhimento ou qualquer dado clínico individual (CFP/LGPD).
2. **Dados Reais Prematuros:** Coleta de dados reais de crianças ou famílias antes da homologação formal do **Portão G2**.
3. **Áudio e Relatos Livres no MVP:** Áudio, transcrição e relatos livres de famílias ou oficineiros (alocados exclusivamente no **Módulo Opcional E**, fora do MVP, condicionado ao Portão G5).
4. **Painéis Abertos ao Vivo:** Painel, dashboard ou página pública conectada diretamente à base operacional viva.
5. **Promessas Financeiras e Fiscais:** Projeção de receita, retenção garantida de doadores (rejeitado R$ 16k/ano) ou captação via incentivo fiscal como promessa intrínseca do software.
6. **Atribuição Causal:** Afirmação de que as melhorias socioemocionais foram causadas estritamente pelas oficinas.
7. **IA Preditiva ou Classificatória:** Uso de inteligência artificial para classificar, pontuar ou rotular comportamento de crianças.

---

## 2. Histórias de Usuário Priorizadas

### US-01 (P1 · MVP) — Registrar Chamada da Turma
**Como** educador voluntário de sábado,  
**Quero** marcar presença por toque rápido no smartphone,  
**Para** concluir a chamada em poucos segundos e liberar os alunos pontualmente.
- **Critérios de Aceite:**
  1. *Given* a turma aberta no dia, *When* o voluntário toca em cada criança, *Then* o status alterna presente/ausente e o totalizador atualiza imediatamente.
  2. *Given* dispositivo sem internet, *When* o envio é acionado, *Then* o registro persiste localmente com indicação de sincronização pendente e efetua o flush ao reconectar, sem duplicidades.
  3. *Given* chamada já existente para (turma + data), *When* o voluntário tenta reenviar, *Then* o sistema abre a chamada existente para edição (idempotência).

### US-02 (P1 · MVP) — Registrar 3 Observações Pedagógicas por Criança Presente
**Como** educador voluntário,  
**Quero** selecionar valores em escalas fechadas (1 a 5, incluindo opção "Não observado"),  
**Para** alimentar a série longitudinal pedagógica sem redigir texto livre.
- **Critérios de Aceite:**
  1. *Given* criança presente, *When* o voluntário marca os 3 indicadores (Autonomia, Convivência em Grupo e Participação Ativa), *Then* o registro armazena valor, versão da rubrica e identificação do autor.
  2. *Given* aluno presente sem os 3 indicadores, *When* tenta enviar, *Then* o sistema avisa quais faltam, permitindo justificativa fechada ("Não observado").
  3. Formulário inspecionado contém **0 campos de texto livre**.

### US-03 (P1 · MVP) — Acompanhar Pendências do Mesmo Dia (D0)
**Como** coordenadora geral,  
**Quero** visualizar quais turmas não registraram a chamada até o encerramento do sábado,  
**Para** acionar os educadores faltantes em menos de 1 minuto.
- **Critérios de Aceite:**
  1. *Given* a data do encontro, *When* abre o painel D0, *Then* vê turmas pendentes, parciais e concluídas, com horário do último envio.

### US-04 (P1 · MVP) — Manter Cadastro Mestre Pseudonimizado (MDM)
**Como** coordenadora geral,  
**Quero** gerenciar participantes com ID único pseudonimizado (`EBZ-###`) e matrículas por programa,  
**Para** acompanhar trajetórias sem expor dados civis no dia a dia operacional.
- **Critérios de Aceite:**
  1. *Given* novo cadastro coincidente com registro existente segundo regras de deduplicação, *When* submetido, *Then* bloqueia e exige revisão.
  2. *Given* criança matriculada em múltiplos programas, *When* consultada, *Then* o sistema associa ambas as matrículas ao mesmo ID pseudonimizado.

### US-05 (P2 · MVP) — Registrar Metadados da Vivência Terapêutica
**Como** psicóloga da instituição (guardiã ética),  
**Quero** registrar ocorrência (S/N), duração em minutos, total agregado de participantes presentes e checklist de infraestrutura,  
**Para** prestar contas da carga horária sem violar o sigilo profissional (CFP/LGPD).
- **Critérios de Aceite:**
  1. Interface estritamente restrita: 0 campos de nome de criança, 0 prontuários, 0 diagnósticos (CID) ou anotações clínicas.
  2. A tabela de vivências no banco não possui chave estrangeira para participante individual.

### US-06 (P2 · MVP) — Gerar Relatório Agregado com Revisão Humana
**Como** coordenação e diretoria,  
**Quero** gerar relatório a partir de dados analíticos agregados,  
**Para** prestar contas do que foi executado e observado com rigor e segurança.
- **Critérios de Aceite:**
  1. *Given* período selecionado, *When* gera o relatório, *Then* extrai exclusivamente da Zona C (analítica), aplicando regra de supressão para amostras pequenas ($n < 10$).
  2. *Given* relatório gerado, *When* inspecionado, *Then* exibe obrigatoriamente a seção "O que este relatório não afirma" (limitações metodológicas e ausência de causalidade).
  3. Relatório só pode ser classificado como "publicável" após registro de aprovação formal (nome, data, versão).

### US-07 (P2 · MVP) — Corrigir e Auditar Registros
**Como** coordenadora,  
**Quero** retificar registros operacionais mantendo trilha de auditoria,  
**Para** assegurar governança e integridade das informações.
- **Critérios de Aceite:**
  1. Toda alteração registra autor, timestamp, valor anterior e motivo selecionado em taxonomia fechada.

### US-08 (P3 · Pós-Piloto) — Caderno de Evidências de Execução
**Como** diretoria,  
**Quero** exportar dossiê estruturado de execução (datas, frequência, carga horária e permanência),  
**Para** fundamentar prestações de contas a financiadores e mantenedores.
- Conteúdo descritivo de execução física; não garante parecer contábil ou fiscal.

### US-09 (P3 · Pós-Piloto) — Relatório Semestral para Doadores
**Como** equipe de comunicação/captação,  
**Quero** modelo sintetizado de 2 páginas com indicadores agregados aprovados,  
**Para** manter relacionamento transparente com doadores.
- Apenas após Portão G4; sem recortes de turmas pequenas; sem falas individuais literais.

### US-10 (Opcional · Módulo E — FORA DO MVP) — Escuta de Responsáveis e Voz
**Status**: Condicionado ao **Portão G5** (parecer jurídico, teste de segurança, política de descarte e capacidade de triagem comprovada).

---

## 3. Requisitos Funcionais Detalhados

### 3.1 Cadastro e Identidade
- **FR-001**: ID único pseudonimizado no formato `EBZ-###`, sem conter dados pessoais na codificação.
- **FR-002**: Dados civis fisicamente armazenados na Zona A (restrita), separados da base operacional (Zona B).
- **FR-003**: Suporte a matrículas múltiplas por programa/turma com datas e status.
- **FR-004**: Regras de deduplicação e log formal de fusões ou correções.
- **FR-005**: Pseudônimo pedagógico opcional para exibição em sala (a definir em ADR).

### 3.2 Coleta em Campo
- **FR-010**: Chamada com registro único por tripla (turma, data, participante). Reenvio não gera duplicação (idempotência).
- **FR-011**: 3 indicadores em escalas fechadas (1 a 5), opção "Não observado" e vínculo com versão da rubrica.
- **FR-012**: Operação offline nativa com indicador visual de status de sincronização e flush automático.
- **FR-013**: Validação pré-envio de consistência e restrições de data.
- **FR-014**: Edição de registros permitida ao voluntário apenas na janela definida (até domingo seguinte); fora disso, apenas coordenação com justificativa.
- **FR-015**: Formulários do fluxo do voluntário com **0 campos de texto livre**.

### 3.3 Módulo da Psicologia (Fronteira Ética)
- **FR-020**: Interface restrita com campos exclusivos: realizada (S/N), data, duração (minutos), total de presentes agregados e checklist de infraestrutura.
- **FR-021**: Nenhuma chave estrangeira de participante na tabela de metadados da vivência.

### 3.4 Gestão, Relatórios e Publicação
- **FR-030**: Painel de pendências D0 destacando turmas pendentes, parciais e concluídas.
- **FR-031**: Painel de qualidade com indicadores de completude, duplicidades e atraso.
- **FR-032**: Painel gerencial interno lendo exclusivamente a Zona C.
- **FR-033**: Geração de relatório em PDF a partir de dados agregados com metadados de versão e seção de limitações metodológicas.
- **FR-034**: Regra de supressão obrigatória: ocultar agregações com amostras menores que $n < 10$.
- **FR-035**: Fluxo de aprovação em quatro estados: `GERADO` → `REVISADO_COORDENACAO` → `APROVADO_DIRETORIA` → `ARQUIVADO`.
- **FR-036**: Publicação externa estritamente por **arquivo estático imutável aprovado**, vedado link vivo à base.
- **FR-037**: Caderno de evidências de execução para fins institucionais (pós-piloto).
- **FR-038**: Exportação completa em formato aberto (CSV) para evitar aprisionamento tecnológico.

### 3.5 Módulo Opcional E (Fora do MVP — Portão G5)
- **FR-E01**: Canal opcional de texto curto para responsáveis familiares.
- **FR-E02**: Observação pontual por voz para oficineiros.
- **FR-E03**: Fila privada de triagem com estados controlados e tempo de mediação contabilizado fora da 1 h/semana.
- **FR-E04**: Mídias e textos brutos isolados da base analítica e do Looker Studio.
- **FR-E05**: Política formal de retenção e expurgo automático.
- **FR-E06**: Alternativa assistida presencial para famílias sem acesso digital.

---

## 4. Métricas e Metas de Sucesso

| Dimensão | Métrica | Meta Piloto (S13–S17) | Meta Regime Regular |
|---|---|---|---|
| **Adoção** | Registro no mesmo dia (D0) | > 80% | > 90% |
| **Esforço** | Tempo médio de coleta por turma | < 4 minutos | < 3 minutos |
| **Qualidade** | Cobertura de indicadores (presentes com notas) | > 75% | > 85% |
| **Integridade** | Duplicidades cadastrais e registros órfãos | 0 | 0 |
| **Satisfação** | CSAT de voluntários | > 4,0 / 5,0 | > 4,5 / 5,0 |
| **Gestão** | Esforço semanal da coordenação | <= 1,5 h/sem | <= 1,0 h/sem |
| **Segurança** | Incidentes de vazamento ou acesso indevido | 0 | 0 |
| **Governança** | Relatórios publicados com aprovação formal prévia | 100% | 100% |

---

## 5. Portões de Decisão (Gate System)

- **Portão G0 (Fundação)**: ADR-001 a 006 formalizados; PoC offline validada; elegibilidade de licenças confirmada; rubricas v0; dicionário de dados v0.
- **Portão G1 (Piloto Sintético)**: Validação 100% sintética; teste de usabilidade; matriz de acessos testada; ensaio de backup/restauração.
- **Portão G2 (Piloto Real Controlado)**: Parecer jurídico LGPD/ECA; autorização da diretoria; política de retenção; comunicação aos responsáveis; treinamento de voluntários. *(Obrigatório para transição de dados sintéticos para reais)*.
- **Portão G3 (Expansão)**: Metas do piloto atingidas; carga de gestão sustentável; rubricas calibradas entre avaliadores.
- **Portão G4 (Publicação Externa)**: Regras de supressão $n < 10$ testadas; texto de limitações aprovado; autorização da diretoria; arquivo estático gerado.
- **Portão G5 (Módulo Opcional E)**: Parecer específico para voz/texto; capacidade de triagem comprovada; orçamento específico de transcrição.
