from fastapi import APIRouter, Depends, Response, HTTPException
from starlette.status import HTTP_204_NO_CONTENT
from sqlmodel import select, or_, and_
from db.config import Session, Get_Session
from models.carreras import carreras as t_carreras
from models.sedes import sedes as t_sedes
from models.sedecarrera import sedecarrera as t_sedecarrera
from models.docentes import docentes as t_docentes
from models.preceptores import preceptores as t_preceptores
from models.materias import materias as t_materias
from models.materiacarrera import materiacarrera as t_materiacarrera
from schemas.materiacarrera import Materiacarrera, MateriacarreraOUTPUT
from datetime import datetime


materiacarrera = APIRouter(prefix="/API/MATERIACARRERA")

@materiacarrera.get("/")
def Get_Materiacarreras(filtro: str = None, session: Session = Depends(Get_Session)):
    result = []
    if filtro: # cruza y filtra los datos
        
        data = session.execute(select(
            t_materiacarrera,
            t_materias,
            t_sedecarrera,
            t_sedes,
            t_carreras,
            t_docentes,
            t_preceptores
        ).where(
            and_(
            t_materiacarrera.c.MATERIA_ID == t_materias.c.MATERIA_ID,
            t_materiacarrera.c.SEDECARRERA_ID == t_sedecarrera.c.SEDECARRERA_ID,
            t_sedecarrera.c.SEDE_ID == t_sedes.c.SEDE_ID,
            t_sedecarrera.c.CARRERA_ID == t_carreras.c.CARRERA_ID,
            t_materiacarrera.c.DOCENTE_ID == t_docentes.c.DOCENTE_ID,
            t_materiacarrera.c.PRECEPTOR_ID == t_preceptores.c.PRECEPTOR_ID,
            #filtros
            or_(
            str(t_materiacarrera.c.CICLO_LECTIVO) == filtro,
            t_sedes.c.DESCRIPCION.contains(filtro),
            t_carreras.c.DESCRIPCION.contains(filtro),
            t_docentes.c.NOMBRE.contains(filtro),
            t_preceptores.c.NOMBRE.contains(filtro)

        )))).fetchall()
        
    else:      # solo cruza los datos

        data = session.execute(select(
            t_materiacarrera,
            t_materias,
            t_sedecarrera,
            t_sedes,
            t_carreras,
            t_docentes,
            t_preceptores
            ).where(
            and_(
            t_materiacarrera.c.MATERIA_ID == t_materias.c.MATERIA_ID,
            t_materiacarrera.c.SEDECARRERA_ID == t_sedecarrera.c.SEDECARRERA_ID,
            t_sedecarrera.c.SEDE_ID == t_sedes.c.SEDE_ID,
            t_sedecarrera.c.CARRERA_ID == t_carreras.c.CARRERA_ID,
            t_materiacarrera.c.DOCENTE_ID == t_docentes.c.DOCENTE_ID,
            t_materiacarrera.c.PRECEPTOR_ID == t_preceptores.c.PRECEPTOR_ID
            ))).fetchall()


    for i in data: 
        single = MateriacarreraOUTPUT()
        single.MATERIACARRERA_ID        = i.MATERIACARRERA_ID
        single.MATERIA_ID               = i.MATERIA_ID
        single.SEDECARRERA_ID           = i.SEDECARRERA_ID
        single.DOCENTE_ID               = i.DOCENTE_ID
        single.PRECEPTOR_ID             = i.PRECEPTOR_ID
        single.CICLO_LECTIVO            = i.CICLO_LECTIVO
        single.CURSO                    = i.CURSO
        single.REGULARIZABLE            = i.REGULARIZABLE
        single.MATERIA_DESCRIPCION      = i.DESCRIPCION
        single.CARRERA_ANIO             = i.CARRERA_ANIO
        single.CARRERA                  = i.DESCRIPCION_2
        single.SEDE                     = i.DESCRIPCION_1
        single.PROFESOR                 = f'{i.APELLIDO}, {i.NOMBRE} '
        single.PRECEPTOR                = f'{i.APELLIDO_1}, {i.NOMBRE_1} '
        single.TURNO                    = i.TURNO
        single.STATUS                   = i.STATUS
        single.ADD_DATE                 = i.ADD_DATE
        single.LAST_UPDATED_DATE        = i.LAST_UPDATED_DATE
        result.append(single)
    return result
      
