"""
Script para empacotar funções Lambda para implantação.

Este script cria pacotes ZIP para cada função Lambda com suas dependências.
"""
import os
import shutil
import subprocess
import zipfile

# Configurações
LAMBDA_FUNCTIONS = {
    "hello_terraform": {
        "src_dir": "src/lambdas/hello_terraform",
        "dist_file": "hello_terraform_lambda.zip",
    },
    "add_item": {"src_dir": "src/lambdas/add_item", "dist_file": "add_item_lambda.zip"},
    "update_item": {
        "src_dir": "src/lambdas/update_item",
        "dist_file": "update_item_lambda.zip",
    },
    "delete_item": {
        "src_dir": "src/lambdas/delete_item",
        "dist_file": "delete_item_lambda.zip",
    },
    "get_item": {
        "src_dir": "src/lambdas/get_item",
        "dist_file": "get_item_lambda.zip",
    },

}

DIST_DIR = "dist"
TMP_DIR = "tmp"
REQUIREMENTS_FILE = "requirements.txt"


def main():
    """Função principal para empacotar todas as funções Lambda."""
    os.makedirs(DIST_DIR, exist_ok=True)

    for name, config in LAMBDA_FUNCTIONS.items():
        print(f"Empacotando função {name}...")

        # Diretório temporário para esta função
        func_tmp_path = os.path.join(TMP_DIR, name)
        os.makedirs(func_tmp_path, exist_ok=True)

        # Copiar código da função
        lambda_src_dir = config["src_dir"]
        for item in os.listdir(lambda_src_dir):
            if item.endswith(".py"):
                src_file = os.path.join(lambda_src_dir, item)
                dst_file = os.path.join(func_tmp_path, item)
                shutil.copy2(src_file, dst_file)

        # Instalar dependências
        subprocess.run(
            ["pip", "install", "-r", REQUIREMENTS_FILE, "-t", func_tmp_path], check=True
        )

        # Criar arquivo ZIP
        zip_path = os.path.join(DIST_DIR, config["dist_file"])
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(func_tmp_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, func_tmp_path)
                    zipf.write(full_path, arcname)

        print(f"Função {name} empacotada com sucesso: {zip_path}")

    # Limpar diretório temporário
    shutil.rmtree(TMP_DIR, ignore_errors=True)
    print(f"Todos os pacotes foram criados em {DIST_DIR}/")


if __name__ == "__main__":
    main()
