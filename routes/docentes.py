from fastapi import APIRouter, HTTPException, Depends, Response
from starlette.status import HTTP_204_NO_CONTENT
from models.docentes import docentes as t_docentes
from sqlmodel import select, and_, or_
from db.config import Get_Session, Session
from schemas.docentes import Docente
from datetime import datetime


docentes = APIRouter(prefix="/API/DOCENTES")

@docentes.get('/')
def Get_Docentes(filtro: str = None, session: Session = Depends(Get_Session)):
    if not filtro:
        docentes = session.execute(select(t_docentes)).fetchall()
    else:
        docentes = session.execute(
            select(t_docentes).where(
            or_(
            t_docentes.c.NOMBRE.contains(filtro),
            t_docentes.c.APELLIDO.contains(filtro),
            t_docentes.c.DNI.contains(filtro)
            ))).fetchall()
    return docentes

@docentes.get('/{id}')
def Get_Docente(id: int, session: Session = Depends(Get_Session)):
    docente = session.execute(select(t_docentes).where(t_docentes.c.DOCENTE_ID == id)).first()
    if not docente:
        raise HTTPException(status_code=404, detail='No se encontró ningún docente para el ID especificado.')
    return docente
    

@docentes.post('/add')
def Add_Docente(docente: Docente, session: Session = Depends(Get_Session)):
    new = {

        "NOMBRE": docente.NOMBRE,
        "APELLIDO": docente.APELLIDO,
        "FECHA_NACIMIENTO": docente.FECHA_NACIMIENTO,
        "DNI": docente.DNI,
        "PASSWORD": docente.PASSWORD,
        "TELEFONO": docente.TELEFONO,
        "EMAIL": docente.EMAIL
    }
    try:
        resultado = session.execute(t_docentes.insert().values(new))
        session.commit()
        id = resultado.inserted_primary_key[0]
        return session.execute(select(t_docentes).where(t_docentes.c.DOCENTE_ID == id)).first()
    except Exception as e:
        error = 'No se pudo insertar el registro. Error: ', e
        return error

@docentes.put('/update/{id}')
def Update_Docente(id: int, docente: Docente, session: Session = Depends(Get_Session)):
    try: 
        old = session.execute(select(t_docentes).where(t_docentes.c.DOCENTE_ID == id)).first()
        if old:
            new = {
            "NOMBRE": docente.NOMBRE,
            "APELLIDO": docente.APELLIDO,
            "FECHA_NACIMIENTO": docente.FECHA_NACIMIENTO,
            "DNI": docente.DNI,
            "PASSWORD": docente.PASSWORD,
            "TELEFONO": docente.TELEFONO,
            "EMAIL": docente.EMAIL,
            "LAST_UPDATED_DATE": datetime.now()
            }

            session.execute(t_docentes.update().values(new).where(t_docentes.c.DOCENTE_ID == id))
            session.commit()
            return session.execute(select(t_docentes).where(t_docentes.c.DOCENTE_ID == id)).first()
        raise HTTPException(status_code=404, detail='No se encontró ningún docente para el ID especificado.')
    except Exception as e:
        error = f'No fue posible actualizar el registro. Error: {e}'
        return error

@docentes.delete('/delete/{id}')
def Delete_Docente(id: int, session: Session = Depends(Get_Session)):
    docente = session.execute(select(t_docentes).where(t_docentes.c.DOCENTE_ID == id)).first()
    if not docente:
        raise HTTPException(status_code=404,detail='No se encontró ningún docente para el ID especificado.')
    #has_children = session.execute(select(t_materiacarrera).where(t_materiacarrera.c.DOCENTE_ID == id)).first()
    has_children = None
    if has_children:
        #Borrado lógico
        session.execute(t_docentes.update().values(STATUS=0).where(t_docentes.c.DOCENTE_ID == id))
        session.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)
    session.execute(t_docentes.delete().where(t_docentes.c.DOCENTE_ID == id))
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)