from pydantic import BaseModel
from datetime import date, datetime

class Carrera(BaseModel):
    CARRERA_ID:         int | None
    DESCRIPCION:        str | None
    PLAN_CARRERA:       str | None
    PLAN_START_DATE:    date | None
    PLAN_END_DATE:      date | None
    STATUS:             int | None
    ADD_DATE:           datetime | None
    LAST_UPDATED_DATE:  datetime | None