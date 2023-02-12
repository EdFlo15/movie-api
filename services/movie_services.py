
from models.movie import Movie as MovieModel
from schemas.movie_schema import Movie
class MovieService():

    def __init__(self,db)-> None:
        self.db = db

    def get_movies(self):
        result=self.db.query(MovieModel).all()
        return result

    def get_movie(self,id):
        result=self.db.query(MovieModel).filter(MovieModel.id==id).first()
        return result

    def get_movie_by_category(self,category):
        result=self.db.query(MovieModel).filter(MovieModel.category==category).all()
        return result

    def create_movie(self,movie:Movie):
        new_movie=MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return 

    def update_movie(self,movie:Movie,id:int):
        result=self.db.query(MovieModel).filter(MovieModel.id==id).first()
        try:
            result.title=movie.title
            result.overview=movie.overview
            result.year=movie.year
            result.rating=movie.rating
            result.category=movie.category
            self.db.commit()
            return {"message": "update movie completed successfully"}
        except :
            return {"message": "Movie not found"}

    def delete_movie(self,id):
        try:
            result=self.db.query(MovieModel).filter(MovieModel.id==id).first()
            self.db.delete(result)
            self.db.commit()
            return {"message": "delete movie"}
        except :
            return {"message": "Movie not found"}