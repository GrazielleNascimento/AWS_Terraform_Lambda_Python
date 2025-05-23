"""
Função Lambda para atualizar um item da lista de mercado.

Esta função permite alterar o nome e/ou o status (TODO para DONE) de um item
existente na lista, identificado por sua chave composta no DynamoDB.
"""

import json
import os

import boto3
from boto3.dynamodb.conditions import Key

# Inicializar cliente DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("DYNAMODB_TABLE_NAME", "MarketList"))


def lambda_handler(event, context):
    """
    Manipulador da função Lambda para atualizar item.

    :param event: Evento contendo listId, itemId e updates (mudanças a aplicar)
    :param context: Contexto de execução da Lambda
    :return: Resposta com status 200 e o item atualizado
    """
    try:
        # Extrair valores do evento
        body = event

        if not isinstance(body, dict):
            body = (
                json.loads(event.get("body", "{}")) if isinstance(event, dict) else {}
            )

        list_id = body.get("listId")
        item_id = body.get("itemId")
        updates = body.get("updates", {})

        if not list_id or not item_id or not updates:
            return {
                "statusCode": 400,
                "body": "Parâmetros obrigatórios: listId, itemId e updates",
            }

        # Verificar se o item existe
        pk = f"LIST#{list_id}"
        sk = f"ITEM#{item_id}"

        response = table.get_item(Key={"PK": pk, "SK": sk})

        if "Item" not in response:
            return {"statusCode": 404, "body": "Item não encontrado"}

        # Construir expressão de atualização
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}

        for i, (key, value) in enumerate(updates.items()):
            placeholder = f":val{i}"
            attr_name = f"#attr{i}"

            update_expression += f"{attr_name} = {placeholder}, "
            expression_attribute_values[placeholder] = value
            expression_attribute_names[attr_name] = key

        # Remover vírgula e espaço finais
        update_expression = update_expression[:-2]

        # Atualizar o item
        response = table.update_item(
            Key={"PK": pk, "SK": sk},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="ALL_NEW",
        )

        # Retornar o item atualizado
        return {"statusCode": 200, "body": response.get("Attributes", {})}

    except Exception as e:
        if context:
            context.log(f"Error: {str(e)}")
        return {"statusCode": 500, "body": f"Error updating item: {str(e)}"}
