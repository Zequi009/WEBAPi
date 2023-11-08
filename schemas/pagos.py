from pydantic import BaseModel
from datetime import date, datetime

class Pagos(BaseModel):
    PAGO_ID:                int | None
    INSCRIPCION_ID:         int | None
    FECHA:                 date | None
    MONTO:                float | None
    SALDO:                float | None

    STATUS:                 int | None
    ADD_DATE:          datetime | None
    LAST_UPDATED_DATE: datetime | None

class PagosOUTPUT(Pagos):
    ALUMNO_NOMBRE:          str | None
    ALUMNO_APELLIDO:        str | None
    ALUMNO_DNI:             str | None
    CARRERA:                str | None
    SEDE:                   str | None
    TURNO:                  str | None