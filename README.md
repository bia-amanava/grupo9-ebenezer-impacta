# Ebenézer Impacta (v2.0)

> **Plataforma de Acompanhamento Ético de Trajetórias em Oficinas Socioeducativas e Prestação de Contas Agregada**  
> *Instituto Social Ebenézer • Jardim Ângela (São Paulo)*  
> *MBA em IA & Dados para Negócios (Inteli) — Módulo 3 (PRD v2.0 revisado)*

---

## 1. Visão Geral e Fronteiras do Produto

O **Instituto Social Ebenézer** atua no Jardim Ângela oferecendo oficinas socioeducativas e apoio psicossocial para crianças, adolescentes e suas famílias. Historicamente, os registros limitavam-se a listas manuais de chamada e notas escolares anuais. Não havia série longitudinal de observações pedagógicas que permitisse responder com evidências verificáveis "o que mudou na participação e na convivência das crianças?".

O **Ebenézer Impacta** transforma registros rápidos e não clínicos de oficinas em **trajetórias programáticas agregadas, verificáveis e protegidas**, apoiando a gestão pedagógica e a prestação de contas do Instituto sem jamais expor a vida clínica das crianças.

> **Importante (Alinhamento PRD v2.0):** Retenção de doadores, captação por incentivos fiscais e custo zero de licenças são **hipóteses de benefício** a serem comprovadas, não promessas do software. O produto entrega dados de execução e observação pedagógica agregados; não demonstra impacto causal.

---

## 2. Princípios Inegociáveis (A Constituição da Solução)

1. **Melhor Interesse da Criança:** Prevalece sobre qualquer métrica, relatório ou meta de captação.
2. **Minimização:** Coleta estritamente restrita ao que possui finalidade documentada no dicionário de dados.
3. **Fronteira Clínica:** Nenhum dado clínico entra no sistema. O módulo de psicologia NUNCA registra prontuários, diagnósticos ou narrativas de acolhimento; apenas metadados agregados (ocorrência, duração, volume de presentes e checklist de infraestrutura).
4. **Pseudonimização ≠ Anonimização:** O ID pseudonimizado (`EBZ-###`) não torna o dado anônimo; o acesso aos dados pseudonimizados permanece restrito e controlado.
5. **Separação por Zonas Físicas de Sensibilidade:** Permissões em planilhas/arquivos expõem o arquivo todo; logo, a separação é física (arquivos e projetos apartados), em 5 zonas:
   - **Zona A (Restrita):** Dados civis identificáveis (nome completo, filiação, telefone).
   - **Zona B (Operacional):** IDs pseudonimizados, presenças e 3 indicadores em escalas fechadas (1 a 5).
   - **Zona C (Analítica):** Dados agregados com supressão mandatória de pequenas amostras ($n < 10$).
   - **Zona D (Publicada):** Arquivos estáticos imutáveis (PDFs) devidamente aprovados por humanos.
   - **Zona E (Opcional):** Relatos e gravações (fora do MVP / Portão G5).
6. **Revisão Humana Prévia:** Nenhum relatório externo é gerado direto da base viva, e é vedada a publicação de links vivos ou dinâmicos conectados à base.
7. **Afirmações com Evidência:** Rejeição explícita de valores sem base empírica (rejeitados R$ 16k/ano, R$ 15-35k e conformidade fiscal garantida). Inclusão obrigatória de seção de limitações metodológicas ("O que este relatório não afirma").
8. **Simplicidade Proporcional:** Rotina da coordenação planejada para $\le 1$ h/semana (hipótese a medir no piloto).
9. **Saída Possível:** Exportação completa em formato aberto (CSV) para assegurar portabilidade.
10. **Dados Sintéticos Obrigatórios até o Portão G2:** O ambiente opera 100% com dados sintéticos até parecer jurídico e homologação de piloto real.

---

## 3. Portões de Decisão (Decision Gates)

```
[Portão G0: Fundação] ──► [Portão G1: Piloto Sintético] ──► [Portão G2: Piloto Real] ──► [Portão G3: Expansão] ──► [Portão G4: Publicação] ──► [Portão G5: Módulo E]
```

