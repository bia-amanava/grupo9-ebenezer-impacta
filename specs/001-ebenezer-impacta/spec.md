# Feature Specification: Ebenézer Impacta - Plataforma de Monitoramento Ético e Relatório de Transparência

**Feature Branch**: `001-ebenezer-impacta`

**Created**: 2026-10-05

**Status**: Draft

**Input**: User description: "Preciso criar uma solução baseada nesse arquivo prd, use o spec kit para desenvolver"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Coleta de Chamada e Avaliação Socioemocional Mobile-First em Campo (Priority: P1)

Como Voluntário / Educador Comunitário de oficina de sábado, desejo realizar a chamada da minha turma e registrar a observação de 3 indicadores socioemocionais (Autonomia, Convivência em Grupo e Participação Ativa) em menos de 3 minutos através do meu smartphone, mesmo se estiver sem conexão com a internet, para que eu possa liberar as crianças pontualmente sem sobrecarga burocrática e garantir que os dados cheguem no mesmo dia (D0).

**Why this priority**: É a espinha dorsal de toda a plataforma. Sem o registro rápido e de baixíssimo atrito em campo, não há dados para monitoramento, saneamento ou geração de relatórios de impacto.

**Independent Test**: Pode ser testado simulando o preenchimento de uma turma de 15 alunos em modo offline em um dispositivo móvel, medindo o tempo decorrido (<3 minutos) e validando o envio dos dados quando a conexão for reestabelecida.

**Acceptance Scenarios**:

1. **Given** um voluntário autenticado acessando sua oficina do dia com 15 participantes cadastrados, **When** ele preenche a lista de presença e marca as escalas fechadas dos 3 indicadores para cada aluno presente, **Then** o sistema conclui o envio em menos de 3 minutos e exibe confirmação visual imediata de registro concluído.
2. **Given** que o voluntário está sem conexão de internet na sede do projeto, **When** ele realiza o lançamento da chamada e indicadores, **Then** o sistema armazena localmente todos os registros de forma segura e sincroniza automaticamente com o servidor assim que a conexão de rede for restabelecida.
3. **Given** a interface de chamada e avaliação do voluntário, **When** o voluntário visualiza o formulário, **Then** o formulário contém apenas seletores binários de presença e botões com opções em escalas fechadas, sem campos abertos de texto livre ou gravação de áudio no fluxo padrão.

---

### User Story 2 - Cadastro Mestre Pseudonimizado (MDM) e Painel de Saneamento da Coordenação (Priority: P2)

Como Coordenadora Geral de Projetos, desejo visualizar em tempo real um painel de pendências de registros do dia ("Pendências D0") e manter uma base centralizada de dados cadastrais relacionando cada criança a um ID pseudonimizado único (ex: EBZ-026) com dados civis estritamente segregados, para que eu identifique turmas não lançadas em menos de 1 clique e dedique no máximo 1 hora semanal ao saneamento operacional.

**Why this priority**: Garante a governança e integridade das informações entre os múltiplos programas (Laboratório de Sonhos, Reforço Escolar, Primeira Infância e Vivências), impedindo duplicidades cadastrais e desoneração brutal do tempo da gestão.

**Independent Test**: Pode ser testado cadastrando alunos em múltiplos programas sob o mesmo código pseudonimizado e verificando se o painel de pendências acusa automaticamente oficinas que não enviaram registro até o horário limite de sábado.

**Acceptance Scenarios**:

1. **Given** uma criança que frequenta simultaneamente o Reforço Escolar e o Laboratório de Sonhos, **When** a coordenação cadastra suas matrículas, **Then** o sistema vincula ambas ao mesmo ID pseudonimizado único e impede criação de registros duplicados.
2. **Given** a base analítica do sistema, **When** qualquer usuário não autorizado acessa as tabelas de monitoramento, **Then** nenhum dado civil identificável (nome completo, endereço, telefone, RG/CPF) é exposto junto aos indicadores socioemocionais.
3. **Given** que 3 de 8 oficinas concluíram seu horário no sábado sem envio de chamada, **When** a Coordenadora abre o Painel de Pendências, **Then** as 3 turmas são destacadas com status pendente e indicação do educador responsável com apenas 1 clique.

---

### User Story 3 - Módulo Operacional Blindado da Vivência Terapêutica (Priority: P3)

Como Psicóloga da Instituição, desejo registrar exclusivamente os metadados agregados das sessões de vivência terapêutica (duração em minutos, quantidade total de presentes e tópicos socioeducativos abordados), sem qualquer registro de prontuário clínico ou notas nominais de comportamento, para assegurar o cumprimento integral do Código de Ética do CFP e da LGPD, protegendo as crianças contra estigmas.

