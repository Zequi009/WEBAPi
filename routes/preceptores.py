from fastapi import APIRouter, HTTPException, Depends, Response
from starlette.status import HTTP_204_NO_CONTENT
from models.preceptores import preceptores as t_preceptores
from sqlmodel import select, or_
from db.config import Get_Session, Session
from schemas.preceptores import Preceptor
from datetime import datetime


preceptores = APIRouter(prefix="/API/PRECEPTORES")

@preceptores.get('/')
def Get_Preceptores(filtro: str = None, session: Session = Depends(Get_Session)):
    if not filtro:
        preceptores = session.execute(select(t_preceptores)).fetchall()
    else:
        preceptores = session.execute(
            select(t_preceptores).where(
            or_(
            t_preceptores.c.NOMBRE.contains(filtro),
            t_preceptores.c.APELLIDO.contains(filtro),
            t_preceptores.c.DNI.contains(filtro)
            ))).fetchall()
    return preceptores

@preceptores.get('/{id}')
def Get_Preceptor(id: int, session: Session = Depends(Get_Session)):
    preceptor = session.execute(select(t_preceptores).where(t_preceptores.c.PRECEPTOR_ID == id)).first()
    if not preceptor:
        raise HTTPException(status_code=404, detail='No se encontró ningún preceptor para el ID especificado.')
    return preceptor
    

@preceptores.post('/add')
def Add_Preceptor(preceptor: Preceptor, session: Session = Depends(Get_Session)):
    new = {

        "NOMBRE": preceptor.NOMBRE,
        "APELLIDO": preceptor.APELLIDO,
        "FECHA_NACIMIENTO": preceptor.FECHA_NACIMIENTO,
        "DNI": preceptor.DNI,
        "PASSWORD": preceptor.PASSWORD,
        "TELEFONO": preceptor.TELEFONO,
        "EMAIL": preceptor.EMAIL
    }
    try:
        resultado = session.execute(t_preceptores.insert().values(new))
        session.commit()
        id = resultado.inserted_primary_key[0]
        return session.execute(select(t_preceptores).where(t_preceptores.c.PRECEPTOR_ID == id)).first()
    except Exception as e:
        error = 'No se pudo insertar el registro. Error: ', e
        return error

@preceptores.put('/update/{id}')
def Update_Preceptor(id: int, preceptor: Preceptor, session: Session = Depends(Get_Session)):
    try: 
        old = session.execute(select(t_preceptores).where(t_preceptores.c.PRECEPTOR_ID == id)).first()
        if old:
            new = {
            "NOMBRE": preceptor.NOMBRE,
            "APELLIDO": preceptor.APELLIDO,
            "FECHA_NACIMIENTO": preceptor.FECHA_NACIMIENTO,
            "DNI": preceptor.DNI,
            "PASSWORD": preceptor.PASSWORD,
            "TELEFONO": preceptor.TELEFONO,
            "EMAIL": preceptor.EMAIL,
            "LAST_UPDATED_DATE": datetime.now()
            }

            session.execute(t_preceptores.update().values(new).where(t_preceptores.c.PRECEPTOR_ID == id))
            session.commit()
            return session.execute(select(t_preceptores).where(t_preceptores.c.PRECEPTOR_ID == id)).first()
        raise HTTPException(status_code=404, detail='No se encontró ningún preceptor para el ID especificado.')
    except Exception as e:
        error = f'No fue posible actualizar el registro. Error: {e}'
        return error

@preceptores.delete('/delete/{id}')
def Delete_Preceptor(id: int, session: Session = Depends(Get_Session)):
    preceptor = session.execute(select(t_preceptores).where(t_preceptores.c.PRECEPTOR_ID == id)).first()
    if not preceptor:
        raise HTTPException(status_code=404,detail='No se encontró ningún preceptor para el ID especificado.')
    #has_children = session.execute(select(t_materiacarrera).where(t_materiacarrera.c.PRECEPTOR_ID == id)).first()
    has_children = None
    if has_children:
        #Borrado lógico
        session.execute(t_preceptores.update().values(STATUS=0).where(t_preceptores.c.PRECEPTOR_ID == id))
        session.commit()
        return Response(status_code=HTTP_204_NO_CONTENT)
    session.execute(t_preceptores.delete().where(t_preceptores.c.PRECEPTOR_ID == id))
    session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)