from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import HTTP_204_NO_CONTENT
from db.config import Session, Get_Session
from sqlmodel import or_,and_, select, distinct
from schemas.sedecarrera import SCarrera, SCarreraOUTPUT
from models.sedecarrera import sedecarrera as t_scarrera
from models.sedes import sedes as t_sedes
from models.carreras import carreras as t_carreras


sedecarrera = APIRouter(prefix='/API/SEDECARRERA')

@sedecarrera.get('/{id}')
def Get_SedeCarrera(id: int,session: Session = Depends(Get_Session)):
    '''Devuelve un único obj del schema SCarreraOUTPUT donde están todos los datos relevantes
    de las tres entidades (sedecarrera, sede, carrera)'''
    scarrera = SCarreraOUTPUT()

    sc = session.execute(select(t_scarrera, t_sedes, t_carreras).where(and_(
        t_scarrera.c.SEDECARRERA_ID == id,
        t_scarrera.c.SEDE_ID        == t_sedes.c.SEDE_ID,
        t_scarrera.c.CARRERA_ID     == t_carreras.c.CARRERA_ID
    ))).first()
   
    if sc:
        scarrera.SEDECARRERA_ID     = sc.SEDECARRERA_ID
        scarrera.TURNO              = sc.TURNO
        scarrera.CODIGO_CARRERA     = sc.CODIGO_CARRERA
        scarrera.STATUS             = sc.STATUS
        scarrera.ADD_DATE           = sc.ADD_DATE
        scarrera.LAST_UPDATED_DATE  = sc.LAST_UPDATED_DATE
        scarrera.TITULO_CARRERA     = sc.DESCRIPCION_1
        scarrera.PLAN_START_DATE    = sc.PLAN_START_DATE
        scarrera.PLAN_END_DATE      = sc.PLAN_END_DATE
        scarrera.SEDE_DESCRIPCION   = sc.DESCRIPCION
        scarrera.SEDE_DIRECCION     = sc.DIRECCION
        scarrera.SEDE_BARRIO        = sc.BARRIO
        scarrera.SEDE_LOCALIDAD     = sc.LOCALIDAD
        scarrera.SEDE_HORARIO_DESDE = sc.HORA_DESDE
        scarrera.SEDE_HORARIO_HASTA = sc.HORA_HASTA
        scarrera.SEDE_DIA_DESDE     = sc.DIA_DESDE
        scarrera.SEDE_DIA_HASTA     = sc.DIA_HASTA
    else:
        return 'No data found'

    return scarrera

@sedecarrera.get('/')
def GetSedeCarreras(filtro: str = None,session: Session = Depends(Get_Session)):
    '''Devuelve una lista de obj del schema SCarreraOUTPUT donde están todos los datos relevantes
    de las tres entidades (sedecarrera, sede, carrera)
    Se puede filtrar opcionalmente por TURNO (SCARRERA) Y DESCRIPCION (TANTO DE SEDES COMO CARRERAS)'''
    #Filtro va a buscar en TURNO (SCARRERA) Y DESCRIPCION (TANTO DE SEDES COMO CARRERAS).
    result = []
    if filtro:
        data = session.execute(
        select(t_scarrera,t_sedes,t_carreras)
        .where(
        and_(t_scarrera.c.SEDE_ID == t_sedes.c.SEDE_ID,
             t_scarrera.c.CARRERA_ID == t_carreras.c.CARRERA_ID,
             or_(t_carreras.c.DESCRIPCION.contains(filtro),
             t_sedes.c.DESCRIPCION.contains(filtro),
             t_scarrera.c.TURNO.contains(filtro)
             )))).fetchall()
    else:
        data = session.execute(
               select(t_scarrera,t_sedes,t_carreras)
               .where(
               and_(t_scarrera.c.SEDE_ID == t_sedes.c.SEDE_ID,
               t_scarrera.c.CARRERA_ID == t_carreras.c.CARRERA_ID)).distinct()).fetchall()
    
    for i in data:
        single = SCarreraOUTPUT()
        single.SEDECARRERA_ID     = i.SEDECARRERA_ID
        single.CARRERA_ID         = i.CARRERA_ID
        single.SEDE_ID            = i.SEDE_ID
        single.TURNO              = i.TURNO
        single.CODIGO_CARRERA     = i.CODIGO_CARRERA
        single.STATUS             = i.STATUS
        single.ADD_DATE           = i.ADD_DATE
        single.LAST_UPDATED_DATE  = i.LAST_UPDATED_DATE
        single.TITULO_CARRERA     = i.DESCRIPCION_1
        single.PLAN_START_DATE    = i.PLAN_START_DATE
        single.PLAN_END_DATE      = i.PLAN_END_DATE
        single.SEDE_DESCRIPCION   = i.DESCRIPCION
        single.SEDE_DIRECCION     = i.DIRECCION
        single.SEDE_BARRIO  	  = i.BARRIO
        single.SEDE_LOCALIDAD     = i.LOCALIDAD
        single.SEDE_HORARIO_DESDE = i.HORA_DESDE
        single.SEDE_HORARIO_HASTA = i.HORA_HASTA
        single.SEDE_DIA_DESDE     = i.DIA_DESDE
        single.SEDE_DIA_HASTA     = i.DIA_HASTA
        result.append(single)
    return result