@materiacarrera.get("/{id}")
def Get_Materiacarrera(id: int, session:Session = Depends(Get_Session)):
    i = session.execute(select(
            t_materiacarrera,
            t_materias,
            t_sedecarrera,
            t_sedes,
            t_carreras,
            t_docentes,
            t_preceptores
            ).where(
            and_(
            t_materiacarrera.c.MATERIACARRERA_ID == id,
            t_materiacarrera.c.MATERIA_ID == t_materias.c.MATERIA_ID,
            t_materiacarrera.c.SEDECARRERA_ID == t_sedecarrera.c.SEDECARRERA_ID,
            t_sedecarrera.c.SEDE_ID == t_sedes.c.SEDE_ID,
            t_sedecarrera.c.CARRERA_ID == t_carreras.c.CARRERA_ID,
            t_materiacarrera.c.DOCENTE_ID == t_docentes.c.DOCENTE_ID,
            t_materiacarrera.c.PRECEPTOR_ID == t_preceptores.c.PRECEPTOR_ID
            ))).first()
    
    print(i)
    if i:
        single = MateriacarreraOUTPUT()
        single.MATERIACARRERA_ID        = i.MATERIACARRERA_ID
        single.MATERIA_ID               = i.MATERIA_ID
        single.SEDECARRERA_ID           = i.SEDECARRERA_ID
        single.DOCENTE_ID               = i.DOCENTE_ID
        single.PRECEPTOR_ID             = i.PRECEPTOR_ID
        single.CICLO_LECTIVO            = i.CICLO_LECTIVO
        single.CURSO                    = i.CURSO
        single.REGULARIZABLE            = i.REGULARIZABLE
        single.MATERIA_DESCRIPCION      = i.DESCRIPCION
        single.CARRERA_ANIO             = i.CARRERA_ANIO
        single.CARRERA                  = i.DESCRIPCION_2
        single.SEDE                     = i.DESCRIPCION_1
        single.PROFESOR                 = f'{i.APELLIDO}, {i.NOMBRE} '
        single.PRECEPTOR                = f'{i.APELLIDO_1}, {i.NOMBRE_1} '
        single.TURNO                    = i.TURNO
        single.STATUS                   = i.STATUS
        single.ADD_DATE                 = i.ADD_DATE
        single.LAST_UPDATED_DATE        = i.LAST_UPDATED_DATE
        return single
    else: 
        raise HTTPException(status_code=404, detail='No se encontraron registros con el ID solicitado.')
 
@materiacarrera.post("/add")
def Add_Materiacarreras(materiacarrera: Materiacarrera, session: Session = Depends(Get_Session)):
    try:
        new = {
            "MATERIA_ID":        materiacarrera.MATERIA_ID,     
            "SEDECARRERA_ID":    materiacarrera.SEDECARRERA_ID,
            "DOCENTE_ID":        materiacarrera.DOCENTE_ID,
            "PRECEPTOR_ID":      materiacarrera.PRECEPTOR_ID,
            "CICLO_LECTIVO":     materiacarrera.CICLO_LECTIVO,
            "CURSO":             materiacarrera.CURSO,
            "REGULARIZABLE":     materiacarrera.REGULARIZABLE
        }


        resultado = session.execute(t_materiacarrera.insert().values(new))
        session.commit()
        id = resultado.inserted_primary_key[0]
        return session.execute(select(t_materiacarrera).where(t_materiacarrera.c.MATERIACARRERA_ID == id)).first()
        
    except Exception as e:
        error = f'No se pudo insertar el registro. Error: {e}'
        return error
    
@materiacarrera.put("/{id}")
def Update_Materiacarreras(id: int, materiacarrera: Materiacarrera, session: Session = Depends(Get_Session)):
    old = session.execute(select(t_materiacarrera).where(t_materiacarrera.c.MATERIACARRERA_ID == id)).first()
    if old:
        new = {
            "MATERIA_ID":        materiacarrera.MATERIA_ID,     
            "SEDECARRERA_ID":    materiacarrera.SEDECARRERA_ID,
            "DOCENTE_ID":        materiacarrera.DOCENTE_ID,
            "PRECEPTOR_ID":      materiacarrera.PRECEPTOR_ID,
            "CICLO_LECTIVO":     materiacarrera.CICLO_LECTIVO,
            "CURSO":             materiacarrera.CURSO,
            "REGULARIZABLE":     materiacarrera.REGULARIZABLE,
            "LAST_UPDATED_DATE": datetime.now()
        }
        session.execute(t_materiacarrera.update().values(new).where(t_materiacarrera.c.MATERIACARRERA_ID == id))
        session.commit()
        return session.execute(select(t_materiacarrera).where(t_materiacarrera.c.MATERIACARRERA_ID == id)).first()
    else:
        raise HTTPException(status_code=404, detail='El registro solicitado no existe.')

@materiacarrera.delete("/{id}")
def Delete_Materiacarreras(id: int, session: Session = Depends(Get_Session)):
    materiacarrera = session.execute(select(t_materiacarrera).where(t_materiacarrera.c.MATERIACARRERA_ID == id)).first()
    has_children = False #Verificar con las tablas relacionadas si se puede borrar o poner en 0
    
    if materiacarrera:
        if has_children:
            session.execute(t_materiacarrera.update().values(STATUS=0).where(t_materiacarrera.c.MATERIACARRERA_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)
        else:
            session.execute(t_materiacarrera.delete().where(t_materiacarrera.c.MATERIACARRERA_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)
   
    raise HTTPException(status_code=404, detail='El registro solicitado no existe.')
        
