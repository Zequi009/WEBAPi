from fastapi import APIRouter, Response, HTTPException, Depends
from db.config import Session, Get_Session
from models.clases import clases as t_clases
from schemas.clases import Clase
from starlette.status import HTTP_204_NO_CONTENT
from sqlmodel import select, or_
from datetime import datetime

clases = APIRouter(prefix='/API/CLASES')

@clases.get('/')
def Get_Clases(filtro: str = None, session: Session = Depends(Get_Session)):
    if not filtro:
        clases = session.execute(select(t_clases)).fetchall()
    else:
        clases = session.execute(
            select(t_clases).where(
            or_(
            str(t_clases.c.MATERIACARRERA_ID) == filtro,
            t_clases.c.DESCRIPCION.contains(filtro),
            t_clases.c.OBSERVACIONES.contains(filtro)
            
            ))).fetchall()
    return clases

@clases.get('/{id}')
def Get_Clase(id: int, session: Session = Depends(Get_Session)):
    clase = session.execute(select(t_clases).where(t_clases.c.CLASE_ID == id)).first()
    if not clase:
        raise HTTPException(status_code=404, detail='No se encontró ninguna clase para el ID especificado.')
    return clase

@clases.post('/add')
def Add_Clase(clase: Clase, session: Session = Depends(Get_Session)):
    new = { 
            "MATERIACARRERA_ID": clase.MATERIACARRERA_ID,
            "FECHA":             clase.FECHA,
            "DESCRIPCION":       clase.DESCRIPCION,
            "OBSERVACIONES":     clase.OBSERVACIONES
        }
    try:
        resultado = session.execute(t_clases.insert().values(new))
        session.commit()
        id = resultado.inserted_primary_key[0]
        return session.execute(select(t_clases).where(t_clases.c.CLASE_ID == id)).first()
    except Exception as e:
        error = f'No se pudo insertar el registro. Error: {e}'
        return error

@clases.put('/Update/{id}')
def Update_Clase(id: int, clase: Clase, session: Session = Depends(Get_Session)):
    old = session.execute(select(t_clases).where(t_clases.c.CLASE_ID == id)).first()

    if old:
        new = {
            "MATERIACARRERA_ID": clase.MATERIACARRERA_ID,
            "FECHA":             clase.FECHA,
            "DESCRIPCION":       clase.DESCRIPCION,
            "OBSERVACIONES":     clase.OBSERVACIONES,
            "LAST_UPDATED_DATE": datetime.now()
        }

    try:
        session.execute(t_clases.update().values(new).where(t_clases.c.CLASE_ID == id))
        session.commit()
        return session.execute(select(t_clases).where(t_clases.c.CLASE_ID == id)).first()
    except Exception as e:
        error = f'No fue posible actualizar el registro. Error {e}.'
        return error

@clases.delete('/Delete/{id}')
def Delete_Clase(id: int, session: Session = Depends(Get_Session)):
    clase = session.execute(select(t_clases).where(t_clases.c.CLASE_ID == id)).first()
    if not clase:
        raise HTTPException(status_code=404,detail='No se encontró ninguna clase para el ID especificado.')
    has_children = None #Hace falta en este? 
    if has_children:
        #Borrado lógico
        session.execute(t_clases.update().values(STATUS=0).where(t_clases.c.CLASE_ID == id))
        session.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)
    session.execute(t_clases.delete().where(t_clases.c.CLASE_ID == id))
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)