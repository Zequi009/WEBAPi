from pydantic import BaseModel
from datetime import datetime, date

class Examen(BaseModel):
    EXAMEN_ID:         int | None
    MATERIACARRERA_ID: int | None
    FECHA:             date | None
    DESCRIPCION:       str | None
    ETAPA:             int | None
    TIPO:              str | None
    STATUS:            int | None
    ADD_DATE:          datetime | None
    LAST_UPDATED_DATE: datetime | None