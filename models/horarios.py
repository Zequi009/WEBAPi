from sqlmodel import Table, Column, ForeignKey, INTEGER, NVARCHAR, DATE, DATETIME
from db.config import meta

horarios = Table(
    'HORARIOS',
    meta,
    Column('HORARIO_ID', INTEGER, autoincrement=True, primary_key=True),
    Column('MATERIACARRERA_ID', INTEGER, ForeignKey('MATERIACARRERA.MATERIACARRERA_ID', ondelete='SET NULL')),
    Column('HORA_INICIO', NVARCHAR(20)),
    Column('HORA_FIN', NVARCHAR(20)),
    Column('DIA', NVARCHAR(20)),
    Column('STATUS', INTEGER),
    Column('ADD_DATE', DATETIME),
    Column('LAST_UPDATED_DATE', DATETIME)
)