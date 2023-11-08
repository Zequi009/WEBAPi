from sqlmodel import Table, Column, INTEGER, FLOAT, NVARCHAR, DATE, DATETIME, ForeignKey
from db.config import meta

materiacarrera = Table(
    'MATERIACARRERA',
    meta,
    Column('MATERIACARRERA_ID', INTEGER, autoincrement=True, primary_key=True),
    Column('MATERIA_ID', INTEGER, ForeignKey('MATERIAS.MATERIA_ID', ondelete='SET NULL')),
    Column('SEDECARRERA_ID', INTEGER, ForeignKey('SEDECARRERA.SEDECARRERA_ID', ondelete='SET NULL')),
    Column('DOCENTE_ID', INTEGER, ForeignKey('DOCENTES.DOCENTE_ID', ondelete='SET NULL')),
    Column('PRECEPTOR_ID', INTEGER, ForeignKey('PRECEPTORES.PRECEPTOR_ID', ondelete='SET NULL')),
    Column('CICLO_LECTIVO',INTEGER),
    Column('CURSO', NVARCHAR(10)),
    Column('REGULARIZABLE', INTEGER),

    Column('STATUS', INTEGER),
    Column('ADD_DATE', DATETIME),
    Column('LAST_UPDATED_DATE', DATETIME)
)

