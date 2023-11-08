from pydantic import BaseModel
from datetime import date, datetime

class Alumnos(BaseModel):
    ALUMNO_ID:                  int | None
    NOMBRE:                     str | None
    APELLIDO:                   str | None
    FECHA_NACIMIENTO:          date | None
    DNI:                        str | None
    PASSWORD:                   str | None
    TELEFONO:                   str | None
    EMAIL:                      str | None
    DIRECCION:                  str | None
    PISO:                       int | None
    DEPTO:                      str | None
    BARRIO:                     str | None
    LOCALIDAD:                  str | None
    CONTACTO_EMERGENCIA:        str | None
    CONTACTO_EMERGENCIA_TEL:    str | None

    STATUS:                     int | None
    ADD_DATE:              datetime | None
    LAST_UPDATED_DATE:     datetime | None 

