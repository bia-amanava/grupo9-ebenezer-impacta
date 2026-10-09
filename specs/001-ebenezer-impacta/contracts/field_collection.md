# Interface Contract: Coleta de Campo do Voluntário (AppSheet / API)

**ID**: `CONTRACT-COL-001`
**Finalidade**: Submissão em lote de chamada de presença e notas dos 3 indicadores socioemocionais para uma oficina.

## Schema de Requisição de Submissão

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SubmissaoChamadaOficina",
  "type": "object",
  "required": [
    "encontro_id",
    "programa_id",
    "data_encontro",
    "educador_id",
    "avaliacoes"
  ],
  "properties": {
    "encontro_id": {
      "type": "string",
      "description": "Identificador do encontro ou gerado localmente em modo offline"
    },
    "programa_id": {
      "type": "string",
      "enum": ["PROG-SONHOS", "PROG-REFORCO", "PROG-INFANCIA", "PROG-VIVENCIAS"]
    },
    "data_encontro": {
      "type": "string",
      "format": "date"
    },
    "educador_id": {
      "type": "string"
    },
    "tempo_preenchimento_segundos": {
      "type": "integer",
      "description": "Telemetria de usabilidade para validar o teto de 180 segundos (<3 min)"
    },
    "avaliacoes": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["participant_id", "presenca"],
        "properties": {
          "participant_id": {
            "type": "string",
            "pattern": "^EBZ-[0-9]{3,}$"
          },
          "presenca": {
            "type": "boolean"
          },
          "score_autonomia": {
            "type": ["integer", "null"],
            "minimum": 1,
            "maximum": 5
          },
          "score_convivencia": {
            "type": ["integer", "null"],
            "minimum": 1,
            "maximum": 5
          },
          "score_participacao": {
            "type": ["integer", "null"],
            "minimum": 1,
            "maximum": 5
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

## Regras de Blindagem (Gate de Validação)
- Se `presenca == false`, os scores devem ser `null`.
- Se `presenca == true`, os 3 scores são obrigatórios com valores inteiros de 1 a 5.
- Campos adicionais (como texto livre, observações narrativas ou áudios) são expressamente rejeitados (`additionalProperties: false`).
