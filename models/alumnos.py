from sqlmodel import Table, Column, INTEGER, NVARCHAR, DATE, DATETIME
from db.config import meta

alumnos = Table(
    'ALUMNOS',
    meta,
    Column('ALUMNO_ID',INTEGER, primary_key=True, autoincrement=True),
    Column('NOMBRE', NVARCHAR(50)),
    Column('APELLIDO',NVARCHAR(50)),
    Column('FECHA_NACIMIENTO', DATE),
    Column('DNI', NVARCHAR(15)),
    Column('PASSWORD', NVARCHAR(100)),
    Column('TELEFONO',NVARCHAR(50)),
    Column('EMAIL',NVARCHAR(100)),
    Column('DIRECCION',NVARCHAR(100)),
    Column('PISO', INTEGER),
    Column('DEPTO', NVARCHAR(10)),
    Column('BARRIO', NVARCHAR(50)),
    Column('LOCALIDAD', NVARCHAR(100)),
    Column('CONTACTO_EMERGENCIA', NVARCHAR(100)),
    Column('CONTACTO_EMERGENCIA_TEL', NVARCHAR(50)),
    Column('STATUS', INTEGER),
    Column('ADD_DATE', DATETIME),
    Column('LAST_UPDATED_DATE', DATETIME)
)