import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from lambdas.add_item.lambda_function import lambda_handler

def test_add_item_success(mock_dynamodb_table, valid_event):
    
    mock_dynamodb_table.put_item.return_value = {}

    response = lambda_handler(valid_event, {})

    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert body["name"] == "Macarrão"
    assert body["PK"].startswith("LIST#20250701")
    assert body["SK"].startswith("ITEM#")
    assert body["status"] == "TODO"
    assert "createdAt" in body


def test_add_item_missing_parameters(mock_dynamodb_table, event_missing_params):
    response = lambda_handler(event_missing_params, {})

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "Parâmetros obrigatórios" in body["message"]


def test_add_item_invalid_json(mock_dynamodb_table, invalid_json_event):
    response = lambda_handler(invalid_json_event, {})

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "Erro interno" in body["message"]


def test_add_item_dynamodb_failure(mock_dynamodb_table, valid_event):
    mock_dynamodb_table.put_item.side_effect = Exception("Simulated DynamoDB failure")

    response = lambda_handler(valid_event, {})

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "Simulated DynamoDB failure" in body["message"]