@sedecarrera.post('/add')
def AddSedeCarrera(scarrera: SCarrera,session: Session = Depends(Get_Session)):
    '''Recibe un objeto de tipo SCarrera y lo inserta en la tabla. No enviarle sedecarrera_id, status, add_date ni last_updated_date.'''
    nueva_scarrera = {
        "SEDE_ID":          scarrera.SEDE_ID,
        "CARRERA_ID":       scarrera.CARRERA_ID,
        "TURNO":            scarrera.TURNO,
        "CODIGO_CARRERA":   scarrera.CODIGO_CARRERA
    }

    resultado = session.execute(t_scarrera.insert().values(nueva_scarrera))
    session.commit()
    id =  resultado.inserted_primary_key[0]
      
    return session.execute(select(t_scarrera).where(t_scarrera.c.SEDECARRERA_ID == id)).first()

@sedecarrera.put('/update/{id}')
def UpdateSedeCarrera(id: int, scarrera:SCarrera, session: Session = Depends(Get_Session)):
    '''Actualiza los valores (toma todos excepto status y add_date) si el id existe.'''
    old = session.execute(select(t_scarrera).where(t_scarrera.c.SEDECARRERA_ID == id)).first()
    new = {
        "SEDE_ID":          scarrera.SEDE_ID,
        "CARRERA_ID":       scarrera.CARRERA_ID,
        "TURNO":            scarrera.TURNO,
        "CODIGO_CARRERA":   scarrera.CODIGO_CARRERA,
        "LAST_UPDATED_DATE": datetime.now()
    }

    if not old:
        raise HTTPException(status_code=404, detail='La SedeCarrera especificada no existe.')
    
    session.execute(t_scarrera.update().values(new).where(t_scarrera.c.SEDECARRERA_ID == id))
    session.commit()

    return session.execute(select(t_scarrera).where(t_scarrera.c.SEDECARRERA_ID == id)).first()

@sedecarrera.put('/delete/{id}')
def DeleteSedeCarrera(id: int, session: Session = Depends(Get_Session)):
    '''Elimina si el registro todavía no está relacionado. 
    Desactiva (status = 0) si el registro ya tiene relaciones creadas.'''

    sedecarrera = session.execute(select(t_scarrera).where(t_scarrera.c.SEDECARRERA_ID == id)).first()
    has_children = False #Cuando esté hecha 'inscripciones', aplicar has_children filtrando si hay relaciones.

    if sedecarrera:
        if has_children:
            session.execute(t_scarrera.update().values(STATUS = 0).where(t_scarrera.c.SEDECARRERA_ID == id))
            session.commit()
            return Response(status_code = HTTP_204_NO_CONTENT)
        else:
            session.execute(t_scarrera.delete().where(t_scarrera.c.SEDECARRERA_ID == id))
            session.commit()
            return Response(status_code = HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail='La SedeCarrera solicitada no existe.')