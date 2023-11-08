from fastapi import APIRouter, Depends, Query, HTTPException, Response
from db.config import Get_Session, Session
from starlette.status import HTTP_204_NO_CONTENT
from sqlmodel import select
from datetime import datetime
from models.sedes import sedes as t_sedes
from models.sedecarrera import sedecarrera as t_scarrera
from schemas.sedes import Sede
sedes = APIRouter(prefix='/API/SEDES')

@sedes.get('/')
def Get_Sedes(desc: str = Query(None, description="desc es un parámetro opcional"), 
              session: Session = Depends(Get_Session)):
    '''Devuelve todas las sedes cargadas en la BD.'''
    if desc:
        return session.execute(select(t_sedes).where(t_sedes.c.DESCRIPCION == desc)).fetchall()
    else:
        return session.execute(select(t_sedes)).fetchall()
 

@sedes.get('/{id}')
def Get_Sede_by_Id(id: int, session: Session = Depends(Get_Session)):
    '''Devuelve un único registro, filtrando la búsqueda por el id proporcionado como argumento.'''
    sede = session.execute(select(t_sedes).where(t_sedes.c.SEDE_ID == id)).first()
    if sede:
        return sede
    raise HTTPException(status_code=404, detail="La sede especificada no existe.")


@sedes.post('/add')
def Add_Sede(sede: Sede, session: Session = Depends(Get_Session)):
    '''Recibe un objeto de tipo Sede y lo inserta en la tabla. No enviarle sede_id, status, add_date ni last_updated_date.'''
    nueva_sede = {
        "DESCRIPCION":    sede.DESCRIPCION,
        "TELEFONO":       sede.TELEFONO,
        "EMAIL":          sede.EMAIL,
        "DIRECCION":      sede.DIRECCION,
        "PISO":           sede.PISO,
        "DEPTO":          sede.DEPTO,
        "BARRIO":         sede.BARRIO,
        "LOCALIDAD":      sede.LOCALIDAD,
        "HORA_DESDE":     sede.HORA_DESDE,
        "HORA_HASTA":     sede.HORA_HASTA,
        "DIA_DESDE":      sede.DIA_DESDE,
        "DIA_HASTA":      sede.DIA_HASTA
    }
    resultado = session.execute(t_sedes.insert().values(nueva_sede))
    session.commit()
    id = resultado.inserted_primary_key[0]
    return session.execute(select(t_sedes).where(t_sedes.c.SEDE_ID == id)).first()

@sedes.put('/update/{id}')
def Update_Sede(sede: Sede, id: int, session: Session = Depends(Get_Session)):
    '''Actualiza los valores (toma todos excepto status y add_date) si el sede_id existe.'''
    old = session.execute(select(t_sedes).where(t_sedes.c.SEDE_ID == id)).first()
    new = {
        "DESCRIPCION":    sede.DESCRIPCION,
        "TELEFONO":       sede.TELEFONO,
        "EMAIL":          sede.EMAIL,
        "DIRECCION":      sede.DIRECCION,
        "PISO":           sede.PISO,
        "DEPTO":          sede.DEPTO,
        "BARRIO":         sede.BARRIO,
        "LOCALIDAD":      sede.LOCALIDAD,
        "HORA_DESDE":     sede.HORA_DESDE,
        "HORA_HASTA":     sede.HORA_HASTA,
        "DIA_DESDE":      sede.DIA_DESDE,
        "DIA_HASTA":      sede.DIA_HASTA,
        "LAST_UPDATED_DATE": datetime.now()
    }
    if not old:
        raise HTTPException(status_code=404, detail='La sede especificada no existe.')
    
    session.execute(t_sedes.update().values(new).where(t_sedes.c.SEDE_ID == id))
    session.commit()
    return session.execute(select(t_sedes).where(t_sedes.c.SEDE_ID == id)).first()


@sedes.delete('/delete/{id}')
def Delete_Sede(id: int, session: Session = Depends(Get_Session)):
    ''' Elimina si el registro todavía no está relacionado. Desactiva (status 0) si ya hay relaciones creadas.'''
    sede = session.execute(select(t_sedes).where(t_sedes.c.SEDE_ID == id)).first()
    has_children = session.execute(select(t_scarrera).where(t_scarrera.c.SEDE_ID == sede.SEDE_ID)).first()

    if sede:
        if has_children:
            session.execute(t_sedes.update().values(STATUS = 0).where(t_sedes.c.SEDE_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)
        else:
            session.execute(t_sedes.delete().where(t_sedes.c.SEDE_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail='La sede solicitada no existe.')