# Generador de Recetas con IA

Aplicación web desarrollada con **FastAPI + MySQL + OpenRouter (LLM)** que permite a los usuarios registrar ingredientes disponibles en casa y generar recetas personalizadas usando inteligencia artificial.

## Integrantes del equipo

| Nombre | GitHub |
|--------|--------|
| Santiago Jose Uribe Molina | @SanJosUriMol |
| Yesica Gonzalez | @yesicadelcarmengonzalezjulio-cyber |
| Natalia Baena | @nataliatbaena-code |
| Nestor Alandete | @nestor2208 |
| Rafael Garcia | @rafalegartor05 |

## Tecnologías

- **Backend:** Python 3.11 + FastAPI
- **Base de datos:** MySQL 8.0 + SQLAlchemy
- **Autenticación:** JWT (python-jose + passlib)
- **LLM:** OpenRouter API (modelo automático)
- **Despliegue:** AWS Lightsail + Docker + Docker Compose
- **Pruebas:** pytest
- **Frontend:** HTML + CSS + JavaScript (SPA)

## Estructura del proyecto

proyecto-recetas/
├── app/
│   ├── main.py              # Punto de entrada
│   ├── config.py            # Variables de entorno
│   ├── database.py          # Conexión SQLAlchemy
│   ├── models/
│   │   └── models.py        # Tablas de la BD
│   ├── routers/
│   │   ├── auth.py          # Registro e inicio de sesión
│   │   ├── ingredientes.py  # CRUD de ingredientes
│   │   └── recetas.py       # Generación y gestión de recetas
│   ├── schemas/
│   │   └── schemas.py       # Modelos Pydantic
│   └── services/
│       ├── auth_service.py  # JWT y contraseñas
│       └── llm_service.py   # Integración OpenRouter
├── tests/
│   ├── test_ingredientes.py
│   ├── test_llm_service.py
│   └── test_calificacion.py
├── static/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── favicon.ico
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── pytest.ini
└── requirements.txt