# 🛒 Market List com Terraform, AWS Lambda e Python

Este projeto tem como objetivo criar uma aplicação serverless  para gerenciamento de uma lista de compras, utilizando **AWS Lambda**, **DynamoDB**, **Terraform** e **Python**. Ele demonstra como construir, empacotar e implantar múltiplas funções Lambda organizadas, de forma automatizada com infraestrutura como código.

---

## ⚙️ Funcionalidades Disponíveis

* **Hello Terraform**: Retorna uma mensagem simples

* **Add Item**: Adiciona um item à lista de compras

* **Update Item**: Atualiza o nome ou status de um item

* **Delete Item**: Remove um item da lista de compras

---

## 📸 Demonstrações Visuais

### ✅ Hello Terraform

![Hello Terraform](docs/images/image.png)

### ➕ Adicionando um item à lista

![item adicionado](docs/images/image-2.png)

### 🔄 Atualizando um item da lista

![atualizando item](docs/images/image-3.png)

### 🗃️ DynamoDB

![dynamoDB](docs/images/image-4.png)
![dynamoDB](docs/images/image-5.png)

### ❌ Deletando um item da lista

![delete item](docs/images/image-6.png)

### 📉 DynamoDB após exclusão do item

![exclusão do item](docs/images/image-7.png)

---

## 📁 Estrutura do Projeto

```plaintext
meu_projeto/
├── .venv/                      # Ambiente virtual Python
├── dist/                       # Arquivos zip das funções Lambda empacotadas
│   ├── add_item_lambda.zip
│   ├── delete_item_lambda.zip
│   ├── hello_terraform_lambda.zip
│   └── update_item_lambda.zip
├── requirements.txt            # Dependências da aplicação
├── requirements-dev.txt        # Dependências para desenvolvimento e testes
├── scripts/
│   └── build.py                # Script de empacotamento das Lambdas
├── src/
│   ├── common/                 # Código compartilhado entre funções (em breve)
│   └── lambdas/                # Funções Lambda organizadas por responsabilidade
│       ├── add_item/
│       │   └── lambda_function.py
│       ├── delete_item/
│       │   └── lambda_function.py
│       ├── hello_terraform/
│       │   └── lambda_function.py
│       └── update_item/
│           └── lambda_function.py
├── tests/
│   └── test_lambdas/           # Testes automatizados das funções Lambda
├── terraform/                  # Código Terraform para infraestrutura na AWS
│   ├── dynamodb.tf
│   ├── iam.tf
│   ├── main.tf
│   ├── outputs.tf
│   ├── providers.tf
│   ├── variables.tf
│   ├── terraform.tfstate
│   ├── terraform.tfstate.backup
│   
│
│   ├── environments/           # Ambientes separados (dev, prod)
│   │   ├── dev/
│   │   └── prod/
│
│   └── modules/                # Módulos reutilizáveis do Terraform
│       └── lambda/
│           ├── main.tf
│           ├── outputs.tf
│           └── variables.tf

```

## 📦 Empacotamento das Funções Lambda

* Para executar o comando python scripts/build.py e empacotar as funções Lambda, você deve estar na raiz do projeto, onde a pasta scripts está localizada.

```bash
python scripts/build.py
```

## Pré-requisitos

- Python 3.9+
- Terraform 1.0+
- AWS CLI configurado com as credenciais necessárias

🎯 Boas Práticas de Código

### Organizar imports

```bash
isort .
```

### Formatar código

```bash
black .
```

## Clonar o repositório (após criá-lo no GitHub)

```bash
git clone <url-do-repositorio>
cd meu_projeto

# Criar e ativar ambiente virtual
py -m venv .venv

# No Windows pelo GitBash:
source .venv/Scripts/activate

# pelo Powershell
.\.venv\Scripts\activate

# Instalar dependências
pip install -r requirements-dev.txt

1. Empacotar funções Lambda
# Executar script de empacotamento
python scripts/build.py

```

## ☁️ Deploy com Terraform

```bash
cd terraform

# Limpar o cache e reinicializar
rm -rf .terraform

# Inicializar Terraform
terraform init

# Verificar plano de execução
terraform plan

# Aplicar alterações
terraform apply
```

## 🔄 Fluxo de Trabalho Git

Este repositório segue um fluxo de trabalho estruturado para desenvolvimento.

### 🌿 Estrutura de Branches

- `main` 🟢: Branch de produção, contém código estável e testado
- `dev` 🧪: Branch de desenvolvimento, integra features completas
- Branches de feature 🔧: `feature/*`, `bugfix/*`, `hotfix/*`

### 📌 Regras de Fluxo

1. 🚫 **Nunca faça push direto para `main`**
   - ✅ Todo código em `main` deve passar por um PR do branch `dev`

