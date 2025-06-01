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
    monkeypatch.setattr("lambdas.get_item.lambda_function.TABLE", FakeTable())

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

    monkeypatch.setattr("lambdas.get_item.lambda_function.TABLE", FakeTable())

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
    

# Teste para listar todos os itens (sem filtro de data)
def test_get_all_items(monkeypatch):
    class FakeTable:
        def scan(self, FilterExpression):
            return {
                "Items": [
                    {
                        "PK": "LIST#20250520",
                        "SK": "ITEM#123",
                        "name": "Arroz",
                        "status": "TODO",
                        "createdAt": "2025-05-20T12:00:00"
                    },
                    {
                        "PK": "LIST#20250625",
                        "SK": "ITEM#456",
                        "name": "Leite",
                        "status": "TODO",
                        "createdAt": "2025-06-25T14:00:00"
                    }
                ]
            }

    monkeypatch.setattr("lambdas.get_item.lambda_function.TABLE", FakeTable())

    # Evento sem queryStringParameters (listar todos)
    event = {}

    result = lambda_handler(event, None)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert isinstance(body, list)
    assert len(body) == 2
    assert body[0]["name"] == "Arroz"
    assert body[1]["name"] == "Leite"


# Teste com queryStringParameters vazio
def test_get_all_items_empty_params(monkeypatch):
    class FakeTable:
        def scan(self, FilterExpression):
            return {
                "Items": [
                    {
                        "PK": "LIST#20250520",
                        "SK": "ITEM#789",
                        "name": "Pão",
                        "status": "TODO",
                        "createdAt": "2025-05-20T08:00:00"
                    }
                ]
            }

    monkeypatch.setattr("lambdas.get_item.lambda_function.TABLE", FakeTable())

    event = {
        "queryStringParameters": {}  # Parâmetros vazios
    }

    result = lambda_handler(event, None)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert len(body) == 1
    assert body[0]["name"] == "Pão"


# Teste para verificar se o erro é retornado quando há falha na consulta ao DynamoDB
def test_get_items_dynamodb_failure(monkeypatch):
    class FakeTable:
        def query(self, KeyConditionExpression):
            raise Exception("Erro no banco")

    monkeypatch.setattr("lambdas.get_item.lambda_function.TABLE", FakeTable())

    event = {
        "queryStringParameters": {
            "date": "2025-05-27"
        }
    }

    result = lambda_handler(event, None)
    assert result["statusCode"] == 500
    assert "Erro ao buscar itens" in result["body"]


def test_get_items_with_hyphen_date(monkeypatch):
    # Variável para capturar o argumento da query
    query_args = {}
    
    class FakeTable:
        def query(self, **kwargs):
            # Salvar os argumentos para verificação posterior
            nonlocal query_args
            query_args = kwargs
            return {
                "Items": [
                    {
                        "SK": "ITEM#999",
                        "name": "Feijão",
                        "status": "TODO",
                        "createdAt": "2025-05-26T10:00:00"
                    }
                ]
            }

    monkeypatch.setattr("lambdas.get_item.lambda_function.TABLE", FakeTable())

    event = {
        "queryStringParameters": {
            "date": "2025-05-26"  # Com hífens
        }
    }

    result = lambda_handler(event, None)

    # Verificações
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert len(body) == 1
    assert body[0]["name"] == "Feijão"
    assert body[0]["id"] == "999"