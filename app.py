# Librerias FastAPI
from fastapi import Depends, FastAPI,Path,Query,Request,HTTPException
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.security import HTTPBearer

from utils.jwt_manager import create_token,validate_token
# Librerias Pydantic

from pydantic import BaseModel
from pydantic import Field

# liberias python

from typing import List, Optional

app=FastAPI()
app.title="Aplicación con FastAPI"

# reación de modelo

class JWTBearer(HTTPBearer):
    async def __call__(self,request:Request):
        auth= await super().__call__(request)
        data=validate_token(auth.credentials)
        if data['email']!='admin@gmail.com':
            raise HTTPException(status_code=403,detail="NOT VALID CREDENCIAL")


class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel):
    id:Optional[int]=None
    title:str=Field(min_length=5, max_length=50)
    overview:str=Field(min_length=5, max_length=100)
    year:str=Field(min_length=4, max_length=15)
    rating:float=Field(le=10)
    category:str=Field(min_length=1, max_length=15)

    class Config:
        schema_extra={
            'example':{
                'id':1,
                'title':"The house of the Dragon",
                'overview':"Fatastic Serie",
                'year': "2020",
                'rating':7.8,
                'category':'Drama'
                    }
        }

# creación de listas de peliculas

movies=[
      {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Accion"
	},
     {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2020",
		"rating": 7.8,
		"category": "Accion"
	},
    {
		"id": 3,
		"title": "Accion",
		"overview": "Bruce lee",
		"year": "2022",
		"rating": 7.8,
		"category": "Accion"
	},
     {
		"id": 4,
		"title": "Drama",
		"overview": "The love",
		"year": "2009",
		"rating": 7.8,
		"category": "Drama"
	}

]

# pruebas básica de home
@app.get('/', tags=['Home'])
def message():
    return HTMLResponse(
        """
        <h1> Hello World!</h1>
        """
        )

@app.post('/login',tags=['auth'])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password =="admin":
        token:str=create_token(user.dict())
        return JSONResponse(content=token, status_code=200)


# retorrnar el listado de las peliculas
@app.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies, status_code=200)

# Retornar una pelicula en particular por el ID
# Path validation se realiza medinate Path de fastapi
@app.get('/get_movie/{id}', tags=['Movies'], response_model=Movie)
def get_movie(id:int=Path(ge=1,le=100))->Movie:
    for items in movies:
        if items["id"]==id:
            return JSONResponse(content=items,status_code=200) 
    return JSONResponse(content=[],status_code=404)

# retornar una movies de peliculas por categoria y año.
@app.get('/movies/',tags=['Movies'], response_model=list[Movie])
def get_movies_by_category(category:str=Query(min_length=4, max_length=15))->List[Movie]:
    data=[ item for item in movies if item['category']==category]
    return JSONResponse(content=data)

# Crear una pelicula medinate el método post de HTTP

@app.post('/create_movie/',tags=['Movies'], response_model=dict, status_code=201)
def create_movie(movie:Movie):
    movies.append(movie)
    return JSONResponse(content={"Message":"Correctly register"}, status_code=201)


#Actualización de Items
@app.put('/update_movies/{id}', tags=['Movies'], response_model=dict,status_code=200)
def update_movie(
    id:int,
    movie:Movie
):
    for items in movies:
        if items["id"]==id:
            items['title']=movie.title
            items['overview']=movie.overview
            items['year']=movie.year
            items['rating']=movie.rating
            items['category']=movie.category
        return JSONResponse(content={"Message":"Update Corrrectly"},status_code=200)

#Eliminacion de Items

@app.delete('/delete_movie/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(id:int):
    for items in movies:
        if items["id"]==id:
            movies.remove(items)
    return JSONResponse(content={"Message":"Deleted Corrrectly"},status_code=200)



# recarga automática y creación de puerto.
# uvicorn main:app --reload --port 5000

# Si queremos que el contenido sea responsive agregamos --host 0.0.0.0
# uvicorn main:app --reload --port 5000 --host 0.0.0.0