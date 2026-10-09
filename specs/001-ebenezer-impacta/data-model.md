# Data Model: Ebenézer Impacta (v2.0)

**Feature**: `001-ebenezer-impacta` | **PRD Reference**: PRD v2.0 (revisado)  
**Date**: 2026-10-09

---

## Mapeamento por Zonas de Sensibilidade

De acordo com o Princípio V e a Seção 7.2 do PRD v2.0, as entidades estão distribuídas em repositórios fisicamente apartados para garantir privilégio mínimo:

```
Zona A (Restrita)     : PARTICIPANTE_CIVIL
Zona B (Operacional)  : PARTICIPANTE, PROGRAMA_TURMA, MATRICULA, ENCONTRO, PRESENCA, INDICADOR_RUBRICA, OBSERVACAO, VIVENCIA_META, LOG_AUDITORIA
Zona C (Analítica)    : AGREGADO_PUBLICAVEL (com supressão n < 10)
Zona D (Publicada)    : RELATORIO_VERSAO (PDF estático aprovado por humanos)
Zona E (Opcional)     : FEEDBACK_RESTRITO, SINTESE_MODERADA (Fora do MVP / Portão G5)
```

---

## Entidades Centrais do Domínio

### 1. `PARTICIPANTE_CIVIL` (Zona A — Restrita)
Base isolada com chave de criptografia e MFA, acessível unicamente à coordenação geral designada.
- **participant_id** (PK, String): Código alfanumérico único imutável (`EBZ-###`).
- **nome_civil_completo** (String): Nome civil da criança.
- **data_nascimento** (Date, Opcional): Data de nascimento completa (ou faixa etária para minimização).
- **nome_responsavel** (String): Nome do responsável legal.
- **contato_telefone** (String): Telefone de emergência/recado.
- **termo_consentimento_lgpd** (Boolean): Confirmação de ciência e consentimento informado dos responsáveis.
- *Retenção*: Conforme política institucional de descarte aprovada no Portão G2.

### 2. `PARTICIPANTE` (Zona B — Operacional Pseudonimizada)
Identificador mestre de circulação operacional entre voluntários e coordenação.
- **participant_id** (PK, String): Código alfanumérico único (`EBZ-###`).
- **pseudonimo_pedagogico** (String, Opcional): Ex: "Participante Sol" (a validar via ADR-lite).
- **faixa_etaria** (String): `PRIMEIRA_INFANCIA` (0-6), `CRIANCA` (7-11), `ADOLESCENTE` (12-17).
- **status** (String): `ATIVO`, `INATIVO`, `EGRESSO`.

### 3. `PROGRAMA_TURMA` (Zona B — Operacional)
Catálogo de oficinas e turmas socioeducativas.
- **programa_id** (PK, String): Identificador (ex: `PROG-SONHOS`, `PROG-REFORCO`, `PROG-INFANCIA`, `PROG-VIVENCIAS`).
- **turma_id** (PK/String): Identificador da turma (ex: `TURMA-A`, `TURMA-B`).
- **nome** (String): Nome descritivo da oficina.
- **oficineiro_id** (String): Voluntário responsável líder.

### 4. `MATRICULA` (Zona B — Operacional)
Relacionamento muitos-para-muitos entre participante e programas.
- **matricula_id** (PK, UUID/String): Identificador do vínculo.
- **participant_id** (FK, String): Referência ao `PARTICIPANTE`.
- **turma_id** (FK, String): Referência à `PROGRAMA_TURMA`.
- **status** (String): `ATIVA`, `CONCLUIDA`, `CANCELADA`.
- **data_inicio** (Date): Data de ingresso.
- **data_fim** (Date, Nullable): Data de encerramento da participação.

### 5. `ENCONTRO` (Zona B — Operacional)
Sessão realizada de oficina de sábado.
- **encontro_id** (PK, String): Identificador único da sessão.
- **turma_id** (FK, String): Turma correspondente.
- **data** (Date): Data de realização do encontro.
- **oficineiro_id** (String): Educador voluntário que conduziu a sessão.
- **status_registro** (String): `D0_NO_PRAZO`, `ATRASADO`, `PENDENTE`.
- **ts_envio** (DateTime): Carimbo de data/hora do recebimento da chamada.

### 6. `PRESENCA` (Zona B — Operacional)
Marcação individual rápida de presença do encontro.
- **encontro_id** (FK, String): Chave composta.
- **participant_id** (FK, String): Chave composta.
- **presente** (Boolean): `true` (Presente) ou `false` (Ausente).

