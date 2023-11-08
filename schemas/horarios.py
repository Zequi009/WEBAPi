from pydantic import BaseModel
from datetime import datetime

class Horario(BaseModel):
    HORARIO_ID:        int | None
    MATERIACARRERA_ID: int | None
    HORA_INICIO:       str | None
    HORA_FIN:          str | None
    DIA:               str | None
    STATUS:            int | None
    ADD_DATE:          datetime | None
    LAST_UPDATED_DATE: datetime | None
