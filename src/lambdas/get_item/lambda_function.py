import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "MarketList")
TABLE = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    try:
        query_params = event.get("queryStringParameters") or {}
        date = query_params.get("date")
        
        # Se tem data, buscar por data específica
        if date:
            # Remover hífens se existirem
            date_formatted = date.replace('-', '')
            pk = f"LIST#{date_formatted}"
            
            response = TABLE.query(
                KeyConditionExpression=Key("PK").eq(pk)
            )
        else:
            # Se não tem data, buscar todos os itens
            response = TABLE.scan(
                FilterExpression=Attr("PK").begins_with("LIST#")
            )
        
        items = response.get("Items", [])
        
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
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Erro ao buscar itens: {str(e)}"}),
            "headers": {"Content-Type": "application/json"}
        }