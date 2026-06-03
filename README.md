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

## Modelo de base de datos

El sistema cuenta con 4 tablas relacionales:

- **usuarios** — almacena nombre, email y contraseña hasheada
- **ingredientes** — ingredientes del inventario personal de cada usuario
- **recetas** — recetas generadas por la IA con ingredientes, pasos, tiempo y dificultad
- **calificaciones** — calificaciones de 1 a 5 estrellas por receta y usuario

Relaciones:
- Un usuario tiene muchos ingredientes
- Un usuario tiene muchas recetas
- Una receta tiene muchas calificaciones

## Configuración local

### 1. Clonar el repositorio

git clone https://github.com/SanJosUriMol/proyecto-recetas.git
cd proyecto-recetas

### 2. Crear archivo .env

cp .env.example .env
# Editar .env con tus credenciales reales

### 3. Variables necesarias en .env

DATABASE_URL=mysql+pymysql://app_user:app_password@db:3306/recetas_db
SECRET_KEY=tu_clave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=openrouter/auto
MYSQL_ROOT_PASSWORD=root_password
MYSQL_USER=app_user
MYSQL_PASSWORD=app_password

> ⚠️ Nunca subas el archivo `.env` al repositorio. Está incluido en `.gitignore`.

### 4. Levantar con Docker Compose

docker compose up --build

La API estará disponible en http://localhost:8000
Documentación Swagger: http://localhost:8000/docs

### 5. Ejecutar pruebas

docker compose exec app pytest

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/auth/registro` | Registrar nuevo usuario |
| POST | `/auth/login` | Iniciar sesión (devuelve JWT) |
| GET | `/ingredientes/` | Listar ingredientes |
| POST | `/ingredientes/` | Agregar ingrediente |
| PUT | `/ingredientes/{id}` | Editar ingrediente |
| DELETE | `/ingredientes/{id}` | Eliminar ingrediente |
| POST | `/recetas/generar` | Generar receta con IA |
| GET | `/recetas/` | Ver historial de recetas |
| GET | `/recetas/{id}` | Ver receta específica |
| DELETE | `/recetas/{id}` | Eliminar receta |
| POST | `/recetas/{id}/calificar` | Calificar receta (1-5 estrellas) |