**Why this priority**: Garante a conformidade bioética e regulatória, permitindo mensurar a carga horária e alcance das vivências de apoio psicossocial sem violar o sigilo profissional ou gerar vulnerabilidade jurídica para a organização.

**Independent Test**: Pode ser testado autenticando o perfil de psicologia, registrando uma sessão de acolhimento em grupo e confirmando que a interface restringe programaticamente qualquer tentativa de inserir dados nominais ou diagnósticos de saúde mental.

**Acceptance Scenarios**:

1. **Given** a psicóloga autenticada no módulo de vivências, **When** ela submete o registro de um encontro realizado, **Then** o sistema solicita unicamente data, duração em minutos, total agregado de participantes e temas pedagógicos trabalhados em lista fechada.
2. **Given** o formulário da vivência terapêutica, **When** a psicóloga inspeciona a interface, **Then** não existem campos para inserção de relatórios clínicos individuais, diagnósticos de CID ou anotações psicológicas confidenciais.

---

### User Story 4 - Emissão Automatizada de Relatórios de Transparência, Captação e Dossiês Fiscais (Priority: P4)

Como Diretor Institucional e Captador de Recursos, desejo gerar sob demanda e com 1 clique relatórios executivos de prestação de contas (dossiê auditável com carimbo temporal para Lei Rouanet e Lucro Real, relatório de 2 páginas "Impacto do Seu Investimento" para doadores e infográficos prontos para a Página Pública de Transparência), demonstrando a evolução socioemocional longitudinal dos participantes ao longo dos ciclos letivos.

**Why this priority**: Transforma os dados coletados em evidências auditáveis de impacto, garantindo a retenção de patrocinadores atuais (mitigando perda de receita estimada em R$ 16.000,00/ano) e habilitando a captação de R$ 15.000 a R$ 35.000 em leis de incentivo.

**Independent Test**: Pode ser testado disparando a geração do dossiê fiscal e do relatório de impacto para um ciclo encerrado, verificando o cálculo correto das curvas de desenvolvimento (Autonomia, Convivência e Participação) e conformidade dos carimbos de data/hora.

**Acceptance Scenarios**:

1. **Given** dados consolidados de presença e evolução socioemocional ao longo do semestre, **When** o gestor solicita o Dossiê para Prestação de Contas Fiscal, **Then** o sistema emite um documento estruturado contendo taxa de permanência, carga horária ministrada por turma e curvas evolutivas consolidadas por coorte.
2. **Given** a necessidade de prestação de contas a um patrocinador corporativo, **When** o captador seleciona o programa apoiado, **Then** o sistema gera em PDF um relatório executivo de 2 páginas ("Impacto do Seu Investimento") pronto para envio.
3. **Given** o encerramento do ciclo letivo, **When** a coordenação aprova a consolidação anual, **Then** os dados agregados e infográficos formatados ficam disponíveis para incorporação na página pública institucional em menos de 24 horas.

---

### User Story 5 - Canais Opcionais Segregados de Escuta e Fila de Triagem Humana (Priority: P5)

Como Coordenadora de Projetos, desejo gerenciar uma fila restrita de triagem para mensagens facultativas de áudio/texto enviadas por responsáveis e observações pedagógicas de oficineiros, para que nenhuma manifestação livre chegue a dashboards ou relatórios sem prévia moderação humana e classificação estritamente pedagógica não clínica.

**Why this priority**: Fornece um canal seguro de escuta para famílias e educadores enquanto constrói uma salvaguarda inquebrável contra vazamento de dados sensíveis ou situações que demandem encaminhamento externo.

**Independent Test**: Pode ser testado submetendo uma mensagem fictícia de teste por um responsável, verificando que ela entra no status "recebido" em base isolada e só tem sua categoria pedagógica agregada após aprovação explícita da coordenação.

**Acceptance Scenarios**:

1. **Given** uma mensagem opcional de texto ou gravação de voz enviada por um responsável familiar cadastrado, **When** a mensagem é recebida pelo sistema, **Then** ela é gravada em área isolada restrita com status `recebido`, inacessível a voluntários, doadores ou painéis analíticos.
2. **Given** a fila de triagem da coordenação, **When** a coordenadora avalia uma submissão, **Then** ela pode categorizar pedagogicamente (`aproveitado como categoria não clínica`), descartar (`descartado`) ou retirar do fluxo analítico para encaminhamento via rede pública de proteção (`encaminhado por protocolo institucional externo`).
3. **Given** qualquer gráfico, painel público ou relatório de impacto, **When** o sistema renderiza os dados, **Then** nenhuma transcrição, áudio bruto ou texto literal é exibido.

