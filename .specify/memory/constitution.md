<!--
Sync Impact Report:
- Version change: none -> 1.0.0
- List of modified principles:
  - Initial ratification of Core Principles:
    - I. Blindagem Ética, Privacidade e Não Estigmatização (LGPD / ECA / CFP)
    - II. Custo de Licença Zero e Sustentabilidade Operacional
    - III. Interface Mobile-First de Baixo Atrito e Coleta Ágil (< 3 min)
    - IV. Evidências Auditáveis, Impacto Longitudinal e Captação
    - V. Governança Segregada, Triagem Humana e Dados Sintéticos
- Added sections:
  - Normas de Segurança, Engenharia de Dados e Proteção de Menores
  - Protocolos de Homologação, Qualidade e MVP Acadêmico
- Removed sections: none
- Deferred items: none
-->

# Ebenézer Impacta Constitution

## Core Principles

### I. Blindagem Ética, Privacidade e Não Estigmatização (LGPD / ECA / CFP)
A proteção dos direitos e da dignidade de crianças e adolescentes é não negociável.
- **Segregação Clínica vs. Pedagógica**: O sistema NUNCA coletará, armazenará ou processará prontuários médicos ou psicológicos, diagnósticos clínicos ou narrativas íntimas. O módulo da psicologia captura exclusivamente metadados agregados (duração em minutos, volume total de presentes e tópicos pedagógicos trabalhados).
- **Golden Record Pseudonimizado**: Todos os registros analíticos devem utilizar identificadores pseudonimizados únicos (ex: EBZ-026). A tabela de dados civis identificáveis deve residir em base estritamente segregada com controle criptográfico e acesso restrito.
- **Escalas Fechadas**: Formulários operacionais de voluntários em campo operam unicamente com presença binária e escalas avaliativas fechadas e validadas, impedindo a criação de rótulos subjetivos pejorativos ou estigmatizantes.

### II. Custo de Licença Zero e Sustentabilidade Operacional
O Instituto Ebenézer opera no terceiro setor e não pode incorrer em custos recorrentes de licenças de software.
- **Ecossistema Google Workspace for Nonprofits & AppSheet Core/Free Tier**: Toda a arquitetura tecnológica deve ser implementável sem taxas de licença pagas por usuário.
- **Eficiência de Gestão**: Os rituais de saneamento e conciliação de turmas da Coordenação Geral devem exigir no máximo 1 hora de esforço operacional semanal ("Painel de Pendências D0").

### III. Interface Mobile-First de Baixo Atrito e Coleta Ágil (< 3 min)
A experiência do voluntário comunitário deve priorizar velocidade e zero atrito burocrático no término das oficinas.
- **Meta de 3 Minutos**: O registro de presença e a avaliação dos 3 indicadores socioemocionais (Autonomia, Convivência em Grupo e Participação Ativa) para uma turma de até 15 alunos deve ser concluído em menos de 3 minutos pelo celular.
- **Operação Offline e Resiliência**: O aplicativo de campo deve operar nativamente offline no aparelho do voluntário, realizando sincronização automática com a nuvem assim que a conexão de rede for restabelecida.
- **Fluxo Estruturado Livre de Narrativa**: O fluxo primário de chamada e pontuação não deve conter digitação de texto livre nem gravação de áudio.

### IV. Evidências Auditáveis, Impacto Longitudinal e Captação
A plataforma deve transformar o monitoramento rotineiro em evidências robustas de impacto social para sustentar parcerias institucionais.
- **Métricas Longitudinais**: Superar contagens volumétricas arcaicas mediante curvas evolutivas de desenvolvimento socioemocional agregadas por coorte e programa ao longo dos ciclos letivos.
- **Dossiê para Incentivos Fiscais**: Capacidade de geração de relatórios técnicos auditáveis com carimbos de data/hora, taxas de permanência e cargas horárias para prestação de contas de incentivo fiscal (Lei Rouanet e empresas em Lucro Real).
- **Donor Success**: Emissão automatizada em 1 clique do Relatório Executivo semestral ("Impacto do Seu Investimento" - 2 páginas) e geração de infográficos/gráficos para integração contínua na Página Pública de Transparência.

### V. Governança Segregada, Triagem Humana e Dados Sintéticos
A escuta ativa de famílias e oficineiros é canal complementar facultativo com barreiras rígidas de proteção.
- **Canais Opcionais Isolados**: Quaisquer mensagens de áudio ou texto de responsáveis (RF-05) ou observações de oficineiros (RF-06) devem residir em repositório físico isolado, nunca alimentando diretamente tabelas de análise, indicadores ou o Looker Studio.
- **Triagem Humana Obrigatória (RF-07)**: Nenhuma entrada qualitativa é aproveitada sem moderação humana prévia pela coordenação capacitada. O fluxo de triagem deve conter os estados: `recebido` → `em triagem` → `aproveitado como categoria não clínica` / `descartado` / `encaminhado por protocolo institucional externo`.
- **MVP Acadêmico 100% Sintético**: O ambiente de testes e demonstração acadêmica deve utilizar exclusivamente dados sintéticos e personas fictícias. É terminantemente proibido o upload ou manipulação de dados reais de menores sem parecer jurídico prévio e homologação formal.

## Normas de Segurança, Engenharia de Dados e Proteção de Menores

1. **Gestão de Identidade e Controle de Acesso (RBAC)**:
   - Permissões restritas baseadas em papéis: Voluntário (apenas registro de sua turma em D0), Psicóloga (apenas metadados agregados), Coordenação (saneamento, triagem e governança), Diretoria/Captação (relatórios e dashboards consolidados).
   - Trilhas de auditoria para registros, edições e visualizações de dados sensíveis.
2. **Ciclo de Vida e Retenção de Dados**:
   - Definição formal de prazos de retenção e rotinas automáticas de expurgo para gravações de áudio temporárias e rascunhos de transcrição.
   - Proibição de download indiscriminado de mídias brutas.

## Protocolos de Homologação, Qualidade e MVP Acadêmico

- **Test-First e Validação de Contrato**: Cada entidade de dados (MDM, Registro de Encontro, Avaliação Socioemocional, Metadados de Vivência, Fila de Triagem) deve ter esquema rígido de validação, restrições de integridade relacional e dicionário de dados formal.
- **Verificação de Usabilidade**: Simulação em campo com cronômetro para validação do teto de 3 minutos por turma.
- **Portão de Entrada em Produção**: O avanço para dados reais requer obrigatoriamente validação jurídica formal (base legal e melhor interesse do menor), teste de penetração contra vazamento de dados e anuência formal da diretoria institucional.

## Governance

- Esta Constituição prevalece sobre quaisquer decisões técnicas ou arquiteturais conflitantes no ciclo de vida do projeto Ebenézer Impacta.
- Emendas constitucionais exigem justificativa fundamentada, registro de impacto na matriz de conformidade regulatória (LGPD/ECA/CFP) e atualização de versão semântica.
- Todos os requisitos de software, especificações (`spec.md`), planos (`plan.md`) e tarefas (`tasks.md`) do Spec Kit devem ser avaliados e aprovados contra estes princípios.

**Version**: 1.0.0 | **Ratified**: 2026-10-05 | **Last Amended**: 2026-10-05
