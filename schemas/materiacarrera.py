from pydantic import BaseModel
from datetime import date, datetime

class Materiacarrera(BaseModel):
    MATERIACARRERA_ID: int | None
    MATERIA_ID:        int | None
    SEDECARRERA_ID:    int | None
    DOCENTE_ID:        int | None
    PRECEPTOR_ID:      int | None
    CICLO_LECTIVO:     int | None
    CURSO:             str | None
    REGULARIZABLE:     int | None
    STATUS:            int | None
    ADD_DATE:          datetime | None
    LAST_UPDATED_DATE: datetime | None

class MateriacarreraOUTPUT(Materiacarrera):
    #Incluye info relevante de materias, sede, carrera, profesor y preceptor.
    MATERIA_DESCRIPCION: str | None
    CARRERA_ANIO:        str | None
    CARRERA:             str | None
    SEDE:                str | None
    PROFESOR:            str | None
    PRECEPTOR:           str | None
    TURNO:               str | None