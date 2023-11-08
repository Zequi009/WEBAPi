from sqlmodel import Table, Column, ForeignKey, INTEGER, FLOAT, NVARCHAR, DATE, DATETIME
from db.config import meta

clases = Table(
    'CLASES',
    meta,
    Column('CLASE_ID', INTEGER, autoincrement=True, primary_key=True),
    Column('MATERIACARRERA_ID', INTEGER, ForeignKey('MATERIACARRERA.MATERIACARRERA_ID', ondelete='SET NULL')),
    Column('FECHA', DATE),
    Column('DESCRIPCION', NVARCHAR(200)),
    Column('OBSERVACIONES', NVARCHAR(200)),
    Column('STATUS', INTEGER),
    Column('ADD_DATE', DATETIME),
    Column('LAST_UPDATED_DATE', DATETIME)
)