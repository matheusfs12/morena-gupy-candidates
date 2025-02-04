# Filtrador de Candidatos - Gupy API

Este aplicativo é uma ferramenta para consultar a API da Gupy e filtrar candidatos pelo campo `jobStep.name`.

## Funcionalidades

- Autenticação via token (`company_key_auth`).
- Filtragem de candidatos pelo campo `jobStep.name`.
- Exibição das URLs dos candidatos filtrados.

## Requisitos

- Python 3.x
- Bibliotecas: `streamlit`, `requests`

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/morena-gupy.git
    cd morena-gupy
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Execute o aplicativo:
    ```bash
    streamlit run app.py
    ```

2. No navegador, insira o token de autenticação e o `Job Step Name` para filtrar os candidatos.

## Licença

Este projeto está licenciado sob a licença MIT.
