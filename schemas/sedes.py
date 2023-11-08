from pydantic import BaseModel
from datetime import datetime

class Sede(BaseModel):
    SEDE_ID:        int | None
    DESCRIPCION:    str | None
    TELEFONO:       str | None
    EMAIL:          str | None
    DIRECCION:      str | None
    PISO:           int | None
    DEPTO:          str | None
    BARRIO:         str | None
    LOCALIDAD:      str | None
    HORA_DESDE:     str | None
    HORA_HASTA:     str | None
    DIA_DESDE:      str | None
    DIA_HASTA:      str | None
    STATUS:         int | None
    ADD_DATE:       datetime | None
    LAST_UPDATED_DATE:       datetime | None