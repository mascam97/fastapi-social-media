from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "Django Social Media"
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Wrong credentials")

class User(BaseModel):
    email:str
    password:str

class Publication(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    content: str = Field(min_length=15, max_length=50)
    state:str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "My publication",
                "content": "Publication content",
                "state" : "active"
            }
        }

publications = [
    {
		"id": 1,
		"title": "Publication",
		"content": "Publication description",
		"state": "active"
	},
    {
		"id": 2,
		"title": "New publication",
		"content": "Publication description",
		"state": "active"
	}
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@app.get('/publications', tags=['publications'], response_model=List[Publication], status_code=200, dependencies=[Depends(JWTBearer())])
def get_publications() -> List[Publication]:
    return JSONResponse(status_code=200, content=publications)

@app.get('/publications/{id}', tags=['publications'], response_model=Publication)
def get_publication(id: int = Path(ge=1, le=2000)) -> Publication:
    for item in publications:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content=[])

@app.get('/publications/', tags=['publications'], response_model=List[Publication])
def get_publications_by_state(state: str = Query(min_length=5, max_length=15)) -> List[Publication]:
    data = [ item for item in publications if item['state'] == state ]
    return JSONResponse(content=data)

@app.post('/publications', tags=['publications'], response_model=dict, status_code=201)
def create_publication(publication: Publication) -> dict:
    publications.append(publication)
    return JSONResponse(status_code=201, content={"message": "A publication was saved"})

@app.put('/publications/{id}', tags=['publications'], response_model=dict, status_code=200)
def update_publication(id: int, publication: Publication)-> dict:
	for item in publications:
		if item["id"] == id:
			item['title'] = publication.title
			item['content'] = publication.content
			item['state'] = publication.state
			return JSONResponse(status_code=200, content={"message": "The publication was updated"})

@app.delete('/publications/{id}', tags=['publications'], response_model=dict, status_code=200)
def delete_publication(id: int)-> dict:
    for item in publications:
        if item["id"] == id:
            publications.remove(item)
            return JSONResponse(status_code=200, content={"message": "The publication was deleted"})