---

### Edge Cases

- **Voluntário sem sinal móvel (Sem Internet)**: O sistema salva a lista de presença e notas localmente no dispositivo (offline) e efetua o flush imediato para a base assim que a conexão for reestabelecida.
- **Relato de Responsável com Conteúdo de Violação de Direitos ou Saúde Mental**: Na triagem humana, a mensagem é imediatamente marcada como "encaminhado por protocolo institucional externo", expurgada do fluxo analítico e conduzida pelo protocolo social/conselho tutelar fora do software.
- **Participante presente em múltiplas oficinas no mesmo dia**: As presenças e observações de cada programa são atribuídas de forma independente ao ID pseudonimizado (Golden Record), permitindo análises comparativas sem sobreposição de registros.
- **Falta de lançamento no sábado (D0)**: O Painel de Pendências destaca a turma com alerta de pendência para que a coordenação acione o educador sem necessidade de conferência manual de planilhas.
- **Tentativa de cruzamento de dados civis com dados analíticos**: Acesso aos dados civis é blindado por controle de perfil restrito; analistas e comitês só têm acesso ao ID pseudonimizado.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001 (MDM)**: O sistema DEVE atribuir um identificador pseudonimizado único e imutável (ex: EBZ-026) a cada participante e manter os dados civis de identificação pessoal em base fisicamente segregada e protegida.
- **FR-002 (Presença e Indicadores)**: O sistema DEVE fornecer interface mobile-first com suporte offline para realização de chamada e avaliação de 3 indicadores socioemocionais (Autonomia, Convivência em Grupo e Participação Ativa).
- **FR-003 (Escalas Fechadas)**: O formulário operacional de campo DEVE utilizar exclusivamente seletores binários de presença e escalas avaliativas fechadas e padronizadas, sem campos de texto livre ou áudio no fluxo padrão de lançamento.
- **FR-004 (Vivência Terapêutica)**: O sistema DEVE disponibilizar módulo restrito para a profissional de psicologia registrando exclusivamente metadados agregados da sessão (data, duração em minutos, total de participantes presentes e tópicos pedagógicos trabalhados em lista fechada), vedando qualquer inserção de prontuário clínico individual.
- **FR-005 (Painel de Pendências D0)**: O sistema DEVE calcular e exibir em tempo real o status de submissão das oficinas, identificando em 1 clique quais turmas ainda não enviaram registros no dia do encontro.
- **FR-006 (Curvas Longitudinais)**: O sistema DEVE calcular a evolução longitudinal agregada dos participantes por programa e coorte nos 3 eixos socioemocionais (Autonomia, Convivência e Participação).
- **FR-007 (Dossiê Fiscal)**: O sistema DEVE exportar sob demanda o caderno de evidências para prestação de contas fiscais (Lei Rouanet e Lucro Real), contendo data e hora dos registros, taxas de permanência, carga horária executada e síntese de impacto.
- **FR-008 (Donor Success)**: O sistema DEVE gerar relatório executivo sintetizado em PDF de 2 páginas ("Impacto do Seu Investimento") customizável por ciclo e programa apoiado.
- **FR-009 (Alimentação da Transparência)**: O sistema DEVE exportar e disponibilizar dados consolidados, infográficos e séries históricas sem dados nominais para atualização da página pública institucional.
- **FR-010 (Canal Opcional de Responsáveis)**: O sistema DEVE permitir a recepção facultativa de relatos de responsáveis em canal segregado, registrando vínculo de consentimento e mantendo os registros isolados das bases analíticas.
- **FR-011 (Canal Opcional de Oficineiros)**: O sistema DEVE disponibilizar opção pontual para gravação de observação pedagógica por áudio ao término da oficina, fora do fluxo obrigatório de 3 minutos e sem conexão automática com os indicadores.
- **FR-012 (Fila de Triagem Segregada)**: O sistema DEVE fornecer interface privada de moderação para a coordenação gerenciar as submissões livres pelos estados: `recebido` → `em triagem` → `aproveitado como categoria não clínica` / `descartado` / `encaminhado por protocolo institucional externo`.
- **FR-013 (Controle de Acesso Baseado em Papéis - RBAC)**: O sistema DEVE segregar permissões entre Voluntário de Campo, Psicóloga, Coordenadora de Projetos, Diretoria/Captação e Administrador.
- **FR-014 (Trilha de Auditoria e Descarte)**: O sistema DEVE registrar trilhas de auditoria para operações de cadastro, alteração e acesso a dados sensíveis, além de permitir o expurgo seguro de mídias temporárias.

