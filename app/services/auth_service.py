from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

# Servicio de autenticación
# Maneja el hash de contraseñas y la generación/validación de tokens JWT

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Genera un hash seguro de la contraseña usando bcrypt
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verifica si una contraseña plana coincide con el hash almacenado
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Crea un token JWT con tiempo de expiración configurable
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Decodifica y valida un token JWT, retorna el payload
def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])