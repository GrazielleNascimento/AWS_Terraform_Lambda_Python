import json
import os
import uuid
from datetime import datetime

import boto3

# Inicializar cliente DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("DYNAMODB_TABLE_NAME", "MarketList"))

def lambda_handler(event, context):
    """
    Manipulador da função Lambda para adicionar item.

    Compatível com chamadas diretas e via API Gateway HTTP/REST.

    :param event: Evento contendo os campos 'name' e 'date'
    :param context: Contexto de execução Lambda
    :return: Resposta HTTP com status e dados
    """
    try:
         # Suporte para chamadas via API Gateway
        if isinstance(event, dict) and "body" in event:
            body_raw = event.get("body", "{}")
            body = json.loads(body_raw) if isinstance(body_raw, str) else body_raw
        else:
            body = event 
        # Extrair parâmetros obrigatórios
        name = body.get("name")
        date = body.get("date")

        if not name or not date:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Parâmetros obrigatórios: name e date"})
            }

        # Gerar chaves
        pk = f"LIST#{date.replace('-', '')}"
        item_id = str(uuid.uuid4())
        sk = f"ITEM#{item_id}"
        created_at = datetime.now().isoformat()

        # Criar item
        item = {
            "PK": pk,
            "SK": sk,
            "name": name,
            "status": "TODO",
            "createdAt": created_at,
        }

        # Salvar no DynamoDB
        table.put_item(Item=item)

        # Retornar item criado
        return {
            "statusCode": 201,
            "body": json.dumps(item),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        print(f"Erro ao processar requisição: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Erro interno: {str(e)}"})
        }
