from sqlmodel import Table, Column, INTEGER, NVARCHAR, DATE, DATETIME
from db.config import meta

sedes = Table('sedes',
              meta,
              Column('SEDE_ID', INTEGER, autoincrement=True, primary_key=True),
              Column('DESCRIPCION', NVARCHAR(100)),
              Column('TELEFONO', NVARCHAR(50)),
              Column('EMAIL', NVARCHAR(100)),
              Column('DIRECCION', NVARCHAR(100)),
              Column('PISO', INTEGER),
              Column('DEPTO', NVARCHAR(10)),
              Column('BARRIO', NVARCHAR(100)),
              Column('LOCALIDAD', NVARCHAR(100)),
              Column('HORA_DESDE', NVARCHAR(10)),
              Column('HORA_HASTA', NVARCHAR(10)),
              Column('DIA_DESDE', NVARCHAR(10)),
              Column('DIA_HASTA', NVARCHAR(10)),
              Column('STATUS', INTEGER),
              Column('ADD_DATE', DATETIME),
              Column('LAST_UPDATED_DATE', DATETIME),
)