from fastapi import APIRouter

from fastapi import Depends, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie_services import MovieService
from schemas.movie_schema import Movie

movie_router=APIRouter()

@movie_router.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

# Get all movies as a list
@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db=Session()
    result=MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Get movie by id
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db=Session()
    result=MovieService(db).get_movie(id)
    if not result:
            return JSONResponse(status_code=404,content={'message': 'Movie not found in database'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Get movies by category
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie],dependencies=[Depends(JWTBearer())])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db=Session()
    result=MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"mesaage":"Movie with such category not found in database"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

# Create movie
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db=Session()
    new_movie=MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

# Update Movie
@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie)-> dict:
    db=Session()
    result=MovieService(db).update_movie(movie,id)
    return JSONResponse(status_code=200, content=result)

# Delete Movie
@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:
    db=Session()
    result=MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content=result)

