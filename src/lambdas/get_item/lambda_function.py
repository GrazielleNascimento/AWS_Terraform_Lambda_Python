import json
import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("DYNAMODB_TABLE_NAME", "MarketList"))

def lambda_handler(event, context):
    try:
        query_params = event.get("queryStringParameters") or {}
        date = query_params.get("date")

        
        pk = f"LIST#{date}"
        print(f"🔍 Buscando itens com PK: {pk}")

        
        response = table.query(
             KeyConditionExpression=Key("PK").eq(pk)
        )
       
        items = response.get("Items", [])
        print(f"📄 Itens encontrados: {json.dumps(items, indent=2)}")
        

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