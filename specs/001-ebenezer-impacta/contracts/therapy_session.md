# Interface Contract: Módulo de Vivência Terapêutica (Psicologia)

**ID**: `CONTRACT-VIV-002`
**Finalidade**: Submissão exclusiva de metadados operacionais de sessões terapêuticas em grupo, em conformidade com o sigilo do Código de Ética Profissional do Psicólogo (CFP) e LGPD.

## Schema de Requisição

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SubmissaoVivenciaTerapeutica",
  "type": "object",
  "required": [
    "data_sessao",
    "psicologa_id",
    "duracao_minutos",
    "total_presentes_agregado",
    "topicos_pedagogicos"
  ],
  "properties": {
    "data_sessao": {
      "type": "string",
      "format": "date"
    },
    "psicologa_id": {
      "type": "string"
    },
    "duracao_minutos": {
      "type": "integer",
      "minimum": 15,
      "maximum": 240
    },
    "total_presentes_agregado": {
      "type": "integer",
      "minimum": 1,
      "description": "Contagem numérica agregada de participantes atendidos na sessão"
    },
    "topicos_pedagogicos": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string",
        "enum": [
          "AUTOCUIDADO_E_HIGIENE",
          "REGULACAO_EMOCIONAL",
          "CONVIVENCIA_E_VINCULO",
          "RESOLUCAO_PACIFICA_DE_CONFLITOS",
          "PROJETO_DE_VIDA_E_SONHOS",
          "ESCUTA_E_EXPRESSAO_DE_SENTIMENTOS"
        ]
      }
    }
  },
  "additionalProperties": false
}
```

## Regras de Blindagem (Gate Ético e Legal)
- NENHUM campo nominal ou identificador individual de aluno pode ser aceito.
- NENHUM campo de anotação de prontuário, diagnóstico, descrição clínica ou texto aberto é permitido (`additionalProperties: false`).
- Apenas valores da taxonomia fechada pré-aprovada são aceitos para `topicos_pedagogicos`.