- **G0 (Fundação):** ADR-001 a ADR-006 registrados; PoC offline validada; elegibilidade de licenças (H-03); rubricas v0; dicionário de dados v0.
- **G1 (Piloto Sintético):** Validação técnica integral com 100% dados sintéticos; teste de usabilidade; matriz de acessos; ensaio de backup/restauração.
- **G2 (Piloto Real Controlado):** Parecer jurídico formal LGPD/ECA; autorização da diretoria; política de descarte; treinamento de voluntários da turma piloto.
- **G3 (Expansão):** Metas do piloto atingidas (D0 > 80%, tempo < 4 min); calibração de rubricas.
- **G4 (Publicação Externa):** Regras de supressão ($n < 10$) aplicadas; aprovação formal da diretoria; PDF estático imutável gerado.
- **G5 (Módulo Opcional E - Escuta de Famílias e Voz):** Fora do MVP; requer parecer específico, orçamento próprio de transcrição e capacidade de triagem comprovada.

---

## 4. Estrutura do Repositório

```text
├── data/
│   ├── schemas/
│   │   └── dictionary.json          # Dicionário de dados organizado pelas Zonas A a D
│   └── synthetic/                   # Datasets sintéticos do piloto acadêmico (120+ educandos)
│       ├── mdm_participantes.json
│       ├── cadastro_civil_segregado.json
│       ├── encontros_operacionais.json
│       ├── avaliacoes_socioemocionais.json
│       └── vivencias_terapeuticas.json
├── src/
│   ├── app.py                       # Servidor web integrado FastAPI
│   ├── core/
│   │   ├── config.py                # Configurações, limiar de supressão (n < 10) e limites
│   │   ├── models.py                # Modelos Pydantic com validação bioética e Zona D
│   │   ├── mdm.py                   # Golden Record e segregação civil física
│   │   └── metrics.py               # Motor de cálculo com supressão e limitações metodológicas
│   ├── services/
│   │   ├── collection_service.py    # Serviço de chamada e escalas fechadas em campo
│   │   ├── coordination_service.py  # Serviço de monitoramento de pendências D0
│   │   ├── therapy_service.py       # Serviço restrito a metadados da psicologia (FR-020)
│   │   └── triage_service.py        # Módulo Opcional E isolado em quarentena (Portão G5)
│   ├── api/                         # Endpoints RESTful
│   └── templates/                   # Interfaces responsivas com alertas de governança
├── specs/001-ebenezer-impacta/      # Especificações alinhadas ao GitHub Spec Kit
│   ├── spec.md                      # Especificação funcional aderente ao PRD v2.0
│   ├── plan.md                      # Plano de arquitetura, ADRs e Zonas Físicas
│   ├── data-model.md                # Modelo lógico por Zonas de Sensibilidade
│   ├── quickstart.md                # Guia de validação rápida
│   ├── contracts/                   # Contratos de interfaces
│   └── tasks.md                     # Tarefas organizadas por Portões G0 a G5
└── tests/                           # Bateria de testes automatizados com pytest
```

---

## 5. Como Executar a Aplicação Localmente

### 1. Pré-requisitos
- Python 3.10 ou superior instalado.
- Instalar dependências:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Iniciar o Servidor
```bash
python -m uvicorn src.app:app --reload --port 8000
```
Acesse no seu navegador: **[http://localhost:8000](http://localhost:8000)**

### 3. Módulos Disponíveis
- **📱 Voluntário de Campo (`/campo`)**: Chamada rápida e 3 indicadores em escalas fechadas (1 a 5) com suporte a "Não observado" e modo offline.
- **📊 Coordenação Geral (`/coordenacao`)**: Painel de acompanhamento de pendências D0 para cobrança em < 1 minuto.
- **🛡️ Psicologia (`/psicologia`)**: Registro restrito de metadados agregados e checklist de infraestrutura (CFP/LGPD).
- **📥 Fila de Triagem (`/triagem`)**: Módulo Opcional E (Fora do MVP / Portão G5).
- **📜 Transparência & Captação (`/relatorios`)**: Trajetórias longitudinais com supressão de amostras pequenas ($n < 10$), caderno de evidências e limitações metodológicas explícitas.
- **📖 Tutorial & Capacitação Interativa (`/tutorial`)**: Guias passo a passo por perfil, limites bioéticos e simulação interativa da rubrica.
- **🛡️ Controle de Acessos & Governança (`/gestao-acessos`)**: Gestão de colaboradores (RBAC), controle do cadastro de crianças (Zona A civil vs. Zona B pseudonimizada) e gestão de oficinas.

---

## 6. Como Executar a Bateria de Testes Automatizados

```bash
python -m pytest
```
Os testes validam contratos de API, supressão de pequenas amostras, isolamento civil e conformidade com as fronteiras éticas do PRD v2.0.
