from fastapi import APIRouter,Response,HTTPException, Depends
from db.config import Session, Get_Session
from sqlmodel import select, and_, or_
from models.materias import materias as t_materias
from models.alumnos import alumnos as t_alumnos
from models.cursantes import cursantes as t_cursantes
from models.materiacarrera import materiacarrera as t_materiacarrera
from schemas.cursantes import Cursante, CursanteOUTPUT
from starlette.status import HTTP_204_NO_CONTENT
from datetime import datetime

cursantes = APIRouter(prefix='/API/CURSANTES')

@cursantes.get('/')
def Get_Cursante(filtro: str = None, session: Session = Depends(Get_Session)):
    result = []
    if filtro:
        cursantes = session.execute(select(t_cursantes, t_alumnos, t_materiacarrera, t_materias)
                .where(
                    and_(
                        t_cursantes.c.ALUMNO_ID == t_alumnos.c.ALUMNO_ID,
                        t_cursantes.c.MATERIACARRERA_ID == t_materiacarrera.c.MATERIACARRERA_ID,
                        t_materiacarrera.c.MATERIA_ID == t_materias.c.MATERIA_ID,
                        or_(
                        t_alumnos.c.NOMBRE.contains(filtro),
                        t_alumnos.c.APELLIDO.contains(filtro),
                        t_alumnos.c.DNI.contains(filtro),
                        t_materias.c.DESCRIPCION.contains(filtro),
                        str(t_materiacarrera.c.CICLO_LECTIVO) == filtro,
                        t_cursantes.c.ESTADO_CURSADA.contains(filtro)

                        )
                    )
                )).fetchall()
        
        
    else: 
        cursantes = session.execute(
                                select(t_cursantes, t_alumnos, t_materiacarrera, t_materias)
                .where(
                    and_(
                        t_cursantes.c.ALUMNO_ID == t_alumnos.c.ALUMNO_ID,
                        t_cursantes.c.MATERIACARRERA_ID == t_materiacarrera.c.MATERIACARRERA_ID,
                        t_materiacarrera.c.MATERIA_ID == t_materias.c.MATERIA_ID))).fetchall()
        
    for c in cursantes:
        single = CursanteOUTPUT()
        single.CURSANTE_ID = c.CURSANTE_ID
        single.ALUMNO_ID= c.ALUMNO_ID
        single.MATERIACARRERA_ID= c.MATERIACARRERA_ID
        single.ESTADO_CURSADA= c.ESTADO_CURSADA
        single.REGULARIDAD_END_DATE= c.REGULARIDAD_END_DATE
        single.OBSERVACIONES= c.OBSERVACIONES
        single.STATUS= c.STATUS
        single.ADD_DATE= c.ADD_DATE
        single.LAST_UPDATED_DATE=c.LAST_UPDATED_DATE
        single.NOMBRE= c.NOMBRE
        single.APELLIDO= c.APELLIDO
        single.CICLO_LECTIVO=c.CICLO_LECTIVO
        single.MATERIA= c.DESCRIPCION
        result.append(single)
    
    return result

@cursantes.get('/{id}')
def Get_Cursante(id: int, session: Session = Depends(Get_Session)):
    c = session.execute(
                                select(t_cursantes, t_alumnos, t_materiacarrera, t_materias)
                .where(
                    and_(
                        t_cursantes.c.CURSANTE_ID == id,
                        t_cursantes.c.ALUMNO_ID == t_alumnos.c.ALUMNO_ID,
                        t_cursantes.c.MATERIACARRERA_ID == t_materiacarrera.c.MATERIACARRERA_ID,
                        t_materiacarrera.c.MATERIA_ID == t_materias.c.MATERIA_ID))).first()

    if c:
        single = CursanteOUTPUT()
        single.CURSANTE_ID = c.CURSANTE_ID
        single.ALUMNO_ID= c.ALUMNO_ID
        single.MATERIACARRERA_ID= c.MATERIACARRERA_ID
        single.ESTADO_CURSADA= c.ESTADO_CURSADA
        single.REGULARIDAD_END_DATE= c.REGULARIDAD_END_DATE
        single.OBSERVACIONES= c.OBSERVACIONES
        single.STATUS= c.STATUS
        single.ADD_DATE= c.ADD_DATE
        single.LAST_UPDATED_DATE=c.LAST_UPDATED_DATE
        single.NOMBRE= c.NOMBRE
        single.APELLIDO= c.APELLIDO
        single.CICLO_LECTIVO=c.CICLO_LECTIVO
        single.MATERIA= c.DESCRIPCION
    
        return single
    else: 
        raise HTTPException(status_code=404, detail='El cursante solicitado no existe.')

@cursantes.post('/add')
def Add_Cursante(cursante: Cursante, session: Session = Depends(Get_Session)):
    new = {
    "ALUMNO_ID":            cursante.ALUMNO_ID,
    "MATERIACARRERA_ID":    cursante.MATERIACARRERA_ID,
    "ESTADO_CURSADA":       cursante.ESTADO_CURSADA,
    "REGULARIDAD_END_DATE": cursante.REGULARIDAD_END_DATE,
    "OBSERVACIONES":        cursante.OBSERVACIONES
    }

    resultado = session.execute(t_cursantes.insert().values(new))
    session.commit()
    id = resultado.inserted_primary_key[0]
    return session.execute(select(t_cursantes).where(t_cursantes.c.CURSANTE_ID == id)).first()

@cursantes.put('/update/{id}')
def Update_Cursante(id: int, cursante: Cursante, session: Session = Depends(Get_Session)):
    old = session.execute(select(t_cursantes).where(t_cursantes.c.CURSANTE_ID == id)).first()
    if old:
        new = {
                "ALUMNO_ID":            cursante.ALUMNO_ID,
                "MATERIACARRERA_ID":    cursante.MATERIACARRERA_ID,
                "ESTADO_CURSADA":       cursante.ESTADO_CURSADA,
                "REGULARIDAD_END_DATE": cursante.REGULARIDAD_END_DATE,
                "OBSERVACIONES":        cursante.OBSERVACIONES,
                "LAST_UPDATED_DATE":    datetime.now()       
        }
        session.execute(t_cursantes.update().values(new).where(t_cursantes.c.CURSANTE_ID == id))
        session.commit()
        return session.execute(select(t_cursantes).where(t_cursantes.c.CURSANTE_ID == id)).first()
    else:
        raise HTTPException(status_code=404, detail='El cursante solicitado no existe.')

@cursantes.delete('/delete/{id}')
def Delete_Cursante(id:int, session: Session = Depends(Get_Session)):
    cursante = session.execute(select(t_cursantes).where(t_cursantes.c.CURSANTE_ID == id)).first()
    is_related = False #Corroborar si hay materias que lo tengan

    if cursante:
        if is_related:
            session.execute(t_cursantes.update().values(STATUS=0).where(t_cursantes.c.CURSANTE == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)
        else:
            session.execute(t_cursantes.delete().where(t_cursantes.c.CURSANTE_ID == id))
            session.commit()
            return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='El cursante solicitado no existe.')