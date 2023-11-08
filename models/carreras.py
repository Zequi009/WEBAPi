from sqlmodel import Table, Column, INTEGER, NVARCHAR, DATE, DATETIME
from db.config import meta

carreras = Table(
    'CARRERAS',
    meta,
    Column('CARRERA_ID', INTEGER, primary_key=True, autoincrement=True),
    Column('DESCRIPCION', NVARCHAR(100)),
    Column('PLAN_CARRERA', NVARCHAR(50)),
    Column('PLAN_START_DATE', DATE),
    Column('PLAN_END_DATE', DATE),
    Column('STATUS', INTEGER),
    Column('ADD_DATE', DATETIME),
    Column('LAST_UPDATED_DATE', DATETIME)
)