from sqlmodel import Table, Column, INTEGER, NVARCHAR, DATE, DATETIME
from db.config import meta

preceptores = Table(
    'PRECEPTORES',
    meta,
    Column('PRECEPTOR_ID',INTEGER, primary_key=True, autoincrement=True),
    Column('NOMBRE', NVARCHAR(50)),
    Column('APELLIDO',NVARCHAR(50)),
    Column('FECHA_NACIMIENTO', DATE),
    Column('DNI', NVARCHAR(15)),
    Column('PASSWORD', NVARCHAR(100)),
    Column('TELEFONO',NVARCHAR(50)),
    Column('EMAIL',NVARCHAR(100)),
    Column('STATUS', INTEGER),
    Column('ADD_DATE', DATETIME),
    Column('LAST_UPDATED_DATE', DATETIME)
)