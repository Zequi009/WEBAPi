from pydantic import BaseModel
from datetime import date, datetime

class Inscripciones(BaseModel):
    INSCRIPCION_ID:          int | None
    ALUMNO_ID:               int | None
    SEDECARRERA_ID:          int | None
    FOTOCOPIA_DOC_X2:        int | None
    FOTOCOPIA_TITULO:        int | None
    FOTOCOPIA_ANALITICO:     int | None
    EXAMEN_NIVELATORIO:      int | None 
    COOPERADORA_TOTAL:     float | None
    COOPERADORA_ESTADO:      str | None

    STATUS:                  int | None
    ADD_DATE:           datetime | None
    LAST_UPDATED_DATE:  datetime | None

class InscripcionesOUTPUT(Inscripciones):
     #Sacado de Alumnos.
     ALUMNO_NOMBRE:   str | None
     ALUMNO_APELLIDO: str | None
     ALUMNO_DNI:      str | None
     ALUMNO_EMAIL:    str | None
     ALUMNO_TELEFONO: str | None

    #Sacado de SCarreraOutput
     CARRERA_TITULO:  str | None
     CARRERA_TURNO:   str | None
     SEDE_NOMBRE:     str | None