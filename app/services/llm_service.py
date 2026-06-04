import json
import httpx
from app.config import settings


# Servicio de integración con OpenRouter API
# Responsable de construir el prompt, llamar al LLM y parsear la respuesta
# El modelo se configura mediante la variable OPENROUTER_MODEL en el .env
PROMPT_TEMPLATE = """Eres un chef experto. A partir de los siguientes ingredientes disponibles, genera UNA receta completa.

Ingredientes disponibles: {ingredientes}

Responde UNICAMENTE con un objeto JSON valido con esta estructura exacta (sin texto adicional):
{{
  "nombre_plato": "Nombre del plato",
  "ingredientes": [
    {{"nombre": "ingrediente", "cantidad": "cantidad", "unidad": "unidad"}}
  ],
  "pasos": [
    "Paso 1: ...",
    "Paso 2: ..."
  ],
  "tiempo_estimado": "30 minutos",
  "nivel_dificultad": "Facil"
}}"""

# Construye el prompt enviado al LLM con los ingredientes del usuario
def build_prompt(ingredientes: list) -> str:
    ingredientes_str = ", ".join(ingredientes)
    return PROMPT_TEMPLATE.format(ingredientes=ingredientes_str)

# Parsea y valida la respuesta JSON del LLM
def parse_llm_response(raw_response: str) -> dict:
    text = raw_response.strip()
    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    data = json.loads(text)
    required_keys = {"nombre_plato", "ingredientes", "pasos", "tiempo_estimado", "nivel_dificultad"}
    missing = required_keys - set(data.keys())
    if missing:
        raise ValueError(f"La respuesta del LLM no contiene los campos requeridos: {missing}")
    return data

# Llama a OpenRouter y devuelve la receta parseada
async def generate_recipe(ingredientes: list) -> dict:
    prompt = build_prompt(ingredientes)
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.OPENROUTER_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            },
        )
        response.raise_for_status()
    raw = response.json()["choices"][0]["message"]["content"]
    return parse_llm_response(raw)
