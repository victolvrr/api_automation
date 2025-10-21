from urllib import response
from wsgiref import headers
import requests
import pytest

def skip_if_httpbin_down(response):
    if response.status_code == 503:
        pytest.skip("Servidor httpbin.org indisponível (503). Teste pulado.")

# --- 1 BUSCAR COMENTÁRIOS DO POST ID 2 E VALIDAR ---

def test_comments_for_post_2():
    response = requests.get("https://jsonplaceholder.typicode.com/comments", params={"postId": 2})
    assert response.status_code == 200
    data = response.json()
    assert all(comment["postId"] == 2 for comment in data), "Nem todos os comentários são do post 2"

# --- 2 LISTAR OS TO DOS DO USER ID 5 E VALIDAR ---

def test_todos_for_user_5():
    response = requests.get("https://jsonplaceholder.typicode.com/todos", params={"userId": 5})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

# --- 3 BUSCAR TODOS OS ÁLBUNS DO USER ID 9 ---

def test_albums_user_9():
    response = requests.get("https://jsonplaceholder.typicode.com/albums",  params={"userId": 9})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10, f"Esperado 10 álbuns, mas veio {len(data)}"

# --- 4 LISTAR TODOS O TO DOS PARA O USER ID 1 E VALIDAR ---

def test_list_todos_for_user_1():
    response = requests.get("https://jsonplaceholder.typicode.com/todos", params={"userId": 1, "completed": "true"})
    assert response.status_code == 200
    data = response.json()
    assert all(todo["completed"] is True for todo in data)

# # --- 5 ENVIAR UMA REQUEST E VALIDAR ---

def test_custom_header():
    headers = {"X-Custom-Header": "MyValue"}
    response = requests.get("https://httpbin.org/headers", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["headers"]["X-Custom-Header"] == "MyValue"

# --- 6 ENVIAR UMA REQUEST E CHECAR---

def test_custom_response():
    response = requests.get("https://httpbin.org/response-headers", params={"My-Test-Header": "Hello"})
    assert response.status_code == 200
    assert response.headers["My-Test-Header"] == "Hello"

# --- 7 ENVIAR UMA REQUEST E VALIDAR SE RECEBEU CORRETAMENTE---

def test_custom_agent_header():
    headers = {"User-Agent": "My-Test-Agent/1.0"}
    response = requests.get("https://httpbin.org/headers", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["headers"]["User-Agent"] == "My-Test-Agent/1.0"

# --- 8 ENVIAR MULTIPLAS CUSTOM HEADERS ---

def test_multiple_custom_headers():
    headers = {"X-Header-1": "Value1", "X-Header-2": "Value2"}
    response = requests.get("https://httpbin.org/headers", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["headers"]["X-Header-1"] == "Value1"
    assert data["headers"]["X-Header-2"] == "Value2"

# --- 9 ---

def test_basic_auth_success():
    url = "https://httpbin.org/basic-auth/user/passwd"
    response = requests.get(url, auth=("user", "passwd"))
    assert response.status_code == 200
    data = response.json()
    assert data.get("authenticated") is True
    assert data.get("user") == "user"

# --- 10 ---

def test_basic_auth_wrong_password():
    url = "https://httpbin.org/basic-auth/user/passwd"
    response = requests.get(url, auth=("user", "wrong_password"))
    assert response.status_code == 401

# --- 11 ---

def test_bearer_token_success():
    url = "https://httpbin.org/bearer"
    headers = {"Authorization": "Bearer my-mock-token"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data.get("authenticated") is True
    assert data.get("token") == "my-mock-token"

# --- 12 ---

def test_bearer_token_missing():
    url = "https://httpbin.org/bearer"
    response = requests.get(url)
    assert response.status_code == 401

# --- 13 e 14 ---

def test_user_1_data_types():
    response = requests.get("https://jsonplaceholder.typicode.com/users/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["id"], int), "O 'id' não é do tipo int"
    assert isinstance(data["name"], str), "O 'name' não é do tipo str"
    assert isinstance(data["address"], dict), "O 'address' não é do tipo dict"
    assert isinstance(data["company"], dict), "O 'company' não é do tipo dict"
    address = data["address"]
    assert "street" in address, "A chave 'street' não está presente em 'address'"
    assert "city" in address, "A chave 'city' não está presente em 'address'"
    assert "zipcode" in address, "A chave 'zipcode' não está presente em 'address'"

# --- 15 ---

def test_post_10_data_types():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["userId"], int), "O 'userId' não é do tipo int"
    assert isinstance(data["id"], int), "O 'id' não é do tipo int"
    assert isinstance(data["title"], str) and data["title"], "O 'title' não é uma string não vazia"
    assert isinstance(data["body"], str) and data["body"], "O 'body' não é uma string não vazia"

# --- 16 ---

def photos_in_album_1():
    response = requests.get("https://jsonplaceholder.typicode.com/photos", params={"albumId": 1})
    assert response.status_code == 200
    data = response.json()
    required_keys = {"albumId", "id", "title", "url", "thumbnailUrl"}
    for photo in data:
        assert required_keys.issubset(photo.keys()), f"Foto com ID {photo.get('id')} está faltando algumas chaves obrigatórias"

# 17.
    response = requests.get("https://jsonplaceholder.typicode.com/users/3")
    assert response.status_code == 200
    data = response.json()
    email = data.get("email", "")
    assert "@" in email and "." in email.split("@")[-1], f"O email '{email}' não está em um formato válido"

# 18.
def test_comments_for_post_5_not_empty():
    response = requests.get("https://jsonplaceholder.typicode.com/comments", params={"postId": 5})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0, "A lista de comentários para o post ID 5 está vazia"

#19.

def test_first_comment_types_post_5():
    response = requests.get("https://jsonplaceholder.typicode.com/comments", params={"postId": 5})
    assert response.status_code == 200
    data = response.json()
    first_comment = data[0]
    assert isinstance(first_comment["postId"], int), "O 'postId' não é do tipo int"
    assert isinstance(first_comment["id"], int), "O 'id' não é do tipo int"
    assert isinstance(first_comment["name"], str), "O 'name' não é do tipo str"
    assert isinstance(first_comment["email"], str), "O 'email' não é do tipo str"
    assert isinstance(first_comment["body"], str), "O 'body' não é do tipo str"

# 20. 

def test_todo_199_completed_type():
    response = requests.get("https://jsonplaceholder.typicode.com/todos/199")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["completed"], bool), "O valor de 'completed' não é do tipo booleano"