from sqlmodel import Table, Column, ForeignKey, INTEGER, NVARCHAR, DATE, DATETIME
from db.config import meta

examenes = Table(
    'EXAMENES',
    meta,
    Column('EXAMEN_ID', INTEGER, autoincrement=True, primary_key=True),
    Column('MATERIACARRERA_ID', INTEGER, ForeignKey('MATERIACARRERA.MATERIACARRERA_ID', ondelete='SET NULL')),
    Column('FECHA', DATE),
    Column('DESCRIPCION', NVARCHAR(100)),
    Column('ETAPA', INTEGER),
    Column('TIPO', NVARCHAR(100)),
    Column('STATUS', INTEGER),
    Column('ADD_DATE', DATETIME),
    Column('LAST_UPDATED_DATE', DATETIME)
)