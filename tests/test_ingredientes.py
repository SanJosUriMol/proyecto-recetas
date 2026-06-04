import pytest
from pydantic import ValidationError
from app.schemas.schemas import IngredienteCreate

#Ingredientes, cantidad y unidades de estos para las recetas

def test_ingrediente_nombre_valido():
    ing = IngredienteCreate(nombre="Tomate", cantidad="2", unidad="unidades")
    assert ing.nombre == "Tomate"

def test_ingrediente_nombre_vacio_falla():
    with pytest.raises(ValidationError):
        IngredienteCreate(nombre="   ")

def test_ingrediente_nombre_strip():
    ing = IngredienteCreate(nombre="  Cebolla  ")
    assert ing.nombre == "Cebolla"

def test_ingrediente_sin_cantidad_opcional():
    ing = IngredienteCreate(nombre="Sal")
    assert ing.cantidad is None
    assert ing.unidad is None
