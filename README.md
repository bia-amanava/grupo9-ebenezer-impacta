# Ebenézer Impacta

> **Plataforma de Monitoramento Ético e Emissão do Relatório de Transparência e Captação**  
> *Instituto Social Ebenézer • Jardim Ângela (São Paulo)*  
> *MBA em IA & Dados para Negócios (Inteli) — Artefato Técnico da Semana 10 (Versão 1.1)*

---

## 1. Visão Geral e Problema Central

O **Instituto Social Ebenézer** atua no Jardim Ângela oferecendo oficinas socioeducativas e apoio psicossocial para mais de 120 crianças e suas famílias. 
Historicamente, o registro limitava-se a listas manuais de presença em papel e notas escolares anuais. Não havia acompanhamento sistemático da evolução socioemocional dos educandos, dificultando a demonstração de impacto longitudinal para mantenedores e inviabilizando captações em leis de incentivo fiscal (Lei Rouanet e empresas em Lucro Real).

O **Ebenézer Impacta** soluciona essa assimetria através de uma plataforma integrada de governança, coleta ágil em campo (<3 minutos), módulo clínico blindado sob sigilo profissional (CFP) e emissão automatizada de evidências auditáveis de impacto com **custo direto de licença zero**.

---

## 2. Pilares Constitucionais da Solução

1. **Blindagem Ética e Conformidade (LGPD, ECA e CFP)**:
   - Segregação rigorosa entre registros pedagógicos e prontuários clínicos.
   - O módulo de psicologia NUNCA armazena prontuários ou diagnósticos individuais, registrando unicamente metadados agregados (duração em minutos, volume total de presentes e tópicos socioeducativos em taxonomia fechada).
   - Base de dados civis fisicamente apartada do banco analítico; educandos identificados unicamente por códigos alfanuméricos pseudonimizados (Golden Record `EBZ-xxx`).
   - Escalas fechadas (1 a 5) nos indicadores de Autonomia, Convivência em Grupo e Participação Ativa, impedindo a criação de rótulos estigmatizantes.
2. **Custo de Licença Zero Garantido (RNF-01)**:
   - 100% suportado no ecossistema sem fins lucrativos: **Google Workspace for Nonprofits**, **AppSheet Free Tier/Core** e **Looker Studio**.
   - Tempo operacional semanal da coordenação reduzido para menos de 1 hora ("Painel de Pendências D0").
3. **Interface Mobile-First de Baixo Atrito (< 3 minutos)**:
   - Voluntário de sábado completa a chamada e a avaliação de 3 indicadores de 15 alunos pelo celular em menos de 180 segundos.
   - Suporte nativo a operação offline com sincronização automática (*flush*).
4. **Evidências Auditáveis e Captação**:
   - Curvas longitudinais de evolução socioemocional por coorte e programa.
   - Geração sob demanda do Caderno de Evidências Fiscais (Lei Rouanet e Lucro Real).
   - Relatório Executivo sintetizado de 2 páginas (*Donor Success* / "Impacto do Seu Investimento") para retenção de doadores (mitigando perda de receita estimada em R$ 16.000,00/ano).
5. **Canais Opcionais Segregados e Moderação Humana (RF-05, RF-06 e RF-07)**:
   - Mensagens facultativas de famílias e oficineiros ficam em quarentena isolada.
   - Triagem humana obrigatória: `RECEBIDO` → `EM_TRIAGEM` → [`APROVEITADO` | `DESCARTADO` | `PROTOCOLO_EXTERNO`].
   - Conteúdo sensível é expurgado do fluxo analítico e encaminhado à rede de assistência social externa.

---

## 3. Estrutura do Repositório

