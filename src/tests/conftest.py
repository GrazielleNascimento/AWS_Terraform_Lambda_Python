import pytest
import os
from unittest.mock import patch

# Configurar nome da tabela fake
os.environ["DYNAMODB_TABLE_NAME"] = "test_table"


@pytest.fixture
def valid_event():
    return {
        "body": '{"name": "Macarrão", "date": "2025-07-01"}'
    }


@pytest.fixture
def event_missing_params():
    return {
        "body": '{"name": "Falta data"}'
    }


@pytest.fixture
def invalid_json_event():
    return {
        "body": "not-a-json"
    }


@pytest.fixture(autouse=True)
def mock_dynamodb_table():
    with patch("lambdas.add_item.lambda_function.table") as mock_table:
        yield mock_table
