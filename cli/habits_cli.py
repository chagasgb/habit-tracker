import sys
import json
import requests
import typer
from typer import Typer
from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
    colorize=True
)

BASE_URL = "http://localhost:8000"

app = Typer()

@app.command()
def get_habits():
    """Acessa a API de hábitos e exibe os dados formatados em JSON."""
    
    logger.info("Acessando a API de hábitos...")
    url = f"{BASE_URL}/habits/"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # metodo para checar se a requisição foi bem sucedida

        formatted_json = json.dumps(response.json(), indent=4, ensure_ascii=False)
        typer.echo(formatted_json)

        logger.info("Dados recebidos com sucesso!")

    except requests.RequestException as e:
        logger.error(f"Erro ao acessar {url}: {e}")


if __name__ == "__main__":
    app()
