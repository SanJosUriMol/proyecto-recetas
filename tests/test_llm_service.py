import pytest
import json
from app.services.llm_service import build_prompt, parse_llm_response

#Ejemplos de datos que se insertaran o se mostraran en la pagina
def test_build_prompt_contiene_ingredientes():
    prompt = build_prompt(["tomate", "cebolla", "ajo"])
    assert "tomate" in prompt
    assert "cebolla" in prompt
    assert "ajo" in prompt

def test_build_prompt_formato():
    prompt = build_prompt(["arroz"])
    assert "JSON" in prompt
    assert "nombre_plato" in prompt

def test_parse_llm_response_valido():
    data = {
        "nombre_plato": "Arroz con pollo",
        "ingredientes": [{"nombre": "arroz", "cantidad": "1", "unidad": "taza"}],
        "pasos": ["Paso 1: cocer el arroz"],
        "tiempo_estimado": "30 minutos",
        "nivel_dificultad": "Facil"
    }
    result = parse_llm_response(json.dumps(data))
    assert result["nombre_plato"] == "Arroz con pollo"

def test_parse_llm_response_con_markdown():
    data = {
        "nombre_plato": "Sopa",
        "ingredientes": [],
        "pasos": ["Hervir agua"],
        "tiempo_estimado": "15 minutos",
        "nivel_dificultad": "Facil"
    }
    raw = "```json\n" + json.dumps(data) + "\n```"
    result = parse_llm_response(raw)
    assert result["nombre_plato"] == "Sopa"

def test_parse_llm_response_campos_faltantes():
    with pytest.raises(ValueError):
        parse_llm_response(json.dumps({"nombre_plato": "Algo"}))

def test_parse_llm_response_json_invalido():
    with pytest.raises(Exception):
        parse_llm_response("esto no es json")
