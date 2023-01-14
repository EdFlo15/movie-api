# Librerias FastAPI
from fastapi import FastAPI,Path,Query
from fastapi.responses import HTMLResponse,JSONResponse

# Librerias Pydantic

from pydantic import BaseModel
from pydantic import Field

# liberias python

from typing import Optional

app=FastAPI()
app.title="Aplicación con FastAPI"

# reación de modelo

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

# retorrnar el listado de las peliculas
@app.get('/get_movies', tags=['Movies'])
def get_movies():
    return JSONResponse(content=movies)

# Retornar una pelicula en particular por el ID
# Path validation se realiza medinate Path de fastapi
@app.get('/get_movie/{id}', tags=['Movies'])
def get_movie(id:int=Path(ge=1,le=100)):
    for items in movies:
        if items["id"]==id:
            return items 
    return []

# retornar una movies de peliculas por categoria y año.
@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category:str=Query(min_length=4, max_length=15), year:str=Query(min_length=3,max_length=4)):
    for items in movies:
        if (items["title"]==category and items['year']==year):
            return JSONResponse(content=items)
    return JSONResponse(content=[])

# Crear una pelicula medinate el método post de HTTP

@app.post('/create_movie/',tags=['Movies'])
def create_movie(movie:Movie):
    movies.append(movie)
    return JSONResponse(content={"message":"Se registró la pelicula"})


#Actualización de Items
@app.put('/update_movies/{id}', tags=['Movies'])
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
            return movies

#Eliminacion de Items

@app.delete('/delete_movie/{id}', tags=['Movies'])
def delete_movie(id:int):
    for items in movies:
        if items["id"]==id:
            movies.remove(items)
    return movies



# recarga automática y creación de puerto.
# uvicorn main:app --reload --port 5000

# Si queremos que el contenido sea responsive agregamos --host 0.0.0.0
# uvicorn main:app --reload --port 5000 --host 0.0.0.0