from sqlmodel import Table, Column, INTEGER, NVARCHAR, DATETIME, ForeignKey
from db.config import meta

sedecarrera = Table(
    "SEDECARRERA",
    meta,
    Column("SEDECARRERA_ID", INTEGER, autoincrement=True, primary_key=True),
    Column("CARRERA_ID", INTEGER, ForeignKey('CARRERAS.CARRERA_ID', ondelete='SET NULL')),
    Column("SEDE_ID", INTEGER, ForeignKey('SEDES.SEDE_ID', ondelete='SET NULL')),
    Column("TURNO", NVARCHAR(10)),
    Column("CODIGO_CARRERA", NVARCHAR(10)),
    Column("STATUS", INTEGER),
    Column("ADD_DATE", DATETIME),
    Column("LAST_UPDATED_DATE", DATETIME)
)