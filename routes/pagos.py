from fastapi import APIRouter,Response,HTTPException, Depends
from db.config import Session, Get_Session
from sqlmodel import select, and_, or_
from schemas.pagos import Pagos, PagosOUTPUT
from models.inscripciones import inscripciones as t_inscripciones
from models.sedecarrera import sedecarrera as t_scarrera
from models.carreras import carreras as t_carreras
from models.alumnos import alumnos as t_alumnos
from models.pagos import Pagos as t_pagos
from models.sedes import sedes as t_sedes
from starlette.status import HTTP_204_NO_CONTENT
from datetime import date, datetime

pagos = APIRouter(prefix='/API/PAGOS')

@pagos.get('/')
def Get_Pagos(filtro: str = None, session: Session = Depends(Get_Session)):
    result = []
    if filtro:
        pagos = session.execute(select(t_pagos, 
                                       t_inscripciones, 
                                       t_alumnos,
                                       t_scarrera,
                                       t_carreras, 
                                       t_sedes)
                .where(
                    and_(
                        t_pagos.c.INSCRIPCION_ID == t_inscripciones.c.INSCRIPCION_ID,
                        t_inscripciones.c.ALUMNO_ID == t_alumnos.c.ALUMNO_ID,
                        t_scarrera.c.CARRERA_ID == t_carreras.c.CARRERA_ID,
                        t_scarrera.c.SEDE_ID == t_sedes.c.SEDE_ID,
                        or_(
                        t_alumnos.c.NOMBRE.contains(filtro),
                        t_alumnos.c.APELLIDO.contains(filtro),
                        t_alumnos.c.DNI.contains(filtro),
                        t_carreras.c.DESCRIPCION.contains(filtro),
                        t_sedes.c.DESCRIPCION.contains(filtro)
                        )
                    )
                )).fetchall()
        
        
    else: 
        pagos = session.execute(
                                select(t_pagos, 
                                       t_inscripciones, 
                                       t_alumnos,
                                       t_scarrera,
                                       t_carreras, 
                                       t_sedes)
                .where(
                    and_(
                        t_pagos.c.INSCRIPCION_ID == t_inscripciones.c.INSCRIPCION_ID,
                        t_inscripciones.c.ALUMNO_ID == t_alumnos.c.ALUMNO_ID,
                        t_scarrera.c.CARRERA_ID == t_carreras.c.CARRERA_ID,
                        t_scarrera.c.SEDE_ID == t_sedes.c.SEDE_ID))).fetchall()
        
    for p in pagos:
        single = PagosOUTPUT()
        single.PAGO_ID = p.PAGO_ID

        single.INSCRIPCION_ID= p.INSCRIPCION_ID
        single.FECHA= p.FECHA
        single.MONTO= p.MONTO
        single.SALDO= p.SALDO

        single.STATUS= p.STATUS
        single.ADD_DATE= p.ADD_DATE
        single.LAST_UPDATED_DATE= p.LAST_UPDATED_DATE

        single.ALUMNO_NOMBRE=p.NOMBRE
        single.ALUMNO_APELLIDO=p.APELLIDO
        single.ALUMNO_DNI=p.DNI
        single.CARRERA=p.DESCRIPCION
        single.SEDE= p.DESCRIPCION_1
        single.TURNO= p.TURNO

        result.append(single)
    
    return result

@pagos.get('/{id}')
def Get_Pago(id: int, session: Session = Depends(Get_Session)):
    p = session.execute(
        select(t_pagos, 
               t_inscripciones, 
               t_alumnos,
               t_scarrera,
               t_carreras, 
               t_sedes)
        .where(
                t_pagos.c.PAGO_ID == id,
                t_pagos.c.INSCRIPCION_ID == t_inscripciones.c.INSCRIPCION_ID,
                t_inscripciones.c.ALUMNO_ID == t_alumnos.c.ALUMNO_ID,
                t_scarrera.c.CARRERA_ID == t_carreras.c.CARRERA_ID,
                t_scarrera.c.SEDE_ID == t_sedes.c.SEDE_ID
               )).first()

    if p:
        single = PagosOUTPUT()
        single.PAGO_ID = p.PAGO_ID

        single.INSCRIPCION_ID= p.INSCRIPCION_ID
        single.FECHA= p.FECHA
        single.MONTO= p.MONTO
        single.SALDO= p.SALDO

        single.STATUS= p.STATUS
        single.ADD_DATE= p.ADD_DATE
        single.LAST_UPDATED_DATE= p.LAST_UPDATED_DATE

        single.ALUMNO_NOMBRE=p.NOMBRE
        single.ALUMNO_APELLIDO=p.APELLIDO
        single.ALUMNO_DNI=p.DNI
        single.CARRERA=p.DESCRIPCION
        single.SEDE= p.DESCRIPCION_1
        single.TURNO= p.TURNO
    
        return single
    else: 
        raise HTTPException(status_code=404, detail='El pago solicitado no existe.')

@pagos.post('/add')
def Add_Pago(pago: Pagos, session: Session = Depends(Get_Session)):
    new = {
    "INSCRIPCION_ID":pago.INSCRIPCION_ID,
    "FECHA":         pago.FECHA,
    "MONTO":         pago.MONTO,
    "SALDO":         pago.SALDO 
    }

    resultado = session.execute(t_pagos.insert().values(new))
    session.commit()
    id = resultado.inserted_primary_key[0]
    return session.execute(select(t_pagos).where(t_pagos.c.PAGO_ID == id)).first()

@pagos.put('/update/{id}')
def Update_Pago(id: int, pago: Pagos, session: Session = Depends(Get_Session)):
    old = session.execute(select(t_pagos).where(t_pagos.c.PAGO_ID == id)).first()
    if old:
        new = {
                "INSCRIPCION_ID":    pago.INSCRIPCION_ID,
                "FECHA":             pago.FECHA,
                "MONTO":             pago.MONTO,
                "SALDO":             pago.SALDO,
                "LAST_UPDATED_DATE": datetime.now()       
        }
        session.execute(t_pagos.update().values(new).where(t_pagos.c.PAGO_ID == id))
        session.commit()
        return session.execute(select(t_pagos).where(t_pagos.c.PAGO_ID == id)).first()
    else:
        raise HTTPException(status_code=404, detail='El pago solicitado no existe.')

@pagos.delete('/delete/{id}')
def Delete_Pago(id:int, session: Session = Depends(Get_Session)):
    pago = session.execute(select(t_pagos).where(t_pagos.c.PAGO_ID == id)).first()
    is_related = False #Corroborar si hay inscripciones que lo tengan

    if pago:
        if is_related:
            session.execute(t_pagos.update().values(STATUS=0).where(t_pagos.c.PAGO_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)
        else:
            session.execute(t_pagos.delete().where(t_pagos.c.PAGO_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='El pago solicitado no existe.')