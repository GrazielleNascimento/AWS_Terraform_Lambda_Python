import pytest
import json
from lambdas.get_item.lambda_function import lambda_handler

def test_get_items_success(monkeypatch):
    class FakeTable:
        def query(self, KeyConditionExpression):
            return {
                "Items": [
                    {
                        "SK": "ITEM#123",
                        "name": "Arroz",
                        "status": "TODO",
                        "createdAt": "2025-05-26T12:00:00"
                    }
                ]
            }

    # Substituir a tabela real pela tabela simulada
    monkeypatch.setattr("lambdas.get_item.lambda_function.table", FakeTable())

    # Simular o evento de entrada
    event = {
        "queryStringParameters": {
            "date": "2025-05-26"
        }
    }

    result = lambda_handler(event, None)

    assert result["statusCode"] == 200

    body = json.loads(result["body"])
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["id"] == "123"
    assert body[0]["name"] == "Arroz"
    assert body[0]["status"] == "TODO"
    assert body[0]["createdAt"] == "2025-05-26T12:00:00"


# Testar se a lista está vazia
def test_get_items_not_found(monkeypatch):
    class FakeTable:
        def query(self, KeyConditionExpression):
            return {"Items": []}

    monkeypatch.setattr("lambdas.get_item.lambda_function.table", FakeTable())

    event = {
        "queryStringParameters": {
            "date": "2025-05-27"
        }
    }

    result = lambda_handler(event, None)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert isinstance(body, list)
    assert len(body) == 0  
    


# Teste para verificar se o erro é retornado quando há falha na consulta ao DynamoDB
def test_get_items_dynamodb_failure(monkeypatch):
    class FakeTable:
        def query(self, KeyConditionExpression):
            raise Exception("Erro no banco")

    monkeypatch.setattr("lambdas.get_item.lambda_function.table", FakeTable())

    event = {
        "queryStringParameters": {
            "date": "2025-05-27"
        }
    }

    result = lambda_handler(event, None)
    assert result["statusCode"] == 500
    assert "Erro ao buscar itens" in result["body"]
