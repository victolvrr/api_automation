import requests
import pytest
import webbrowser

def test_simple_request():
    response = requests.get("https://pokeapi.co/api/v2/pokemon")
    assert response.status_code == 200

def test_name_pikachu():
    response = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")
    data = response.json()
    assert data["name"] == "pikachu"

def test_type_electric():
    response = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")
    data = response.json()
    types = [t["type"]["name"] for t in data["types"]]
    assert "electric" in types

def test_multiple_pokemons():
    pokemons = ["lucario", "tyranitar", "volcarona"]
    for pokemon in pokemons:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == pokemon

def test_ability_static():
    response = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")
    data = response.json()
    abilities = [a["ability"]["name"] for a in data["abilities"]]
    assert "static" in abilities

def test_lucario_id():
    response = requests.get("https://pokeapi.co/api/v2/pokemon/lucario")
    data = response.json()
    assert data["id"] == 448

def test_invalid_route():
    response = requests.get("https://pokeapi.co/api/v2/pokemon/abcxyz")
    assert response.status_code == 404

def test_performance():
    response = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")
    assert response.elapsed.total_seconds() < 1.0

def test_comparation_id_lucario_tyranitar():
    response_lucario = requests.get("https://pokeapi.co/api/v2/pokemon/lucario")
    response_tyranitar = requests.get("https://pokeapi.co/api/v2/pokemon/tyranitar")
    data_lucario = response_lucario.json()
    data_tyranitar = response_tyranitar.json()
    assert data_lucario["id"] > data_tyranitar["id"]

def test_open_lucario_image():
    response = requests.get("https://pokeapi.co/api/v2/pokemon/lucario")
    data = response.json()
    image_url = data["sprites"]["front_default"]
    webbrowser.open(image_url)

def test_open_tyranitar_image():
    response = requests.get("https://pokeapi.co/api/v2/pokemon/tyranitar")
    data = response.json()
    image_url = data["sprites"]["front_default"]
    webbrowser.open(image_url)

def test_open_volcarona_image():
    response = requests.get("https://pokeapi.co/api/v2/pokemon/volcarona")
    data = response.json()
    image_url = data["sprites"]["front_default"]
    webbrowser.open(image_url)