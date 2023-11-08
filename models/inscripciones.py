from sqlmodel import Table, Column, INTEGER, FLOAT, NVARCHAR, DATE, DATETIME, ForeignKey
from db.config import meta

inscripciones = Table(
    'INSCRIPCIONES',
    meta,
    Column('INSCRIPCION_ID', INTEGER, autoincrement=True, primary_key=True),
    Column('ALUMNO_ID', INTEGER, ForeignKey('ALUMNOS.ALUMNO_ID', ondelete='SET NULL')),
    Column('SEDECARRERA_ID', INTEGER, ForeignKey('SEDECARRERA.SEDECARRERA_ID', ondelete='SET NULL')),
    Column('FOTOCOPIA_DOC_X2', INTEGER),
    Column('FOTOCOPIA_TITULO', INTEGER),
    Column('FOTOCOPIA_ANALITICO', INTEGER),
    Column('EXAMEN_NIVELATORIO',INTEGER),
    Column('COOPERADORA_TOTAL', FLOAT),
    Column('COOPERADORA_ESTADO', NVARCHAR(20)),
    Column('STATUS', INTEGER),
    Column('ADD_DATE', DATETIME),
    Column('LAST_UPDATED_DATE', DATETIME)
)