```text
├── data/
│   ├── schemas/
│   │   └── dictionary.json          # Dicionário de dados e esquemas para Google Sheets / AppSheet
│   └── synthetic/                   # Datasets sintéticos do MVP acadêmico (130 educandos, 10 semanas)
│       ├── mdm_participantes.json
│       ├── cadastro_civil_segregado.json
│       ├── encontros_operacionais.json
│       ├── avaliacoes_socioemocionais.json
│       └── vivencias_terapeuticas.json
├── src/
│   ├── app.py                       # Servidor web integrado FastAPI
│   ├── core/
│   │   ├── config.py                # Configurações e limites constitucionais
│   │   ├── models.py                # Modelos de dados e validações Pydantic
│   │   ├── mdm.py                   # Master Data Management (Golden Record & segregação civil)
│   │   └── metrics.py               # Motor de cálculo de curvas longitudinais e dossiê fiscal
│   ├── services/
│   │   ├── collection_service.py    # Serviço de coleta de campo do voluntário
│   │   ├── coordination_service.py  # Serviço de pendências D0 da gestão
│   │   ├── therapy_service.py       # Serviço operacional blindado da psicologia
│   │   └── triage_service.py        # Serviço de triagem e moderação em quarentena
│   ├── api/                         # Endpoints RESTful dos módulos
│   └── templates/                   # Interfaces responsivas (HTML5 + Tailwind CSS):
│       ├── campo_voluntario.html    # Interface mobile de campo (<3 min)
│       ├── coordenacao_d0.html      # Painel de pendências e saneamento D0
│       ├── vivencia_psicologia.html # Módulo blindado de vivência terapêutica
│       ├── triagem_escuta.html      # Fila privada de moderação de áudio/texto
│       └── relatorios_captacao.html # Emissão de relatórios e dossiê Rouanet
├── specs/001-ebenezer-impacta/      # Especificações completas geradas via GitHub Spec Kit
│   ├── spec.md                      # Requisitos de produto e personas
│   ├── plan.md                      # Plano de arquitetura e tecnologia
│   ├── data-model.md                # Modelo lógico de entidades
│   ├── quickstart.md                # Guia de validação rápida
│   ├── contracts/                   # Contratos formais de interface
│   └── tasks.md                     # Decomposição em tarefas acionáveis
└── tests/                           # Bateria de testes automatizados com pytest
```

---

## 4. Como Executar o Protótipo Interativo

### 1. Pré-requisitos
- Python 3.10 ou superior instalado.
- Instalar dependências:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Iniciar a Aplicação Localmente
```bash
python -m uvicorn src.app:app --reload --port 8000
```
Acesse no seu navegador: **[http://localhost:8000](http://localhost:8000)**

### 3. Navegação pelos Módulos
- **📱 Voluntário de Campo (`/campo`)**: Simule a realização da chamada e pontuação dos 3 indicadores observáveis em menos de 3 minutos, com cronômetro em tempo real e teste de modo offline.
- **📊 Coordenação Geral (`/coordenacao`)**: Visualize o status dos lançamentos do sábado em tempo real, pendências e acionamento de cobrança em 1 clique.
- **🛡️ Psicologia (`/psicologia`)**: Registre sessões de acolhimento sob estrita blindagem bioética (sem prontuários ou diagnósticos individuais).
- **📥 Fila de Triagem (`/triagem`)**: Gerencie a moderação humana dos relatos facultativos de familiares e educadores.
- **📜 Transparência & Captação (`/relatorios`)**: Analise as trajetórias longitudinais semana a semana, gere o Dossiê para a Lei Rouanet e o resumo de 2 páginas *Donor Success*.

---

## 5. Como Executar a Bateria de Testes Automatizados

Para validar contratos, limites de tempo, cálculos matemáticos e regras de conformidade:
```bash
python -m pytest
```

---

## 6. Conformidade e Aprovação Técnica

- **Ambiente de Demonstração Acadêmica**: Opera estritamente com **dados sintéticos** e simulações fictícias de áudio/texto, garantindo 0% de exposição de crianças reais.
- **Ingresso em Produção Real**: O uso em ambiente de produção com dados reais está condicionado a parecer jurídico prévio, termo de consentimento dos responsáveis com base na LGPD e formalização da política de retenção e descarte pela diretoria institucional.
