from sqlmodel import Table, Column, ForeignKey, INTEGER, FLOAT, NVARCHAR, DATE, DATETIME
from db.config import meta

materias = Table(
    'MATERIAS',
    meta,
    Column('MATERIA_ID', INTEGER, autoincrement=True, primary_key=True),
    Column('DESCRIPCION', NVARCHAR(100)),
    Column('COD_RESOLUCION', NVARCHAR(10)),
    Column('CARRERA_ANIO', INTEGER),
    Column('STATUS', INTEGER),
    Column('ADD_DATE', DATETIME),
    Column('LAST_UPDATED_DATE', DATETIME)
)