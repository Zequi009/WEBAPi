from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import HTTP_204_NO_CONTENT
from db.config import Session, Get_Session
from sqlmodel import select
from models.carreras import carreras as t_carreras
from schemas.carreras import Carrera
from datetime import datetime

carreras = APIRouter(prefix='/API/CARRERAS')

@carreras.get('/')
def Get_Carreras(descripcion: str = None, session: Session = Depends(Get_Session)):
    '''Devuelve todas las carreras cargadas en la base de datos, sin ningún filtro.'''
    resultado = session.execute(select(t_carreras)).fetchall()
    if descripcion:
        resultado = session.execute(select(t_carreras).where(t_carreras.c.DESCRIPCION.contains(descripcion))).fetchall()
    return resultado

@carreras.get('/{id}')
def Get_Carrera(id: int, session: Session = Depends(Get_Session)):
    resultado = session.execute(select(t_carreras).where(t_carreras.c.CARRERA_ID == id)).first()
    if resultado:
        return resultado
    raise HTTPException(status_code=404, detail='La carrera especificada no existe.')

@carreras.post('/add')
def Add_Carrera(carrera: Carrera, session: Session = Depends(Get_Session)):
    '''Recibe un obj carrera y lo inserta en la BD. Devuelve el obj recién creado.'''
    new = {
    "DESCRIPCION":          carrera.DESCRIPCION,
    "PLAN_CARRERA":         carrera.PLAN_CARRERA,
    "PLAN_START_DATE":      carrera.PLAN_START_DATE,
    "PLAN_END_DATE":        carrera.PLAN_END_DATE
    }
    resultado = session.execute(t_carreras.insert().values(new))
    session.commit()
    id = resultado.inserted_primary_key[0]
    return session.execute(select(t_carreras).where(t_carreras.c.CARRERA_ID == id)).first()

@carreras.put('/update/{id}')
def Update_Carrera(id: int, carrera: Carrera, session: Session = Depends(Get_Session)):
    old = session.execute(select(t_carreras).where(t_carreras.c.CARRERA_ID == id)).first()
    if old:
        new = {
    "DESCRIPCION":          carrera.DESCRIPCION,
    "PLAN_CARRERA":         carrera.PLAN_CARRERA,
    "PLAN_START_DATE":      carrera.PLAN_START_DATE,
    "PLAN_END_DATE":        carrera.PLAN_END_DATE,
    "LAST_UPDATED_DATE":    datetime.now()       
        }
        session.execute(t_carreras.update().values(new).where(t_carreras.c.CARRERA_ID == id))
        session.commit()
        return session.execute(select(t_carreras).where(t_carreras.c.CARRERA_ID == id)).first()
    raise HTTPException(status_code=404, detail='La carrera solicitada no existe.')

@carreras.delete('/delete/{id}')
def Delete_Carrera(id: int, session: Session = Depends(Get_Session)):
    '''Elimina si el registro todavía no está relacionado. Desactiva (status 0) si ya hay relaciones creadas.'''
    carrera = session.execute(select(t_carreras).where(t_carreras.c.CARRERA_ID == id)).first()
    has_children = False#session.execute(select(t_sedecarrera.c.CARRERA_ID == id)).fetchall()
    
    if carrera:
        if has_children:
            session.execute(t_carreras.update().values(STATUS = 0).where(t_carreras.c.CARRERA_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)
        else:
            session.execute(t_carreras.delete().where(t_carreras.c.CARRERA_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail='La carrera solicitada no existe.')