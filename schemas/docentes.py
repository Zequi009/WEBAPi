from pydantic import BaseModel
from datetime import date, datetime

class Docente(BaseModel):
    DOCENTE_ID:        int | None
    NOMBRE:            str | None
    APELLIDO:          str | None
    FECHA_NACIMIENTO:  date | None
    DNI:               str | None
    PASSWORD:          str | None
    TELEFONO:          str | None
    EMAIL:             str | None

    STATUS:            int | None
    ADD_DATE:          datetime | None
    LAST_UPDATED_DATE: datetime | None
