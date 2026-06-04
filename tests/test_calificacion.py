import pytest
from pydantic import ValidationError
from app.schemas.schemas import CalificacionCreate

#Calificaciones
def test_calificacion_valida():
    cal = CalificacionCreate(estrellas=5)
    assert cal.estrellas == 5

#Error en caso de que la calificacion contenga un valor fuera de los establecidos
def test_calificacion_fuera_de_rango_alto():
    with pytest.raises(ValidationError):
        CalificacionCreate(estrellas=6)

def test_calificacion_fuera_de_rango_bajo():
    with pytest.raises(ValidationError):
        CalificacionCreate(estrellas=0)
