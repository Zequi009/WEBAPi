from sqlmodel import Table, Column, ForeignKey, INTEGER, NVARCHAR, DATE, DATETIME
from db.config import meta

cursantes = Table(
    'CURSANTES',
    meta,
    Column('CURSANTE_ID', INTEGER, autoincrement=True, primary_key=True),
    Column('ALUMNO_ID', INTEGER, ForeignKey('ALUMNOS.ALUMNO_ID', ondelete='SET NULL')),
    Column('MATERIACARRERA_ID', INTEGER, ForeignKey('MATERIACARRERA.MATERIACARRERA_ID', ondelete='SET NULL')),
    Column('ESTADO_CURSADA', NVARCHAR(20)),
    Column('REGULARIDAD_END_DATE', DATE),
    Column('OBSERVACIONES', NVARCHAR(200)),
    Column('STATUS', INTEGER),
    Column('ADD_DATE', DATETIME),
    Column('LAST_UPDATED_DATE', DATETIME)
)