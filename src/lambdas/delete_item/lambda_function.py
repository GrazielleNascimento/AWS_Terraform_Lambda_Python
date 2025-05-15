"""
Função Lambda para excluir um item da lista de mercado.

Esta função permite remover um item existente na lista,
identificado por sua chave composta no DynamoDB.
"""
import json
import os

import boto3

# Inicializar cliente DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("DYNAMODB_TABLE_NAME", "MarketList"))


def lambda_handler(event, context):
    """
    Manipulador da função Lambda para excluir item.

    :param event: Evento contendo listId e itemId
    :param context: Contexto de execução da Lambda
    :return: Resposta com status 200 e confirmação da exclusão
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

        if not list_id or not item_id:
            return {
                "statusCode": 400,
                "body": "Parâmetros obrigatórios: listId e itemId",
            }

        # Formar a chave composta
        pk = f"LIST#{list_id}"
        sk = f"ITEM#{item_id}"

        # Verificar se o item existe
        response = table.get_item(Key={"PK": pk, "SK": sk})

        item_exists = "Item" in response

        # Excluir o item
        if item_exists:
            response = table.delete_item(
                Key={"PK": pk, "SK": sk}, ReturnValues="ALL_OLD"
            )

            deleted_item = response.get("Attributes", {})

            return {
                "statusCode": 200,
                "body": {
                    "message": "Item removido com sucesso.",
                    "deleted": True,
                    "item": deleted_item,
                },
            }
        else:
            return {
                "statusCode": 200,
                "body": {
                    "message": "O item não foi encontrado ou já foi removido.",
                    "deleted": False,
                },
            }

    except Exception as e:
        if context:
            context.log(f"Error: {str(e)}")
        return {"statusCode": 500, "body": f"Error deleting item: {str(e)}"}
