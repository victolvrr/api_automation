import requests
import pytest

# --- 1 REQUISIÇÃO SIMPLES ---

def test_simple_request():
    response = requests.get("https://api.github.com")
    assert response.status_code == 200

# --- 2 3 REQUISIÇÃO USER ---

def test_get_specific_user():
    response = requests.get("https://api.github.com/users/octocat")
    data = response.json()
    assert data["login"] == "octocat"
    print(data["login"])

# --- 4 REQUISIÇÃO REPOSITÓRIO ---

def test_request_repository():
    response = requests.get("https://api.github.com/repositories/1296269")
    data = response.json()
    assert data["id"] == 1296269

# --- 5 USER INVÁLIDO ---

def test_invalid_user():
    response = requests.get("https://api.github.com/user/nonexistentuser12345")
    response.json()
    assert response.status_code == 404

# --- 6 LISTAR REPOSITÓRIOS ---

def test_list():
    response = requests.get("https://api.github.com/users/google/repos?per_page=5")
    data = response.json()
    print(data[0]["name"])
    assert len(data) <= 5

# ---  7 NAVEGAÇÃO FOLLOWER PAGINATION ---

def test_step_7():
    microsoft_followers = requests.head("https://api.github.com/users/microsoft/followers")
    microsoft_next_page_link = microsoft_followers.links["next"]["url"]
    print(microsoft_next_page_link)
    micro_follows = requests.get(microsoft_next_page_link)
    assert micro_follows.status_code == 200

# --- 8 REPOSITÓRIO PÚBLICO ---

def test_facebook_repositories():
    response = requests.get("https://api.github.com/users/facebook")
    data = response.json()
    assert data["public_repos"] == 153

# --- 9 LINGUAGEM ESPECÍFICA ---

def test_language_js():
    response = requests.get("https://api.github.com/repos/facebook/react/languages")
    data = response.json()
    assert "JavaScript" in data

# --- 10 EXPLORAR OUTRO ENDPOINT (EMOJIS) ---

def test_emojis():
    response = requests.get("https://api.github.com/emojis")
    data = response.json()
    assert "+1" in data

# --- 11 VALIDAR REPOSITÓRIO ESTRUTURA JSON ---

def test_linux_repository():
    response = requests.get("https://api.github.com/repos/torvalds/linux")
    data = response.json()
    assert "name" in data
    assert "owner" in data
    assert "language" in data

# --- 12 COMPARAR ATRIBUTOS DE UM REPOSITÓRIO ---

def test_repository_attributes():
    response_vscode = requests.get("https://api.github.com/repos/microsoft/vscode")
    data_vscode = response_vscode.json()["stargazers_count"]

    response_atom = requests.get(f"https://api.github.com/repos/atom/atom")
    data_atom = response_atom.json()["stargazers_count"]
    assert data_vscode > data_atom

# --- 13 LICENÇA ---

def test_mit_license():
    response = requests.get("https://api.github.com/licenses/mit")
    data = response.json
    assert data

# --- 14 LISTAR TODAS AS LICENÇAS ---

def test_list_licenses():
    response = requests.get("https://api.github.com/licenses")
    data = response.json()
    print(f"Total de licenças: {len(data)}")
    assert len(data) > 0

# --- 21 CRIAR UM NOVO POST 22 VALIDAÇÃO ---

def test_create_post():
    payload = {"title": "New post", "body": "test", "userId": 1}
    response = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload)
    data = response.json()
    print(response.json())
    assert response.status_code == 201
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]

# --- 23 ATUALIZAR UM POST 24 VALIDAÇÃO ---

def test_update_post():
    payload = {"id": 1, "title": "Post atualizado", "body": "Conteúdo editado", "userId": 1}
    response = requests.put("https://jsonplaceholder.typicode.com/posts/1", json=payload)
    data = response.json()
    print(response.json())
    assert response.status_code == 200
    assert data["body"] == payload["body"]

# --- 25 DELETAR UM POST ---

def test_delete_post():
    response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
    assert response.status_code == 200

# --- 26 LISTAR TODOS OS USUÁRIOS ---

def test_all_users():
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    data = response.json()
    print(f"Total de usuários: {len(data)}")
    assert len(data) == 10

# --- 27 BUSCAR UM USUÁRIO ESPECÍFICO ---

def test_fetch_chelsey():
    response = requests.get("https://jsonplaceholder.typicode.com/users/5")
    data = response.json()
    print(data)