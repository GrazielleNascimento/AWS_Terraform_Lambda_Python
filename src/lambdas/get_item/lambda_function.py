import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("DYNAMODB_TABLE_NAME", "MarketList"))

def lambda_handler(event, context):
    """
    Listar os itens da lista de mercado.
    """
    try:
        query_params = event.get("queryStringParameters") or {}
        date = query_params.get("date")

        if not date:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Parâmetro obrigatório: date"}),
                "headers": {"Content-Type": "application/json"}
            }
        
        pk = f"LIST#{date.replace('-', '')}"

        # Consultar DynamoDB
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("PK").eq(pk)
        )

        items = response.get("Items", [])

        # Estrutura para o consumidor final
        items_formatados = [
            {
                "id": item["SK"].replace("ITEM#", ""),
                "name": item.get("name"),
                "status": item.get("status"),
                "createdAt": item.get("createdAt")
            }
            for item in items
        ]

        return {
            "statusCode": 200,
            "body": json.dumps(items_formatados),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        if context:
            context.log(f"Erro ao buscar itens: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Erro ao buscar itens: {str(e)}"}),
            "headers": {"Content-Type": "application/json"}
        }
