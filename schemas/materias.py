from pydantic import BaseModel
from datetime import date, datetime

class Materia(BaseModel):
    MATERIA_ID:             int | None
    DESCRIPCION:            str | None
    COD_RESOLUCION:         str | None
    CARRERA_ANIO:           int | None

    STATUS:                 int | None
    ADD_DATE:          datetime | None
    LAST_UPDATED_DATE: datetime | None

