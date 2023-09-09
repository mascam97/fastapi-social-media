from fastapi import APIRouter
from fastapi import Depends, Path, Query
from starlette.responses import JSONResponse
from config.database import Session
from models.publication import Publication as PublicationModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.publication import PublicationService
from schemas.publication import Publication

publication_router = APIRouter()


@publication_router.get('/publications', tags=['publications'], dependencies=[Depends(JWTBearer())])
def get_publications() -> JSONResponse:
  db = Session()
  result = PublicationService(db).get_publications()
  return JSONResponse(status_code=200, content={"data": jsonable_encoder(result)})


@publication_router.get('/publications/{id}', tags=['publications'], dependencies=[Depends(JWTBearer())])
def get_publication(id: int = Path(ge=1, le=2000)) -> JSONResponse:
  db = Session()
  result = PublicationService(db).get_publication(id)
  if not result:
    return JSONResponse(status_code=404, content={'message': "Not Found"})
  return JSONResponse(status_code=200, content={"data": jsonable_encoder(result)})


@publication_router.get('/publications/', tags=['publications'], dependencies=[Depends(JWTBearer())])
def get_publications_by_state(state: str = Query(min_length=5, max_length=15)) -> JSONResponse:
  db = Session()
  result = PublicationService(db).get_publications_by_state(state)
  return JSONResponse(status_code=200, content={"data": jsonable_encoder(result)})


@publication_router.post('/publications', tags=['publications'], dependencies=[Depends(JWTBearer())])
def create_publication(publication: Publication) -> JSONResponse:
  db = Session()
  PublicationService(db).create_publication(publication)
  return JSONResponse(
    status_code=201,
    content={"message": "The publication was created", "data": jsonable_encoder(publication)}
  )


@publication_router.put('/publications/{id}', tags=['publications'], dependencies=[Depends(JWTBearer())])
def update_publication(id: int, publication: Publication) -> JSONResponse:
  db = Session()
  result = PublicationService(db).get_publication(id)
  if not result:
    return JSONResponse(status_code=404, content={'message': "Not Found"})

  new_publication = PublicationService(db).update_publication(id, publication)
  return JSONResponse(
    status_code=200,
    content={"message": "The publication was updated", "data": jsonable_encoder(new_publication)}
  )


@publication_router.delete('/publications/{id}', tags=['publications'], dependencies=[Depends(JWTBearer())])
def delete_publication(id: int) -> JSONResponse:
  db = Session()
  result: PublicationModel = db.query(PublicationModel).filter(PublicationModel.id == id).first()
  if not result:
    return JSONResponse(status_code=404, content={"message": "Not found"})
  PublicationService(db).delete_publication(id)
  return JSONResponse(status_code=200, content={"message": "The publication was deleted"})
