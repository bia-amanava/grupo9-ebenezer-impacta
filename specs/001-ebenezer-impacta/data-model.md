# Data Model: Ebenézer Impacta

**Feature**: `001-ebenezer-impacta`
**Date**: 2026-10-05

## Entidades e Esquemas Relacionais

### 1. `MDM_PARTICIPANTES` (Golden Record Cadastral)
Base unificada e pseudonimizada de todos os educandos atendidos pelo Instituto Social Ebenézer.
- **participant_id** (PK, String): Código alfanumérico único imutável (ex: `EBZ-001`, `EBZ-002`).
- **coorte_ano** (Integer): Ano de ingresso no Instituto (ex: `2024`, `2025`, `2026`).
- **faixa_etaria** (String): `PRIMEIRA_INFANCIA` (0-6), `CRIANCA` (7-11), `ADOLESCENTE` (12-17).
- **matriculas_ativas** (Array[String]): Lista de IDs de programas onde o participante está ativo.
- **status** (String): `ATIVO`, `INATIVO`, `TRANSFERIDO`, `EGRESSO`.
- **data_cadastro** (Date): Data da primeira matrícula.

### 2. `CADASTRO_CIVIL_RESTRITO` (Base Segregada com Acesso Restrito)
Base isolada contendo dados de identificação civil das crianças e responsáveis. Protegida por criptografia e acessível exclusivamente pela Coordenação Geral.
- **civil_id** (PK, UUID): Identificador do registro civil.
- **participant_id** (FK, String): Chave de ligação ao MDM (protegida).
- **nome_completo_crianca** (String): Nome civil da criança.
- **data_nascimento** (Date): Data de nascimento.
- **nome_responsavel** (String): Nome do responsável legal.
- **parentesco** (String): `MAE`, `PAI`, `AVO`, `TUTOR_LEGAL`, `OUTRO`.
- **telefone_contato** (String): Telefone de contato.
- **endereco_bairro** (String): Bairro de residência (ex: Jardim Ângela).
- **termo_consentimento_lgpd** (Boolean): Termo de consentimento assinado.

### 3. `PROGRAMAS_OFICINAS`
Catálogo de programas e oficinas socioeducativas ministradas na instituição.
- **programa_id** (PK, String): Identificador (ex: `PROG-SONHOS`, `PROG-REFORCO`, `PROG-INFANCIA`, `PROG-VIVENCIAS`).
- **nome** (String): `Laboratório de Sonhos`, `Reforço Escolar`, `Primeira Infância`, `Vivências Terapêuticas`.
- **eixo_pedagogico** (String): Descrição da finalidade socioeducativa.
- **dia_semana** (String): `SABADO`, `SEGUNDA_A_SEXTA`.
- **carga_horaria_sessao_minutos** (Integer): Duração padrão (ex: `120`).
- **voluntario_responsavel_id** (String): Identificador do educador voluntário líder.

### 4. `ENCONTROS_OPERACIONAIS`
Registro de cada sessão de oficina realizada.
- **encontro_id** (PK, UUID/String): Identificador único do encontro.
- **programa_id** (FK, String): Referência ao programa.
- **data_encontro** (Date): Data de realização (ex: `2026-10-03`).
- **horario_inicio** (Time): Horário de início.
- **horario_fim** (Time): Horário de término.
- **educador_id** (String): Voluntário que aplicou a oficina.
- **data_envio_registro** (DateTime): Timestamp de quando a chamada foi enviada.
- **status_lancamento** (String): `D0_NO_PRAZO` (mesmo dia), `ATRASADO`, `PENDENTE`.

