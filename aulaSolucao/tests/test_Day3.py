import pytest
import csv
import os

def load_test_cases_from_csv(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Corrige o caminho do CSV para funcionar de qualquer diretório
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "aula3.csv")
test_data = load_test_cases_from_csv(csv_path)

@pytest.mark.api_test
@pytest.mark.parametrize("test_case", test_data, ids=[tc["title"] for tc in test_data])
def test_create_post_dynamically(base_url, api_client, test_case):
    """Testa criação de posts com dados do CSV."""
    payload = {
        "title": test_case["title"],
        "body": test_case["body"],
        "userId": int(test_case["userId"]) if test_case["userId"] else 1
    }
    expected_status = int(test_case["expected_status"])

    response = api_client.post(f"{base_url}/posts", json=payload)

    assert response.status_code == expected_status
    if expected_status == 201:
        assert response.json()["title"] == payload["title"]
