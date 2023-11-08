from pydantic import BaseModel
from datetime import date, datetime

class Cursante(BaseModel):
    CURSANTE_ID:          int | None
    ALUMNO_ID:            int | None 
    MATERIACARRERA_ID:    int | None
    ESTADO_CURSADA:       str | None
    REGULARIDAD_END_DATE: date | None
    OBSERVACIONES:        str | None
    STATUS:               int | None
    ADD_DATE:             datetime | None
    LAST_UPDATED_DATE:    datetime | None

class CursanteOUTPUT(Cursante):
    #Agrego info de alumno
    NOMBRE: str | None
    APELLIDO: str | None

    #Agrego info de Materiacarrera (año lectivo)
    CICLO_LECTIVO: int | None

    #Agrego info de materia.
    MATERIA: str | None