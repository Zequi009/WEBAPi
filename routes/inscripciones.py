from fastapi import APIRouter,Response, HTTPException, Depends
from datetime import date, datetime
from sqlmodel import select, delete, or_, and_
from db.config import Session, Get_Session
from starlette.status import HTTP_204_NO_CONTENT
from schemas.inscripciones import Inscripciones, InscripcionesOUTPUT
from models.inscripciones import inscripciones as t_inscripciones
from models.sedecarrera import sedecarrera as t_scarrera
from models.carreras import carreras as t_carreras
from models.alumnos import alumnos as t_alumnos
from models.sedes import sedes as t_sedes


inscripciones = APIRouter(prefix='/API/INSCRIPCIONES')

@inscripciones.get('/')
def Get_Inscripciones(filtro: str = None, session: Session = Depends(Get_Session)):
    ''' Devuelve una lista de obj del schema InscripcionesOUTPUT donde están todos los datos relevantes
    de las tres entidades (Inscripciones, Alumnos, SedeCarreras)
    Se puede filtrar opcionalmente por TURNO, SEDE, TITULO, ALUMNO'''
    result = []
    if filtro:
        data = session.execute(select(t_inscripciones, t_alumnos, t_scarrera, t_carreras, t_sedes)
        .where(
            and_(
            t_inscripciones.c.ALUMNO_ID == t_alumnos.c.ALUMNO_ID,
            t_inscripciones.c.SEDECARRERA_ID == t_scarrera.c.SEDECARRERA_ID,
            t_scarrera.c.CARRERA_ID == t_carreras.c.CARRERA_ID,
            t_scarrera.c.SEDE_ID == t_sedes.c.SEDE_ID,
            or_(
            t_alumnos.c.NOMBRE.contains(filtro),
            t_carreras.c.DESCRIPCION.contains(filtro),
            t_scarrera.c.TURNO.contains(filtro),
            t_sedes.c.DESCRIPCION.contains(filtro)
            )#fin or_
            )#fin and_
        )#fin where                               
        ).fetchall()
    else:
        data = session.execute(select(
            t_inscripciones, 
            t_alumnos,
            t_scarrera, 
            t_carreras, 
            t_sedes
            ).where(
            and_(
            t_inscripciones.c.ALUMNO_ID == t_alumnos.c.ALUMNO_ID,
            t_inscripciones.c.SEDECARRERA_ID == t_scarrera.c.SEDECARRERA_ID,
            t_scarrera.c.CARRERA_ID == t_carreras.c.CARRERA_ID,
            t_scarrera.c.SEDE_ID == t_sedes.c.SEDE_ID
            )
            )).fetchall()
        
    for i in data:
        single = InscripcionesOUTPUT()
        single.INSCRIPCION_ID      =i.INSCRIPCION_ID
        single.ALUMNO_ID           =i.ALUMNO_ID
        single.SEDECARRERA_ID      =i.SEDECARRERA_ID
        single.FOTOCOPIA_DOC_X2    =i.FOTOCOPIA_DOC_X2
        single.FOTOCOPIA_TITULO    =i.FOTOCOPIA_TITULO
        single.FOTOCOPIA_ANALITICO =i.FOTOCOPIA_ANALITICO
        single.EXAMEN_NIVELATORIO  =i.EXAMEN_NIVELATORIO
        single.COOPERADORA_TOTAL   =i.COOPERADORA_TOTAL
        single.COOPERADORA_ESTADO  =i.COOPERADORA_ESTADO

        single.STATUS              =i.STATUS
        single.ADD_DATE            =i.ADD_DATE
        single.LAST_UPDATED_DATE   =i.LAST_UPDATED_DATE

        #Sacado de Alumnos.
        single.ALUMNO_NOMBRE       =i.NOMBRE
        single.ALUMNO_APELLIDO     =i.APELLIDO
        single.ALUMNO_DNI          =i.DNI
        single.ALUMNO_EMAIL        =i.EMAIL
        single.ALUMNO_TELEFONO     =i.TELEFONO

        #Sacado de SCarreraOutput
        single.CARRERA_TITULO      =i.DESCRIPCION
        single.CARRERA_TURNO       =i.TURNO
        single.SEDE_NOMBRE         =i.DESCRIPCION_1
        result.append(single)
    return result

