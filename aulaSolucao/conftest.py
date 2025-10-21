import pytest
import requests
import csv
import logging
import os
from datetime import datetime

# LOGGING GLOBAL
def setup_logging():
    """Configura log para console e arquivo."""
    log_filename = f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_filename, encoding="utf-8"),
            logging.StreamHandler()
        ],
    )
    logging.info("=== Iniciando sessão de testes ===")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Executa antes dos testes começarem."""
    setup_logging()


# API CLIENT PERSONALIZADO
class ApiClient(requests.Session):
    """Cliente HTTP customizado que armazena o último response."""
    def __init__(self):
        super().__init__()
        self.last_response = None

    def request(self, method, url, **kwargs):
        logging.info(f" {method.upper()} {url}")
        if "json" in kwargs:
            logging.info(f"Payload: {kwargs['json']}")
        response = super().request(method, url, **kwargs)
        self.last_response = response
        logging.info(f" Status: {response.status_code}")
        return response


# FIXTURES
@pytest.fixture(scope="session")
def base_url():
    """URL base da API."""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_client():
    """Cria uma instância compartilhada do ApiClient."""
    client = ApiClient()
    yield client
    client.close()


def load_csv_test_cases(path):
    """Lê um CSV e devolve lista de dicionários."""
    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


@pytest.fixture(scope="session")
def post_test_cases():
    """Carrega os casos de teste do CSV automaticamente."""
    # Descobre o diretório raiz do projeto (onde está este conftest)
    root_dir = os.path.dirname(__file__)
    # Monta o caminho até o CSV dentro da pasta tests/
    csv_path = os.path.join(root_dir, "tests", "aula3.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Arquivo CSV não encontrado em: {csv_path}")
    return load_csv_test_cases(csv_path)


# HOOK – INJETAR RESPONSE NO RELATÓRIO HTML
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Anexa o corpo da resposta no relatório se o teste falhar."""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        client = item.funcargs.get("api_client", None)
        if client and client.last_response is not None:
            try:
                body = client.last_response.text
                rep.longrepr = f"{rep.longrepr}\n\n--- API Response Body ---\n{body}"
            except Exception as e:
                logging.error(f"Erro ao anexar resposta ao relatório: {e}")