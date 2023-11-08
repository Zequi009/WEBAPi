from fastapi import APIRouter, Response, Depends, HTTPException
from starlette.status import HTTP_204_NO_CONTENT
from models.alumnos import alumnos as t_alumnos
from db.config import Session, Get_Session
from sqlmodel import select, delete, or_
from schemas.alumnos import Alumnos
from datetime import datetime




alumnos = APIRouter(prefix='/API/ALUMNOS')

@alumnos.get('/')
def Get_Alumnos(filtro: str = None, session: Session = Depends(Get_Session)):
    '''Busca alumnos. Si se pasa por parámetro un filtro, va a buscar por nombre, apellido o dni.
    Si no se pasa ningún filtro trae todos.'''
    if filtro:
        alumnos = session.execute(
            select(t_alumnos).where(
            or_(
            t_alumnos.c.NOMBRE.contains(filtro),
            t_alumnos.c.APELLIDO.contains(filtro),
            t_alumnos.c.DNI.contains(filtro)
            ) #fin or_
            ) #fin where
        ).fetchall()
        return alumnos
    else:
        alumnos = session.execute(select(t_alumnos)).fetchall()
        return alumnos
    
@alumnos.get('/{id}')
def Get_Alumno(id: int, session: Session = Depends(Get_Session)):
    alumno = session.execute(select(t_alumnos).where(t_alumnos.c.ALUMNO_ID == id)).first()

    if alumno: 
        return alumno
    else:
        raise HTTPException(status_code=404, detail='No se encontró ningún alumno para el ID especificado.')
    
@alumnos.post('/add/')
def Add_Alumno(alumno: Alumnos, session: Session = Depends(Get_Session)):
    '''Recibe un obj de tipo Alumnos y lo inserta en la tabla.'''
    nuevo_alumno = {
        "NOMBRE":                  alumno.NOMBRE,
        "APELLIDO":                alumno.APELLIDO,
        "FECHA_NACIMIENTO":        alumno.FECHA_NACIMIENTO,
        "DNI":                     alumno.DNI,
        "PASSWORD":                alumno.PASSWORD,
        "TELEFONO":                alumno.TELEFONO,
        "EMAIL":                   alumno.EMAIL,
        "DIRECCION":               alumno.DIRECCION,
        "PISO":                    alumno.PISO,
        "DEPTO":                   alumno.DEPTO,
        "BARRIO":                  alumno.BARRIO,
        "LOCALIDAD":               alumno.LOCALIDAD,
        "CONTACTO_EMERGENCIA":     alumno.CONTACTO_EMERGENCIA,
        "CONTACTO_EMERGENCIA_TEL": alumno.CONTACTO_EMERGENCIA_TEL
    }

    #en estos insert habria que agregar un try/except por las dudas.
    resultado =  session.execute(t_alumnos.insert().values(nuevo_alumno))
    session.commit()
    id = resultado.inserted_primary_key[0]
    return session.execute(select(t_alumnos).where(t_alumnos.c.ALUMNO_ID == id)).first()

@alumnos.put('/update/{id}')
def Update_Alumno(id: int, alumno: Alumnos, session: Session = Depends(Get_Session)):
    old = session.execute(select(t_alumnos).where(t_alumnos.c.ALUMNO_ID == id)).first()
    if old:
        new = {
        "NOMBRE":                  alumno.NOMBRE,
        "APELLIDO":                alumno.APELLIDO,
        "FECHA_NACIMIENTO":        alumno.FECHA_NACIMIENTO,
        "DNI":                     alumno.DNI,
        "PASSWORD":                alumno.PASSWORD,
        "TELEFONO":                alumno.TELEFONO,
        "EMAIL":                   alumno.EMAIL,
        "DIRECCION":               alumno.DIRECCION,
        "PISO":                    alumno.PISO,
        "DEPTO":                   alumno.DEPTO,
        "BARRIO":                  alumno.BARRIO,
        "LOCALIDAD":               alumno.LOCALIDAD,
        "CONTACTO_EMERGENCIA":     alumno.CONTACTO_EMERGENCIA,
        "CONTACTO_EMERGENCIA_TEL": alumno.CONTACTO_EMERGENCIA_TEL,
        "LAST_UPDATED_DATE":       datetime.now()
        }
        session.execute(t_alumnos.update().values(new).where(t_alumnos.c.ALUMNO_ID == id))
        session.commit()
        return session.execute(select(t_alumnos).where(t_alumnos.c.ALUMNO_ID == id)).first()
    else:
        raise HTTPException(status_code=404, detail='El alumno especificado no existe.')

@alumnos.put('/delete/{id}')
def Delete_Alumno(id: int, session: Session = Depends(Get_Session)):
    '''Elimina si el registro todavía no está relacionado. Desactiva (status 0) si ya hay relaciones creadas.'''
    alumno = session.execute(select(t_alumnos).where(t_alumnos.c.ALUMNO_ID == id)).first()
    has_children = False #session(execute(select(t_inscripciones).where(t_inscripciones.c.ALUMNO_ID == id))).first()

    if alumno: 
        if has_children:
            session.execute(t_alumnos.update().values(STATUS = 0).where(t_alumnos.c.ALUMNO_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)
        else:
            session.execute(delete(t_alumnos).where(t_alumnos.c.ALUMNO_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)
        
    raise HTTPException(status_code=404, detail='El alumno especificado no existe.')