from fastapi import APIRouter, Depends, Response, HTTPException
from db.config import Session, Get_Session
from sqlmodel import select, or_
from models.horarios import horarios as t_horarios
from schemas.horarios import Horario
from datetime import datetime
from starlette.status import HTTP_204_NO_CONTENT

horarios = APIRouter(prefix="/API/HORARIOS")

@horarios.get('/')
def Get_Horarios(filtro: str = None, session: Session = Depends(Get_Session)):
    if not filtro:
        horarios = session.execute(select(t_horarios)).fetchall()
    else:
        horarios = session.execute(
            select(t_horarios).where(t_horarios.c.MATERIACARRERA_ID == filtro)).fetchall()
    return horarios


@horarios.get('/{id}')
def Get_Horario(id: int, session: Session = Depends(Get_Session)):
    horario = session.execute(select(t_horarios).where(t_horarios.c.HORARIO_ID == id)).first()
    if not horario:
        raise HTTPException(status_code=404, detail='No se encontró ningún horario para el ID especificado.')
    return horario

@horarios.post('/')
def Add_Horario(horario: Horario, session: Session = Depends(Get_Session)):
    new = { 
            "MATERIACARRERA_ID": horario.MATERIACARRERA_ID,
            "HORA_INICIO":       horario.HORA_INICIO,
            "HORA_FIN":          horario.HORA_FIN,
            "DIA":               horario.DIA
    }
    try:
        resultado = session.execute(t_horarios.insert().values(new))
        session.commit()
        id = resultado.inserted_primary_key[0]
        return session.execute(select(t_horarios).where(t_horarios.c.HORARIO_ID == id)).first()
    except Exception as e:
        error = f'No se pudo insertar el registro. Error: {e}'
        return error


@horarios.put('/{id}')
def Update_Horario(id: int, horario: Horario, session: Session = Depends(Get_Session)):
    old = session.execute(select(t_horarios).where(t_horarios.c.HORARIO_ID == id)).first()

    if old:
        new = {
            "MATERIACARRERA_ID": horario.MATERIACARRERA_ID,
            "HORA_INICIO":       horario.HORA_INICIO,
            "HORA_FIN":          horario.HORA_FIN,
            "DIA":               horario.DIA,
            "LAST_UPDATED_DATE": datetime.now()
        }

    try:
        session.execute(t_horarios.update().values(new).where(t_horarios.c.HORARIO_ID == id))
        session.commit()
        return session.execute(select(t_horarios).where(t_horarios.c.HORARIO_ID == id)).first()
    except Exception as e:
        error = f'No fue posible actualizar el registro. Error {e}.'
        return error
 


@horarios.delete('/{id}')
def Delete_Horario(id: int, session: Session = Depends(Get_Session)):
    horario = session.execute(select(t_horarios).where(t_horarios.c.HORARIO_ID == id)).first()
    if not horario:
        raise HTTPException(status_code=404,detail='No se encontró ningún horario para el ID especificado.')
    has_children = None #Hace falta en este? 
    if has_children:
        #Borrado lógico
        session.execute(t_horarios.update().values(STATUS=0).where(t_horarios.c.HORARIO_ID == id))
        session.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)
    session.execute(t_horarios.delete().where(t_horarios.c.HORARIO_ID == id))
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)

