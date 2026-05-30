import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Ingrediente, Receta, Usuario, Calificacion
from app.schemas.schemas import RecetaOut, CalificacionCreate, CalificacionOut
from app.services.llm_service import generate_recipe
from app.routers.auth import get_current_user

router = APIRouter(prefix="/recetas", tags=["Recetas"])

@router.post("/generar", response_model=RecetaOut, status_code=201)
async def generar(db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    ingredientes = db.query(Ingrediente).filter(Ingrediente.usuario_id == user.id).all()
    if not ingredientes:
        raise HTTPException(status_code=400, detail="No tienes ingredientes en tu inventario")
    nombres = [i.nombre for i in ingredientes]
    receta_data = await generate_recipe(nombres)
    receta = Receta(
        nombre_plato=receta_data["nombre_plato"],
        ingredientes_json=json.dumps(receta_data["ingredientes"], ensure_ascii=False),
        pasos_json=json.dumps(receta_data["pasos"], ensure_ascii=False),
        tiempo_estimado=receta_data.get("tiempo_estimado"),
        nivel_dificultad=receta_data.get("nivel_dificultad"),
        usuario_id=user.id,
    )
    db.add(receta)
    db.commit()
    db.refresh(receta)
    return receta

@router.get("/", response_model=list[RecetaOut])
def historial(db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return db.query(Receta).filter(Receta.usuario_id == user.id).order_by(Receta.created_at.desc()).all()

@router.get("/{receta_id}", response_model=RecetaOut)
def detalle(receta_id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    receta = db.query(Receta).filter(Receta.id == receta_id, Receta.usuario_id == user.id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta

@router.delete("/{receta_id}", status_code=204)
def eliminar(receta_id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    receta = db.query(Receta).filter(Receta.id == receta_id, Receta.usuario_id == user.id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    db.delete(receta)
    db.commit()

@router.post("/{receta_id}/calificar", response_model=CalificacionOut, status_code=201)
def calificar(receta_id: int, data: CalificacionCreate, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    cal = Calificacion(**data.model_dump(), receta_id=receta_id, usuario_id=user.id)
    db.add(cal)
    db.commit()
    db.refresh(cal)
    return cal
