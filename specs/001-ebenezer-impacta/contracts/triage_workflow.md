# Interface Contract: Fila de Triagem e Moderação Humana (RF-07)

**ID**: `CONTRACT-TRI-003`
**Finalidade**: Transições de estado controladas para a moderação humana de feedbacks opcionais de responsáveis e educadores.

## Schema da Ação de Moderação

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AcaoModeracaoTriagem",
  "type": "object",
  "required": [
    "feedback_id",
    "coordenador_id",
    "decisao"
  ],
  "properties": {
    "feedback_id": {
      "type": "string"
    },
    "coordenador_id": {
      "type": "string"
    },
    "decisao": {
      "type": "string",
      "enum": [
        "APROVEITADO_CATEGORIA_PEDAGOGICA",
        "DESCARTADO",
        "ENCAMINHADO_PROTOCOLO_EXTERNO"
      ]
    },
    "categoria_fechada": {
      "type": "string",
      "enum": [
        "ENGAJAMENTO_FAMILIAR_POSITIVO",
        "EVOLUCAO_DE_HABILIDADES_MANUAIS",
        "AUTONOMIA_NO_COTIDIANO",
        "INTEGRACAO_COMUNITARIA"
      ],
      "description": "Obrigatório unicamente se decisao == APROVEITADO_CATEGORIA_PEDAGOGICA"
    },
    "motivo_descarte_ou_encaminhamento": {
      "type": "string",
      "enum": [
        "CONTEUDO_FORA_DE_ESCOPO",
        "AUDIO_INAUDIVEL_OU_RUIDO",
        "VIOLACAO_DE_DIREITOS_ENCAMINHADA_EXTERNAMENTE",
        "DEMANDA_DE_SAUDE_ENCAMINHADA_A_UBS"
      ],
      "description": "Taxonomia fechada para registro de auditoria sem expor detalhes íntimos no banco analítico"
    }
  },
  "additionalProperties": false
}
```

## Regras de Governança
- Se `decisao == APROVEITADO_CATEGORIA_PEDAGOGICA`, gera registro na base analítica `SINTESE_PEDAGOGICA` contendo apenas a categoria fechada, período e programa.
- Se `decisao == ENCAMINHADO_PROTOCOLO_EXTERNO`, o registro original é retirado de qualquer indexação analítica, gerando alerta de protocolo para tratamento físico e confidencial pela equipe de assistência social do Instituto.
- Nenhum áudio bruto ou transcrição é salvo em planilhas abertas ou disponibilizado ao Looker Studio.
