from sqlmodel import Table, Column, ForeignKey, INTEGER, FLOAT, NVARCHAR, DATE, DATETIME
from db.config import meta

Pagos = Table(
    'PAGOS',
    meta,
    Column('PAGO_ID', INTEGER, autoincrement=True, primary_key=True),
    Column('INSCRIPCION_ID', INTEGER, ForeignKey('INSCRIPCIONES.INSCRIPCION_ID', ondelete='SET NULL')),
    Column('FECHA', DATE),
    Column('MONTO', FLOAT),
    Column('SALDO', FLOAT),
    Column('STATUS', INTEGER),
    Column('ADD_DATE', DATETIME),
    Column('LAST_UPDATED_DATE', DATETIME)
)