### Key Entities *(include if feature involves data)*

- **Participante (Golden Record)**: Identificador pseudonimizado único (código alfanumérico ex: EBZ-026), coorte/ano de ingresso, programas ativos com matrícula (Laboratório de Sonhos, Reforço Escolar, Primeira Infância, Vivências), status de matrícula.
- **Identidade Civil Protegida**: Chave de vinculação ao ID pseudonimizado, nome civil completo da criança, filiação/responsável, data de nascimento, endereço, contatos e autorizações de imagem/consentimento LGPD. Mantida em base segregada com acesso restrito.
- **Programa / Oficina**: Identificador da oficina, nome do programa, horário e dia de realização, educador voluntário responsável, público-alvo e faixa etária.
- **Encontro Operacional**: Identificador do encontro, programa/oficina correspondente, data, voluntário que realizou a chamada, carimbo temporal de envio, status de lançamento (D0 vs. atrasado).
- **Registro de Presença e Avaliação**: Identificador do registro, encontro correspondente, ID pseudonimizado do participante, presença (presente/ausente), nota de Autonomia (escala 1 a 5), nota de Convivência em Grupo (escala 1 a 5), nota de Participação Ativa (escala 1 a 5).
- **Registro de Vivência Terapêutica**: Identificador da sessão, data, psicóloga responsável, duração em minutos, quantidade total agregada de participantes presentes, tópicos pedagógicos/socioeducativos abordados (seleção fechada).
- **Entrada de Feedback Restrita**: Identificador de submissão, ID pseudonimizado do participante, origem (responsável familiar ou oficineiro), tipo de mídia (texto ou áudio), data de envio, status de triagem (`recebido`, `em triagem`, `categorizado`, `descartado`, `protocolo_externo`), caminho seguro do arquivo.
- **Síntese Pedagógica Aprovada**: Identificador da síntese, referência à entrada de feedback, categoria pedagógica fechada atribuída, período letivo, programa relacionado, carimbo temporal e ID da coordenadora que realizou a aprovação.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001 (Performance de Coleta em Campo)**: Tempo total de preenchimento da chamada e avaliação dos 3 indicadores para uma turma de até 15 participantes inferior a 3 minutos por encontro.
- **SC-002 (Taxa de Registro em D0)**: Pelo menos 80% dos encontros no piloto e mais de 90% dos encontros em regime regular registrados no mesmo dia de realização (D0).
- **SC-003 (Cobertura Socioemocional)**: Pelo menos 85% dos participantes frequentes com ciclo avaliativo completo de indicadores ao longo do período letivo.
- **SC-004 (Eficiência Operacional da Coordenação)**: Tempo gasto pela coordenação com acompanhamento de pendências e saneamento de dados reduzido para menos de 1 hora semanal (economia de mais de 80% em relação ao baseline de 15 horas mensais).
- **SC-005 (Blindagem Ética Absoluta)**: Zero registros de prontuários clínicos, diagnósticos ou anotações psicológicas confidenciais no sistema; zero exibição de áudios brutos ou transcrições livres em painéis ou relatórios institucionais.
- **SC-006 (Garantia de Triagem)**: 100% dos relatos livres ou observações opcionais submetidos à moderação humana antes de qualquer agregação ou uso analítico.
- **SC-007 (Agilidade de Prestação de Contas)**: Emissão do Relatório Anual de Transparência e Dossiê Técnico de Prestação de Contas em menos de 24 horas após o fechamento do ciclo letivo.
- **SC-008 (Custo de Licença Zero)**: Custo total de licenças de software de terceiros igual a R$ 0,00, operando integralmente sobre planos não onerosos de impacto social.

## Assumptions

- O ambiente de testes e validação acadêmica do projeto (MBA Inteli) utilizará dados 100% sintéticos e pseudonimizados, respeitando as normas éticas e de proteção à criança e ao adolescente.
- As rubricas de avaliação socioemocional adotam critérios observáveis claros de 1 a 5 para Autonomia, Convivência em Grupo e Participação Ativa, previamente pactuadas entre a coordenação pedagógica e os voluntários.
- A sincronização offline utiliza o cache local do navegador/aplicativo e efetua a transmissão de dados tão logo a conectividade à internet seja restabelecida.
- A triagem de eventuais situações de vulnerabilidade ou violação de direitos reportadas nos canais facultativos segue os fluxos protocolares físicos da assistência social e conselho tutelar do município de São Paulo (Jardim Ângela).
