from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class IngredienteCreate(BaseModel):
    nombre: str
    cantidad: Optional[str] = None
    unidad: Optional[str] = None

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("El nombre del ingrediente no puede estar vacío")
        return v.strip()

class IngredienteOut(BaseModel):
    id: int
    nombre: str
    cantidad: Optional[str]
    unidad: Optional[str]
    class Config:
        from_attributes = True

class RecetaOut(BaseModel):
    id: int
    nombre_plato: str
    ingredientes_json: str
    pasos_json: str
    tiempo_estimado: Optional[str]
    nivel_dificultad: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

class CalificacionCreate(BaseModel):
    estrellas: int
    comentario: Optional[str] = None

    @field_validator("estrellas")
    @classmethod
    def estrellas_validas(cls, v):
        if v < 1 or v > 5:
            raise ValueError("Las estrellas deben estar entre 1 y 5")
        return v

class CalificacionOut(BaseModel):
    id: int
    estrellas: int
    comentario: Optional[str]
    receta_id: int
    created_at: datetime
    class Config:
        from_attributes = True
