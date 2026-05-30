# Generador de Recetas con IA

Aplicación web desarrollada con **FastAPI + MySQL + OpenRouter (LLM)** que permite a los usuarios registrar ingredientes disponibles en casa y generar recetas personalizadas usando inteligencia artificial.

## Integrantes del equipo

| Nombre | GitHub |
|--------|--------|
| (Nombre 1) | @usuario1 |
| (Nombre 2) | @usuario2 |

## Tecnologías

- **Backend:** Python 3.11 + FastAPI
- **Base de datos:** MySQL 8.0 + SQLAlchemy
- **Autenticación:** JWT (python-jose + passlib)
- **LLM:** OpenRouter API (modelo configurable)
- **Despliegue:** AWS EC2 + Docker + Docker Compose
- **Pruebas:** pytest

## Estructura del proyecto

```
proyecto-recetas/
├── app/
│   ├── main.py              # Punto de entrada de la app
│   ├── config.py            # Variables de entorno (pydantic-settings)
│   ├── database.py          # Conexión SQLAlchemy
│   ├── models/
│   │   └── models.py        # Tablas: usuarios, ingredientes, recetas, calificaciones
│   ├── routers/
│   │   ├── auth.py          # Registro e inicio de sesión
│   │   ├── ingredientes.py  # CRUD de ingredientes
│   │   └── recetas.py       # Generación, historial, calificación, eliminación
│   ├── schemas/
│   │   └── schemas.py       # Modelos Pydantic (validación)
│   └── services/
│       ├── auth_service.py  # Hash de contraseñas, JWT
│       └── llm_service.py   # Integración con OpenRouter
├── tests/
│   ├── test_ingredientes.py
│   ├── test_llm_service.py
│   └── test_calificacion.py
├── static/
│   └── favicon.ico
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── pytest.ini
└── requirements.txt
```

## Modelo de base de datos

```
usuarios          ingredientes         recetas              calificaciones
---------         ------------         -------              --------------
id (PK)           id (PK)              id (PK)              id (PK)
nombre            nombre               nombre_plato         estrellas (1-5)
email (único)     cantidad             ingredientes_json    comentario
hashed_password   unidad               pasos_json           receta_id (FK)
created_at        usuario_id (FK) ──►  tiempo_estimado      usuario_id (FK)
     │                                 nivel_dificultad     created_at
     └──────────────────────────────►  usuario_id (FK)
                                       created_at
```

## Configuración local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/proyecto-recetas.git
cd proyecto-recetas
```

### 2. Crear archivo .env

```bash
cp .env.example .env
# Editar .env con tus credenciales reales
```

Las variables necesarias son:

```
DATABASE_URL=mysql+pymysql://usuario:contraseña@db:3306/recetas_db
SECRET_KEY=tu_clave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=mistralai/mistral-7b-instruct
MYSQL_ROOT_PASSWORD=root_password
MYSQL_USER=app_user
MYSQL_PASSWORD=app_password
```

> ⚠️ **Nunca subas el archivo `.env` al repositorio.** Está incluido en `.gitignore`.

### 3. Levantar con Docker Compose

```bash
docker compose up --build
```

La API estará disponible en `http://localhost:8000`  
Documentación Swagger: `http://localhost:8000/docs`

### 4. Ejecutar pruebas

```bash
# Con Docker
docker compose exec app pytest

# Local (con virtualenv activado)
pip install -r requirements.txt
pytest
```

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/auth/registro` | Registrar nuevo usuario |
| POST | `/auth/login` | Iniciar sesión (devuelve JWT) |
| GET | `/ingredientes/` | Listar ingredientes del usuario |
| POST | `/ingredientes/` | Agregar ingrediente |
| PUT | `/ingredientes/{id}` | Editar ingrediente |
| DELETE | `/ingredientes/{id}` | Eliminar ingrediente |
| POST | `/recetas/generar` | Generar receta con LLM |
| GET | `/recetas/` | Ver historial de recetas |
| GET | `/recetas/{id}` | Ver receta específica |
| DELETE | `/recetas/{id}` | Eliminar receta |
| POST | `/recetas/{id}/calificar` | Calificar receta (1-5 estrellas) |

## Despliegue en AWS

La aplicación está desplegada en una instancia EC2 con:
- Docker + Docker Compose instalados
- Puerto 8000 abierto en el Security Group
- Dominio apuntado mediante registro A en GoDaddy

URL de producción: `http://tu-dominio.com`  
Documentación en producción: `http://tu-dominio.com/docs`
