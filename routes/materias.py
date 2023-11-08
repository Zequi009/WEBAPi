from fastapi import APIRouter,Response, HTTPException, Depends
from datetime import date, datetime
from sqlmodel import select, delete, or_, and_
from db.config import Session, Get_Session
from starlette.status import HTTP_204_NO_CONTENT
from schemas.inscripciones import Inscripciones, InscripcionesOUTPUT
from models.materias import materias as t_materias
from schemas.materias import Materia

materias = APIRouter(prefix="/API/MATERIAS")

@materias.get('/')
def Get_Materias(filtro: str = None, session: Session = Depends(Get_Session)):
    '''Busca materias. Si se pasa por parámetro un filtro, va a buscar por nombre, apellido o dni.
    Si no se pasa ningún filtro trae todos.'''
    if filtro:
        materias = session.execute(
            select(t_materias).where(
            or_(
            t_materias.c.DESCRIPCION.contains(filtro),
            t_materias.c.COD_RESOLUCION.contains(filtro),
            t_materias.c.CARRERA_ANIO.contains(filtro)
            ) #fin or_
            ) #fin where
        ).fetchall()
        return materias
    else:
        materias = session.execute(select(t_materias)).fetchall()
        return materias

@materias.get('/{id}')
def Get_Materia(id:int, session: Session = Depends(Get_Session)):
    materia = session.execute(select(t_materias).where(t_materias.c.MATERIA_ID == id)).first()
    if not materia:
        raise HTTPException(status_code=404, detail='No se encontró ninga materia para el ID especificado.')
    return materia

@materias.post('/add')
def Add_Materia(materia: Materia, session: Session = Depends(Get_Session)):
    new = {
            "DESCRIPCION": materia.DESCRIPCION,
            "COD_RESOLUCION": materia.COD_RESOLUCION,
            "CARRERA_ANIO": materia.CARRERA_ANIO
        }

    try:
        resultado = session.execute(t_materias.insert().values(new))
        session.commit()
        id = resultado.inserted_primary_key[0]
        return session.execute(select(t_materias).where(t_materias.c.MATERIA_ID == id)).first()
    except Exception as e:
        error = f'No se pudo insertar el registro. Error: {e}.'
        return error
    

@materias.put('/update/{id}')
def Update_Materia(id: int, materia: Materia, session: Session = Depends(Get_Session)):
    try:
        old = session.execute(select(t_materias).where(t_materias.c.MATERIA_ID == id)).first()
        
        if old:
            new = {
            "DESCRIPCION":      materia.DESCRIPCION,
            "COD_RESOLUCION":   materia.COD_RESOLUCION,
            "CARRERA_ANIO":     materia.CARRERA_ANIO,
            "LAST_UPDATED_DATE": datetime.now()
            }
            session.execute(t_materias.update().values(new).where(t_materias.c.MATERIA_ID == id))
            session.commit()
            return session.execute(select(t_materias).where(t_materias.c.MATERIA_ID == id)).first()
        else:
            raise HTTPException(status_code=404, detail='La materia solicitada no existe.')
    except Exception as e:
        error = f'No se pudo actualizar el registro. Error: {e}.'
        return error

@materias.delete('/delete/{id}')
def Delete_Materia(id: int, session: Session = Depends(Get_Session)):
    materia = session.execute(select(t_materias).where(t_materias.c.MATERIA_ID == id)).first()
    is_related = False #Corroborar si hay materiaxcarrera que la tengan

    if materia:
        if is_related:
            session.execute(t_materias.update().values(STATUS=0).where(t_materias.c.MATERIA_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)
        else:
            session.execute(t_materias.delete().where(t_materias.c.MATERIA_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='La materia solicitada no existe.')