### 7. `INDICADOR_RUBRICA` (Zona B — Operacional)
Definição metodológica das réguas de observação pedagógica.
- **indicador_id** (PK, String): `AUTONOMIA`, `CONVIVENCIA_EM_GRUPO`, `PARTICIPACAO_ATIVA`.
- **nome** (String): Nome descritivo do eixo observável.
- **escala** (String): `1_A_5_COM_NAO_OBSERVADO`.
- **versao** (String): Identificador semântico da rubrica pactuada (ex: `v1.0`).
- **descricao_observavel** (String): Comportamentos visíveis por nível.

### 8. `OBSERVACAO` (Zona B — Operacional)
Pontuações observadas em campo pelos voluntários (0 campos livres).
- **observacao_id** (PK, String): Identificador único.
- **encontro_id** (FK, String): Encontro correspondente.
- **participant_id** (FK, String): Código `EBZ-###`.
- **indicador_id** (FK, String): Referência ao indicador.
- **valor** (Integer, Nullable): Nota de 1 a 5, ou `null` se não observado.
- **nao_observado** (Boolean): Flag indicando ausência de oportunidade de observação justificada.
- **rubrica_versao** (String): Versão vigente no momento do registro.
- **autor_id** (String): Identificador do voluntário avaliador.

### 9. `VIVENCIA_META` (Zona B — Operacional da Psicologia)
Metadados estritamente agregados das sessões de apoio psicossocial (blindagem bioética CFP).
- **vivencia_id** (PK, String): Identificador do encontro.
- **data** (Date): Data da atividade.
- **realizada** (Boolean): `true` se ocorreu, `false` se cancelada.
- **duracao_minutos** (Integer): Tempo total (ex: 60 minutos).
- **total_presentes** (Integer): Contagem agregada de participantes atendidos.
- **checklist_infra** (Array[String]): Checagem de sala e condições estruturais.
- *Regra Inegociável*: Zero chaves de participante individual, zero relatórios individuais, notas clínicas ou diagnósticos (CID).

### 10. `AGREGADO_PUBLICAVEL` (Zona C — Analítica)
Camada agregada gerada por script automatizado com supressão de risco.
- **agregado_id** (PK, String): Identificador da linha consolidada.
- **periodo** (String): Ciclo avaliativo (ex: `2026.2`).
- **programa** (String): Nome do programa.
- **indicador** (String): Indicador socioemocional ou taxa de permanência.
- **metrica** (String): Média, mediana ou percentual agregado.
- **n** (Integer): Número de observações na amostra.
- **suprimido** (Boolean): `true` se $n < 10$ (valor ocultado para mitigar reidentificação), `false` se exibição autorizada.

### 11. `RELATORIO_VERSAO` (Zona D — Publicação Estática)
Trilha imutável de publicações em PDF e artefatos de prestação de contas.
- **relatorio_id** (PK, String): Identificador do relatório emitido.
- **periodo** (String): Período coberto.
- **versao** (String): Versão do documento (ex: `v1.0`).
- **status_aprovacao** (String): `GERADO`, `REVISADO_COORDENACAO`, `APROVADO_DIRETORIA`, `ARQUIVADO`.
- **aprovador_nome** (String): Nome do responsável que assinou a aprovação.
- **data_aprovacao** (DateTime): Timestamp de homologação humana.
- **arquivo_hash** (String): Hash SHA-256 do PDF estático gerado.
- **possui_limitacoes_metodologicas** (Boolean): Obrigatoriamente `true`.

### 12. `LOG_AUDITORIA` (Zona B — Governança Operacional)
Rastreabilidade de saneamentos e alterações cadastrais.
- **log_id** (PK, UUID): Identificador do evento.
- **entidade** (String): Nome da tabela modificada.
- **registro_id** (String): Chave do registro afetado.
- **autor** (String): Usuário que realizou a alteração.
- **timestamp** (DateTime): Data e hora exata.
- **valor_anterior** (JSON/String): Estado antes da modificação.
- **motivo** (String): Justificativa selecionada em lista fechada pela coordenação.

---

## Módulo Opcional E (Fora do MVP — Zona E)

Entidades isoladas mantidas em quarentena criptográfica independente, ativadas apenas após o **Portão G5**:
- `FEEDBACK_RESTRITO`: feedback_id, participant_id, tipo_origem, tipo_midia, status_triagem, referencia_arquivo_protegido, termo_consentimento.
- `SINTESE_MODERADA`: sintese_id, feedback_id, categoria_fechada_aprovada, periodo_letivo, coordenador_aprovador_id, data_aprovacao.
