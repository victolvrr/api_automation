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

# --- 15 ENCONTRAR REPOSITÓRIOS COM APACHE-2.0 ---

def test_repos_with_license():
    response = requests.get("https://api.github.com/search/repositories?q=license:apache-2.0")
    data = response.json()
    first_repo_name = data["items"][0]["name"]
    print(f"Primeiro repositório com licença Apache 2.0: {first_repo_name}")
    assert first_repo_name != ""

# --- 16 VALIDAR ORGANIZAÇÃO DO REPOSITÓRIO ---

def test_repo_organization():
    response = requests.get("https://api.github.com/repos/moby/docker")
    data = response.json()
    print(f"Repositório '{data['name']}' pertence à organização '{data['owner']['login']}'")
    assert data["owner"]["login"] == "moby"

# --- 17 CHECAR O ÚLTIMO COMMIT DE UM REPOSITÓRIO ---

def test_last_commit_message():
    response = requests.get("https://api.github.com/repos/tensorflow/tensorflow/commits")
    data = response.json()
    last_commit = data[0]
    commit_message = last_commit["commit"]["message"]
    print(f"Última mensagem de commit: {commit_message}")
    assert commit_message != ""

# --- 18 CHECAR SE UM USUÁRIO É UMA ORGANIZAÇÃO

def test_apple_organization():
    response = requests.get("https://api.github.com/users/apple")
    data = response.json()
    assert data["type"] == "Organization"

# --- 19 ACHAR NÚMERO DE CONTRIBUINTES DE UM REPOSITÓRIO ---

def test_find_number_of_contributors():
    response = requests.get("https://api.github.com/repos/kubernetes/kubernetes/contributors")
    contributors = response.json()
    print(f"\nA primeira página de contribuidores do Kubernetes tem {len(contributors)} usuários.")
    assert len(contributors) > 0

# --- 20 FINAL CHALLENGE ---

def get_user_data(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    return {
        "login": data["login"],
        "name": data["name"],
        "public_repos": data["public_repos"]
    }

def test_torvalds_data():
    user = get_user_data("torvalds")
    assert user["login"] == "torvalds"
    assert isinstance(user["public_repos"], int)
    print(user)

# ------ JSON -----


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
    assert data["name"] == "Chelsey Dietrich"

# --- 28 CRIAR UM NOVO COMENTÁRIO ---

def test_new_comment():
    payload = {"name": "Meu Comentário", "body": "Conteúdo do comentário"}
    response = requests.post("https://jsonplaceholder.typicode.com/posts/1/comments", json=payload)
    print(response.json())
    assert response.status_code == 201

# --- 29 LISTAR ÁLBUM DE USUÁRIOS ---

def test_list_user_albums():
    response = requests.get("https://jsonplaceholder.typicode.com/users/3/albums")
    data = response.json()
    print(f"Total de álbuns do usuário 3: {len(data)}")
    assert len(data) > 0

# --- 30 LISTAR FOTOS NUM ÁLBUM ---

def test_list_album_photos():
    response = requests.get("https://jsonplaceholder.typicode.com/albums/2/photos")
    data = response.json()
    assert isinstance(data, list)
    assert "title" in data[0]
    print("Primeira foto:", data[0]["title"])

# --- 31 CRIAR UMA NOVA TASK ---

def test_create_todo():
    payload = {"userId": 1, "title": "Learn Pytest", "completed": False}
    response = requests.post("https://jsonplaceholder.typicode.com/todos", json=payload)
    data = response.json()
    print(data)
    assert response.status_code == 201
    assert data["title"] == "Learn Pytest"

# --- 32 ATUALIZAR UMA TASK ---

def test_update_todo_status():
    payload = {"completed": True}
    response = requests.patch("https://jsonplaceholder.typicode.com/todos/5", json=payload)
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data["completed"] is True

# --- 33 LISTAR TASKS ---

def test_list_completed_todos():
    response = requests.get("https://jsonplaceholder.typicode.com/users/1/todos")
    data = response.json()
    completed = [todo for todo in data if todo["completed"]]
    print(f"Total de tasks concluídas: {len(completed)}")
    assert len(completed) > 0

# --- 34 VALIDAR ESTRUTURA ---

def test_comment_structure():
    response = requests.get("https://jsonplaceholder.typicode.com/comments/10")
    data = response.json()
    print(data)
    expected_keys = {"postId", "id", "name", "email", "body"}
    assert expected_keys.issubset(data.keys())

# --- 35 DELETAR UM COMENTÁRIO ---
def test_delete_comment():
    response = requests.delete("https://jsonplaceholder.typicode.com/comments/3")
    assert response.status_code in [200, 204], f"Status inesperado: {response.status_code}"


# --- 36 CRIAR UM POST COM DADOS INVÁLIDOS ---
def test_create_post_invalid():
    response = requests.post("https://jsonplaceholder.typicode.com/posts", json={})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data, "Resposta não contém ID"


# --- 37 BUSCAR UM POST ESPECÍFICO DE USUÁRIO ---
def test_fetch_posts_user7():
    response = requests.get("https://jsonplaceholder.typicode.com/users/7/posts")
    assert response.status_code == 200
    data = response.json()
    print(f"O usuário 7 tem {len(data)} posts.")
    assert len(data) > 0


# --- 38 ATUALIZAR UM EMAIL DE USUÁRIO ---
def test_update_user_email():
    payload = {"email": "new.email@example.com"}
    response = requests.put("https://jsonplaceholder.typicode.com/users/2", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["email"] == "new.email@example.com"


# --- 39 APAGAR UM ÁLBUM ---
def test_delete_album():
    response = requests.delete("https://jsonplaceholder.typicode.com/albums/4")
    assert response.status_code in [200, 204]


# --- 40 FINAL CHALLENGE ---
def create_post_comment_and_delete(user_id):
    post_payload = {"userId": user_id, "title": "Post temporário", "body": "Teste automático"}
    post_resp = requests.post("https://jsonplaceholder.typicode.com/posts", json=post_payload)
    assert post_resp.status_code == 201
    post_id = post_resp.json()["id"]

    comment_payload = {"postId": post_id, "name": "Bot Test", "email": "bot@test.com", "body": "Comentário teste"}
    comment_resp = requests.post("https://jsonplaceholder.typicode.com/comments", json=comment_payload)
    assert comment_resp.status_code == 201

    delete_resp = requests.delete(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    assert delete_resp.status_code in [200, 204]

    return {"post_id": post_id, "status": "OK"}


def test_final_challenge():
    result = create_post_comment_and_delete(1)
    assert result["status"] == "OK"
    print(result)