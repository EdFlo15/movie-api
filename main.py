from fastapi import FastAPI, Body, Request, HTTPException
from fastapi.responses import HTMLResponse

app=FastAPI()
app.title="Aplicación con FastAPI"

# creación de listas de peliculas

movies=[
      {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
     {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2020",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 3,
		"title": "Accion",
		"overview": "Bruce lee",
		"year": "2022",
		"rating": 7.8,
		"category": "Acción"
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
    return movies

# Retornar una pelicula en particular por el ID
@app.get('/get_movie/{id}', tags=['Movies'])
def get_movie(id:int):
    for items in movies:
        if items["id"]==id:
            return items 
    return []

# retornar una movies de peliculas por categoria y año.
@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category:str, year:str):
    for items in movies:
        if (items["title"]==category and items['year']==year):
            return items
    return []

# Crear una pelicula medinate el método post de HTTP

@app.post('/create_movie/',tags=['Movie'])
def create_movie(
    id:int=Body(),
    title:str=Body(),
    overview:str=Body(),
    year:str=Body(),
    rating:float=Body(),
    category:str=Body()
):
    movies.append({
        "id":id,
        "title":title,
        "overview":overview,
        "year":year,
        "rating":rating,
        "category":category
    })
    return movies


#Actualización de Items
@app.put('/update_movies/{id}', tags=['movies'])
def update_movie(
    id:int,
    title:str=Body(),
    overview:str=Body(),
    year:str=Body(),
    rating:float=Body(),
    category:str=Body()
):
    for items in movies:
        if items["id"]==id:
            items['title']=title,
            items['overview']=overview,
            items['year']=year,
            items['rating']=rating,
            items['category']=category
        return movies

#Eliminacion de Items

@app.delete('/delete_movie/{id}', tags=['movies'])
def delete_movie(id:int):
    for items in movies:
        if items["id"]==id:
            movies.remove(items)
    return movies





# recarga automática y creación de puerto.
# uvicorn main:app --reload --port 5000

# Si queremos que el contenido sea responsive agregamos --host 0.0.0.0
# uvicorn main:app --reload --port 5000 --host 0.0.0.0