@inscripciones.get('/{id}')
def Get_Inscripcion(id:int, session: Session = Depends(Get_Session)):
    i = session.execute(select(t_inscripciones, t_alumnos, t_scarrera, t_carreras, t_sedes)
                .where(
        and_(
            t_inscripciones.c.INSCRIPCION_ID == id,
            t_inscripciones.c.ALUMNO_ID == t_alumnos.c.ALUMNO_ID,
            t_inscripciones.c.SEDECARRERA_ID == t_scarrera.c.SEDECARRERA_ID,
            t_scarrera.c.CARRERA_ID == t_carreras.c.CARRERA_ID,
            t_scarrera.c.SEDE_ID == t_sedes.c.SEDE_ID
            ))).first()
    if i:
        single = InscripcionesOUTPUT()
        single.INSCRIPCION_ID      =i.INSCRIPCION_ID
        single.ALUMNO_ID           =i.ALUMNO_ID
        single.SEDECARRERA_ID      =i.SEDECARRERA_ID
        single.FOTOCOPIA_DOC_X2    =i.FOTOCOPIA_DOC_X2
        single.FOTOCOPIA_TITULO    =i.FOTOCOPIA_TITULO
        single.FOTOCOPIA_ANALITICO =i.FOTOCOPIA_ANALITICO
        single.EXAMEN_NIVELATORIO  =i.EXAMEN_NIVELATORIO
        single.COOPERADORA_TOTAL   =i.COOPERADORA_TOTAL
        single.COOPERADORA_ESTADO  =i.COOPERADORA_ESTADO

        single.STATUS              =i.STATUS
        single.ADD_DATE            =i.ADD_DATE
        single.LAST_UPDATED_DATE   =i.LAST_UPDATED_DATE

        #Sacado de Alumnos.
        single.ALUMNO_NOMBRE       =i.NOMBRE
        single.ALUMNO_APELLIDO     =i.APELLIDO
        single.ALUMNO_DNI          =i.DNI
        single.ALUMNO_EMAIL        =i.EMAIL
        single.ALUMNO_TELEFONO     =i.TELEFONO

        #Sacado de SCarreraOutput
        single.CARRERA_TITULO      =i.DESCRIPCION
        single.CARRERA_TURNO       =i.TURNO
        single.SEDE_NOMBRE         =i.DESCRIPCION_1
        return single
    else: 
        raise HTTPException(status_code=404, detail='No se encontraron inscripciones con el ID solicitado.')

@inscripciones.post('/add')
def Add_Inscripcion(inscripcion: Inscripciones, session: Session = Depends(Get_Session)):
    new = {
    "ALUMNO_ID":            inscripcion.ALUMNO_ID,
    "SEDECARRERA_ID":       inscripcion.SEDECARRERA_ID,
    "FOTOCOPIA_DOC_X2":     inscripcion.FOTOCOPIA_DOC_X2,
    "FOTOCOPIA_TITULO":     inscripcion.FOTOCOPIA_TITULO,
    "FOTOCOPIA_ANALITICO":  inscripcion.FOTOCOPIA_ANALITICO,
    "EXAMEN_NIVELATORIO":   inscripcion.EXAMEN_NIVELATORIO,
    "COOPERADORA_TOTAL":    inscripcion.COOPERADORA_TOTAL,
    "COOPERADORA_ESTADO":   inscripcion.COOPERADORA_ESTADO
    }

    result = session.execute(t_inscripciones.insert().values(new))
    session.commit()
    id = result.inserted_primary_key[0]

    return session.execute(select(t_inscripciones).where(t_inscripciones.c.INSCRIPCION_ID == id)).first()

@inscripciones.put('/update/{id}')
def Update_Inscripcion(id:int, inscripcion: Inscripciones, session: Session = Depends(Get_Session)):
    old = session.execute(select(t_inscripciones).where(t_inscripciones.c.INSCRIPCION_ID == id)).first()

    if old:
        new = {
        "SEDECARRERA_ID":       inscripcion.SEDECARRERA_ID,
        "FOTOCOPIA_DOC_X2":     inscripcion.FOTOCOPIA_DOC_X2,
        "FOTOCOPIA_TITULO":     inscripcion.FOTOCOPIA_TITULO,
        "FOTOCOPIA_ANALITICO":  inscripcion.FOTOCOPIA_ANALITICO,
        "EXAMEN_NIVELATORIO":   inscripcion.EXAMEN_NIVELATORIO,
        "COOPERADORA_TOTAL":    inscripcion.COOPERADORA_TOTAL,
        "COOPERADORA_ESTADO":   inscripcion.COOPERADORA_ESTADO,
        "LAST_UPDATED_DATE":    datetime.now()
        }
        session.execute(t_inscripciones.update().values(new).where(t_inscripciones.c.INSCRIPCION_ID == id))
        session.commit()
        return session.execute(select(t_inscripciones).where(t_inscripciones.c.INSCRIPCION_ID == id)).first()
    else:
        raise HTTPException(status_code=404, detail='La inscripción solicitada no existe.')

@inscripciones.delete('/delete/{id}')
def Delete_Inscripcion(id: int, session: Session = Depends(Get_Session)):
    inscripcion = session.execute(select(t_inscripciones).where(t_inscripciones.c.INSCRIPCION_ID == id)).first()
    has_children = False #Verificar con pagos si se puede borrar o poner en 0
    
    if inscripcion:
        if has_children:
            session.execute(t_inscripciones.update().values(STATUS=0).where(t_inscripciones.c.INSCRIPCION_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)
        else:
            session.execute(t_inscripciones.delete().where(t_inscripciones.c.INSCRIPCION_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)
   
    raise HTTPException(status_code=404, detail='La inscrripción solicitada no existe.')
        



