
# 🎯 Aplicação Alvo (SUT): API de Usuários com FastAPI

Este repositório contém uma API RESTful desenvolvida em **FastAPI** utilizando **SQLite** como banco de dados. 

O projeto serve como **System Under Test (SUT)** (Sistema Sob Teste) para o projeto de pesquisa: *"Análise Comparativa da Detecção de Vulnerabilidades e Code Smells em Pull Requests: Uma Abordagem Híbrida com LLMs e Análise Estática Tradicional"*.

O objetivo deste código é servir de base para a submissão de Pull Requests contendo vulnerabilidades intencionais (SQL Injection, XSS, Code Smells) para validar a eficácia da ferramenta **LLM-Code-Reviewer**.

## 🚀 Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Framework Web:** FastAPI
- **Servidor:** Uvicorn
- **ORM:** SQLAlchemy
- **Validação de Dados:** Pydantic
- **Banco de Dados:** SQLite (Arquivo local `app_fastapi.db`)

## 📂 Estrutura do Projeto

```text
projeto-alvo/
│
├── app/                  # Código Fonte da Aplicação
│   ├── __init__.py       # Inicializador do pacote
│   └── main.py           # Entrypoint da API e Modelos ORM
│
├── venv/                 # Ambiente Virtual (Não versionado)
├── .gitignore            # Arquivos ignorados pelo Git
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação
````

## 🛠️ Configuração e Instalação

Siga os passos abaixo para executar o projeto localmente.

### 1\. Pré-requisitos

Certifique-se de ter o **Python 3.10** ou superior instalado.

### 2\. Clonar e Configurar Ambiente

```bash
# Clone o repositório
git clone <URL_DO_SEU_REPO>
cd projeto-alvo

# Crie o ambiente virtual
python3 -m venv venv

# Ative o ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows (PowerShell):
.\venv\Scripts\activate
```

### 3\. Instalar Dependências

```bash
pip install -r requirements.txt
```

## ▶️ Executando a Aplicação

Para iniciar o servidor de desenvolvimento, utilize o comando abaixo. Note que utilizamos o módulo `app.main` devido à estrutura de pastas.

```bash
python -m uvicorn app.main:app --reload
```

O servidor iniciará em: `http://127.0.0.1:8000`

> **Nota:** O parâmetro `--reload` permite que o servidor reinicie automaticamente ao detectar alterações no código.

## 📚 Documentação da API

O FastAPI gera documentação interativa automaticamente. Com o servidor rodando, acesse:

  - **Swagger UI (Recomendado):** [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)  
    Permite testar os endpoints `GET` e `POST` diretamente pelo navegador.

  - **ReDoc:** [http://127.0.0.1:8000/redoc](https://www.google.com/search?q=http://127.0.0.1:8000/redoc)  
    Visualização alternativa da documentação.

## 🧪 Endpoints Disponíveis

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/users/` | Cria um novo usuário (JSON: `username`, `email`). |
| `GET` | `/users/` | Lista todos os usuários cadastrados. |

## ⚖️ Licença

Este projeto é destinado exclusivamente para fins acadêmicos e de pesquisa.

