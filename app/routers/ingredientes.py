from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Ingrediente, Usuario
from app.schemas.schemas import IngredienteCreate, IngredienteOut
from app.routers.auth import get_current_user

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

@router.get("/", response_model=list[IngredienteOut])
def listar(db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return db.query(Ingrediente).filter(Ingrediente.usuario_id == user.id).all()

@router.post("/", response_model=IngredienteOut, status_code=201)
def crear(data: IngredienteCreate, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    ing = Ingrediente(**data.model_dump(), usuario_id=user.id)
    db.add(ing)
    db.commit()
    db.refresh(ing)
    return ing

@router.put("/{ing_id}", response_model=IngredienteOut)
def actualizar(ing_id: int, data: IngredienteCreate, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    ing = db.query(Ingrediente).filter(Ingrediente.id == ing_id, Ingrediente.usuario_id == user.id).first()
    if not ing:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    for k, v in data.model_dump().items():
        setattr(ing, k, v)
    db.commit()
    db.refresh(ing)
    return ing

@router.delete("/{ing_id}", status_code=204)
def eliminar(ing_id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    ing = db.query(Ingrediente).filter(Ingrediente.id == ing_id, Ingrediente.usuario_id == user.id).first()
    if not ing:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    db.delete(ing)
    db.commit()
