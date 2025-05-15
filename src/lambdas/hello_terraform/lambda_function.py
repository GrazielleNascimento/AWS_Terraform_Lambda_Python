"""
Função Lambda que retorna uma mensagem 'Hello Terraform'.

Esta função é um exemplo simples que retorna um objeto JSON
com status code 200 e a mensagem "Hello Terraform".
"""


def lambda_handler(event, context):
    """
    Manipulador da função Lambda.

    :param event: Evento que acionou a função
    :param context: Contexto de execução da Lambda
    :return: Resposta com status 200 e mensagem "Hello Terraform"
    """
    return {"statusCode": 200, "body": "Hello Terraform"}
