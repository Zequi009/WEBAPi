from fastapi import APIRouter, Response, Depends, HTTPException
from starlette.status import HTTP_204_NO_CONTENT
from models.examenes import examenes as t_examenes
from db.config import Session, Get_Session
from schemas.examenes import Examen
from sqlmodel import select, or_
from datetime import datetime
examenes = APIRouter(prefix='/API/EXAMENES')

@examenes.get('/')
def Get_Exanenes(filtro: str = None, session: Session = Depends(Get_Session)):
    if not filtro:
        examenes = session.execute(select(t_examenes)).fetchall()
    else:
        examenes = session.execute(
            select(t_examenes).where(
            or_(
            str(t_examenes.c.MATERIACARRERA_ID) == filtro,
            t_examenes.c.FECHA.contains(filtro),
            t_examenes.c.DESCRIPCION.contains(filtro),
            str(t_examenes.c.ETAPA) == filtro,
            t_examenes.c.TIPO.contains(filtro)
            
            ))).fetchall()
    return examenes

@examenes.get('/{id}')
def Get_Examen(id: int, session: Session = Depends(Get_Session)):
    examen = session.execute(select(t_examenes).where(t_examenes.c.EXAMEN_ID == id)).first()
    if not examen:
        raise HTTPException(status_code=404, detail='No se encontró ningun examen para el ID especificado.')
    return examen

@examenes.post('/add')
def Add_Examen(examen: Examen, session: Session = Depends(Get_Session)):
    new = { 
            "MATERIACARRERA_ID": examen.MATERIACARRERA_ID,
            "FECHA":             examen.FECHA,
            "DESCRIPCION":       examen.DESCRIPCION,
            "ETAPA":             examen.ETAPA,
            "TIPO":              examen.TIPO
        }
    try:
        resultado = session.execute(t_examenes.insert().values(new))
        session.commit()
        id = resultado.inserted_primary_key[0]
        return session.execute(select(t_examenes).where(t_examenes.c.EXAMEN_ID == id)).first()
    except Exception as e:
        error = f'No se pudo insertar el registro. Error: {e}'
        return error

@examenes.put('/Update/{id}')
def Update_Examen(id: int, examen: Examen, session: Session = Depends(Get_Session)):
    old = session.execute(select(t_examenes).where(t_examenes.c.EXAMEN_ID == id)).first()

    if old:
        new = {
            "MATERIACARRERA_ID": examen.MATERIACARRERA_ID,
            "FECHA":             examen.FECHA,
            "DESCRIPCION":       examen.DESCRIPCION,
            "ETAPA":             examen.ETAPA,
            "TIPO":              examen.TIPO,
            "LAST_UPDATED_DATE": datetime.now()
        }

    try:
        session.execute(t_examenes.update().values(new).where(t_examenes.c.EXAMEN_ID == id))
        session.commit()
        return session.execute(select(t_examenes).where(t_examenes.c.EXAMEN_ID == id)).first()
    except Exception as e:
        error = f'No fue posible actualizar el registro. Error {e}.'
        return error

@examenes.delete('/Delete/{id}')
def Delete_Examen(id: int, session: Session = Depends(Get_Session)):
    examen = session.execute(select(t_examenes).where(t_examenes.c.EXAMEN_ID == id)).first()
    if not examen:
        raise HTTPException(status_code=404,detail='No se encontró ningun examen para el ID especificado.')
    has_children = None #-----------------verificar si hace falta 
    if has_children:
        #Borrado lógico
        session.execute(t_examenes.update().values(STATUS=0).where(t_examenes.c.EXAMEN_ID == id))
        session.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)
    session.execute(t_examenes.delete().where(t_examenes.c.EXAMEN_ID == id))
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)