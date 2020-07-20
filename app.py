from flask import Flask, request
from models import MovieSchema, ActorSchema, Movie, Actor, setup_db
from flask_restful import reqparse, Api, Resource
from flask_cors import CORS
from auth import requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)

# Movie
# shows a single movie item and lets you delete a movie item


class MovieResource(Resource):
    @requires_auth('read:movies')
    def get(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        return movie_schema.dump(movie)

    @requires_auth('update:movies')
    def patch(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)

        if 'title' in request.json:
            movie.title = request.json['title']
        if 'release_year' in request.json:
            movie.content = request.json['release_year']

        movie.update()
        return movie_schema.dump(movie)

    @requires_auth('delete:movies')
    def delete(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        movie.delete()
        return '', 204

# MovieList
# shows a list of all movies, and lets you POST to add new movies


class MovieListResource(Resource):
    @requires_auth('read:movies')
    def get(self):
        movies = Movie.query.all()
        return movies_schema.dump(movies)

    @requires_auth('create:movies')
    def post(self):
        new_movie = Movie(
            title=request.json['title'],
            release_year=request.json['release_year']
        )
        new_movie.insert()
        return movie_schema.dump(new_movie)

# Actor
# shows a single actor item and lets you delete an actor item


class ActorResource(Resource):
    @requires_auth('read:actors')
    def get(self, actor_id):
        actor = Actor.query.get_or_404(actor_id)
        return actor_schema.dump(actor)

    @requires_auth('update:actors')
    def patch(self, actor_id):
        actor = Actor.query.get_or_404(actor_id)

        if 'name' in request.json:
            actor.name = request.json['name']
        if 'age' in request.json:
            actor.age = request.json['age']
        if 'gender' in request.json:
            actor.gender = request.json['gender']

        actor.update()
        return actor_schema.dump(actor)

    @requires_auth('delete:actors')
    def delete(self, actor_id):
        actor = Actor.query.get_or_404(actor_id)
        actor.delete()
        return '', 204

# ActorList
# shows a list of all actors, and lets you POST to add new actors


class ActorListResource(Resource):
    @requires_auth('read:actors')
    def get(self):
        actors = Actor.query.all()
        return actors_schema.dump(actors)

    @requires_auth('create:actors')
    def post(self):
        new_actor = Actor(
            name=request.json['name'],
            age=request.json['age'],
            gender=request.json['gender']
        )
        new_actor.insert()
        return actor_schema.dump(new_actor)


api.add_resource(MovieListResource, '/movies')
api.add_resource(MovieResource, '/movies/<movie_id>')

api.add_resource(ActorListResource, '/actors')
api.add_resource(ActorResource, '/actors/<actor_id>')
