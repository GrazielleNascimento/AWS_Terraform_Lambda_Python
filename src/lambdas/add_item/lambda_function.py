"""
Função Lambda para adicionar um item à lista de mercado.

Esta função recebe um nome e uma data, cria um novo item
e o salva no DynamoDB usando o padrão Single Table Design.
"""
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

    :param event: Evento contendo name e date
    :param context: Contexto de execução da Lambda
    :return: Resposta com status 201 e o item criado
    """
    try:
        # Extrair valores do evento
        body = event

        if not isinstance(body, dict):
            body = (
                json.loads(event.get("body", "{}")) if isinstance(event, dict) else {}
            )

        name = body.get("name")
        date = body.get("date")

        if not name or not date:
            return {"statusCode": 400, "body": "Parâmetros obrigatórios: name e date"}

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

        # Preparar resposta
        return {"statusCode": 201, "body": item}

    except Exception as e:
        if context:
            context.log(f"Error: {str(e)}")
        return {"statusCode": 500, "body": f"Error creating item: {str(e)}"}