### 5. `AVALIACOES_SOCIOEMOCIONAIS` (Escalas Fechadas)
Registros de presença individual e mensuração dos 3 indicadores observáveis em campo.
- **avaliacao_id** (PK, UUID/String): Identificador único do registro de avaliação.
- **encontro_id** (FK, String): Referência ao encontro.
- **participant_id** (FK, String): Código pseudonimizado do participante (ex: `EBZ-015`).
- **presenca** (Boolean): `true` (Presente) ou `false` (Ausente).
- **score_autonomia** (Integer, Nullable): Escala de 1 a 5 (somente se presente).
- **score_convivencia** (Integer, Nullable): Escala de 1 a 5 (somente se presente).
- **score_participacao** (Integer, Nullable): Escala de 1 a 5 (somente se presente).
- **timestamp_registro** (DateTime): Data e hora da submissão.
*Regra de Validação*: Sem campos de texto livre ou áudio permitidos nesta tabela.

### 6. `VIVENCIAS_TERAPEUTICAS_METADADOS` (Módulo Blindado da Psicóloga)
Registro de sessões de suporte psicossocial.
- **vivencia_id** (PK, UUID/String): Identificador da sessão terapêutica.
- **data** (Date): Data do encontro.
- **psicologa_responsavel** (String): Registro profissional/identificador.
- **duracao_minutos** (Integer): Duração da atividade em minutos.
- **total_presentes_agregado** (Integer): Contagem total de participantes presentes.
- **topicos_pedagogicos** (Array[String]): Categorias trabalhadas (ex: `["AUTOCUIDADO", "REGULACAO_EMOCIONAL", "VINCULO_COMUNITARIO", "RESOLUCAO_DE_CONFLITOS"]`).
*Regra de Validação*: Proibição absoluta de campos nominais, relatórios individuais ou prontuários.

### 7. `ENTRADA_FEEDBACK_RESTRITA` (Quarentena de Escuta Segregada - RF-05/RF-06)
Recepção isolada de relatos facultativos de responsáveis e educadores.
- **feedback_id** (PK, UUID/String): Identificador do relato.
- **participant_id** (FK, String): ID interno pseudonimizado.
- **tipo_origem** (String): `RESPONSAVEL_FAMILIAR` ou `OFICINEIRO`.
- **tipo_midia** (String): `TEXTO` ou `AUDIO`.
- **data_recebimento** (DateTime): Carimbo de recepção.
- **status_triagem** (Enum): `RECEBIDO`, `EM_TRIAGEM`, `APROVEITADO`, `DESCARTADO`, `PROTOCOLO_EXTERNO`.
- **referencia_arquivo_protegido** (String): URI segura do arquivo em quarentena criptografada.
- **consentimento_registrado** (Boolean): Confirmação de consentimento.

### 8. `SINTESE_PEDAGOGICA` (Classificação Moderada para Análise - RF-07)
Apenas sínteses desidentificadas e categorias fechadas aprovadas pela coordenação.
- **sintese_id** (PK, UUID/String): Identificador da síntese aprovada.
- **feedback_id** (FK, String): Referência ao feedback original.
- **categoria_fechada** (String): `ENGAJAMENTO_FAMILIAR_POSITIVO`, `DESENVOLVIMENTO_DE_HABILIDADES`, `COLABORACAO_PEDAGOGICA`.
- **periodo_letivo** (String): Ex: `2026.1`.
- **programa_id** (FK, String): Programa correlato.
- **coordenador_aprovador_id** (String): Identificador da coordenadora que moderou.
- **data_aprovacao** (DateTime): Timestamp de aprovação.

## Transições de Estado (Fila de Triagem)

```text
[ RECEBIDO ]
     │
     ▼
[ EM_TRIAGEM ] (Coordenação designada analisa o conteúdo isoladamente)
     │
     ├──► [ APROVEITADO ] ──► Cria registro em SINTESE_PEDAGOGICA (categoria fechada)
     │
     ├──► [ DESCARTADO ] ──► Conteúdo irrelevante ou ruído; marcado para descarte
     │
     └──► [ PROTOCOLO_EXTERNO ] ──► Conteúdo sensível/violação de direitos; expurgado
                                     do sistema analítico e conduzido por via externa
```
