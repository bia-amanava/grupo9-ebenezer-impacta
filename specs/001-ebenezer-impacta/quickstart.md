# Quickstart & Validation Guide: Ebenézer Impacta

**Feature**: `001-ebenezer-impacta`
**Date**: 2026-10-05

Este guia descreve os passos práticos para executar e validar os 4 módulos centrais e o módulo de triagem da solução **Ebenézer Impacta**.

## Pré-requisitos
- Python 3.10+ instalado no ambiente (ou navegador moderno para visualização dos artefatos interativos).
- Dependências leves: `fastapi`, `uvicorn`, `pydantic` (ou runner de protótipo standalone).

## 1. Estrutura de Artefatos Gerados no Projeto
- `data/synthetic/`: Gerador de dados sintéticos e bases CSV/JSON prontas para importação no Google Sheets.
- `src/`: Protótipo interativo full-stack autônomo (mobile-first para voluntários, dashboard de pendências para coordenação, módulo da psicologia e fila de triagem).
- `tests/`: Bateria de testes automatizados de conformidade e integridade dos dados (validando os 5 critérios constitucionais e limites de tempo).

## 2. Cenários de Validação Ponta a Ponta

### Cenário 1: Chamada e Avaliação Mobile em Menos de 3 Minutos
1. Abrir a rota de voluntário no navegador móvel (ou simulador mobile).
2. Selecionar a turma (ex: "Laboratório de Sonhos - Turma A").
3. Marcar presença dos 15 educandos e atribuir notas (1 a 5) nos botões rápidos de Autonomia, Convivência e Participação.
4. Acionar "Submeter Chamada".
5. **Resultado Esperado**: Tempo total decorrido < 180 segundos; confirmação de submissão em D0; sincronização dos dados no armazenamento local/servidor.

### Cenário 2: Blindagem Ética do Módulo de Psicologia
1. Acessar o módulo com perfil "Psicologia".
2. Registrar uma sessão informando data, duração (90 min), quantidade de participantes (18) e temas selecionados em lista fechada.
3. Tentar submeter qualquer texto narrativo ou prontuário clínico individual.
4. **Resultado Esperado**: Rejeição programática imediata; garantia de que a base registra apenas os 4 metadados auditáveis.

### Cenário 3: Painel de Saneamento e Pendências D0 da Coordenação
1. Acessar a visão da Coordenadora de Projetos.
2. Observar a listagem em tempo real das oficinas do sábado.
3. **Resultado Esperado**: Oficinas com chamada pendente são destacadas com alerta vermelho e contato do voluntário responsável em 1 clique; indicador de tempo de saneamento semanal <= 1 hora.

### Cenário 4: Geração de Dossiês Fiscais e Relatório de Transparência
1. Acessar a aba de Captação e Transparência.
2. Clicar em "Gerar Dossiê Lei Rouanet / Lucro Real" e "Emitir Relatório de 2 Páginas - Impacto do Seu Investimento".
3. **Resultado Esperado**: Geração imediata de curvas longitudinais agregadas de evolução e demonstrativo de taxas de permanência e carga horária ministrada.

### Cenário 5: Fila de Triagem de Feedbacks Opcionais
1. Simular o envio de um áudio/texto facultativo por um responsável.
2. Abrir a Fila de Triagem da Coordenação.
3. Observar status `RECEBIDO`.
4. Executar moderação: aprovar categoria pedagógica ou acionar protocolo de encaminhamento externo.
5. **Resultado Esperado**: Nenhuma mídia bruta ou dado sensível transborda para o painel de transparência ou base de voluntários.
