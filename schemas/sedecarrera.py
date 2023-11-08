from pydantic import BaseModel
from datetime import datetime, date

class SCarrera(BaseModel):
    SEDECARRERA_ID:                    int | None
    CARRERA_ID:                        int | None
    SEDE_ID:                           int | None
    TURNO:                             int | None
    CODIGO_CARRERA:                    int | None
    STATUS:                            int | None
    ADD_DATE:                     datetime | None   
    LAST_UPDATED_DATE:            datetime | None



class SCarreraOUTPUT(SCarrera):
    #VALORES ADICIONALES DE CARRERA:
    TITULO_CARRERA:                    str | None
    PLAN_START_DATE:                  date | None
    PLAN_END_DATE:                    date | None
    #VALORES ADICIONALES DE SEDE:
    SEDE_DESCRIPCION:                  str | None
    SEDE_DIRECCION:                    str | None
    SEDE_BARRIO:                       str | None
    SEDE_LOCALIDAD:                    str | None
    SEDE_HORARIO_DESDE:                str | None
    SEDE_HORARIO_HASTA:                str | None
    SEDE_DIA_DESDE:                    str | None
    SEDE_DIA_HASTA:                    str | None