2. 🚫 **Nunca faça push direto para `dev`**
   - ✅ Todo código em `dev` deve passar por um PR de um branch de feature

3. ✨ **Desenvolvimento de novas funcionalidades**
   - 🔀 Crie um branch a partir de `dev`:  
     `git checkout -b feature/nome-da-feature dev`
   - 🧪 Desenvolva e teste a funcionalidade
   - 📥 Abra um PR do seu branch de feature para `dev`
   - ✅ Após aprovação, faça merge do PR

4. 🚀 **Releases para produção**
   - 📥 Abra um PR de `dev` para `main`
   - ✅ Após revisão e aprovação, faça merge do PR para `main`

---

## 🧾 Convenção de Commits

Este projeto segue a convenção [Conventional Commits](https://www.conventionalcommits.org/):

- `feat` ✨: Nova funcionalidade
- `fix` 🐛: Correção de bug
- `docs` 📚: Alterações na documentação
- `chore` 🔧: Alterações em scripts de build, configurações, etc.
- `test` ✅: Adição ou modificação de testes
- `refactor` 🔨: Refatoração de código sem alteração de funcionalidade


# ✅ Configuração de CD com GitHub Actions

## 🎯 Contexto

- Configurar **CD (Continuous Deployment)** via **GitHub Actions**.
- Aplicar **Deploy** automaticamente a cada **PR (Pull Request)** aplicado na branch `developer`.
- **Destruir toda infraestrutura local** via **Terraform**.
- Configurar o **GitHub** para fazer o deploy automaticamente.

---

## ✅ Pontos de Ação (Checklist)

- [x] Destruir a infraestrutura local criada pelo Terraform.
- [x] Configurar um **GitHub Action** para aplicar o código no **Merge** de um **Pull Request**.
- [x] Evitar conflito entre **deploy local** e o **GitHub Action**.
- [x] Não criar variáveis genéricas como `AWS_ACCOUNT` ou `AWS_SECRET`.  
Usar Secrets específicos por ambiente:  
→ `AWS_ACCOUNT_DEV`  
→ `AWS_ACCOUNT_HOMOL`

- [x] Planejar múltiplos ambientes (**produção**, **homologação**, etc.) com variáveis separadas.
- [x] Realizar o **destroy** de toda infraestrutura local com Terraform.
- [x] Configurar o **GitHub Action** para aplicar o código automaticamente no Merge.

---

## 💥 Destruindo a infraestrutura local com Terraform

```bash
# 1. Ir para pasta terraform
cd terraform

# 2. Inicializar terraform (para poder destruir)
terraform init

# 3. Destruir toda infraestrutura
terraform destroy -auto-approve

# 4. Limpar arquivos locais
rm terraform.tfstate*
rm -rf .terraform
rm .terraform.lock.hcl

# 5. Voltar para raiz do projeto
cd ..

# 🔐 Passo a Passo - Adicionar Secrets no GitHub

## ✅ PASSO 1: Ir para Settings do Repositório
- Abra seu repositório no GitHub.
- Clique na aba **Settings** (no topo, ao lado de **Actions**).

## ✅ PASSO 2: Navegar para Secrets
- No menu lateral esquerdo, role para baixo.
- Clique em **Secrets and variables**.
- Clique em **Actions**.

## ✅ PASSO 3: Adicionar o Primeiro Secret
- Clique em **New repository secret**.
- **Name:** `AWS_ACCESS_KEY_ID_DEV`
- **Secret:** Cole sua AWS Access Key (exemplo: `AKIA1234567890ABCDEF`).
- Clique em **Add secret**.

## ✅ PASSO 4: Adicionar o Segundo Secret
- Clique em **New repository secret** novamente.
- **Name:** `AWS_SECRET_ACCESS_KEY_DEV`
- **Secret:** Cole sua AWS Secret Key (exemplo: `abc123xyz789...`).
- Clique em **Add secret**.

---

# 🔑 Como pegar suas credenciais AWS

## ✅ Opção 1: AWS Console (Interface Web)
1. Login na **AWS Console**.
2. Vá em **IAM → Users**.
3. Clique no seu usuário.
4. Aba **Security credentials**.
5. Clique em **Create access key**.
6. **Use case:** escolha **Command Line Interface (CLI)**.
7. Copie os valores:

```text
Access key ID → Para AWS_ACCESS_KEY_ID_DEV
Secret access key → Para AWS_SECRET_ACCESS_KEY_DEV
```

## ✅ Opção 2: AWS CLI (se já configurado)

```bash
# Mostrar suas credenciais atuais
cat ~/.aws/credentials
```

**Exemplo de resultado:**

```ini
[default]
aws_access_key_id = AKIA1234567890ABCDEF     ← Copie este
aws_secret_access_key = abc123xyz789...      ← Copie este
```
