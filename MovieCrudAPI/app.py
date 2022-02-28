from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# creating an instance of the flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)



class Movie(db.Model):
    __tablename__ = 'movies'  # creating a table name
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    title = db.Column(db.String(80), nullable=False)
    # nullable is false so the column can't be empty
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(80), nullable=False)


class MovieSchema(ma.Schema):
    class Meta:
        # fields to expose
        fields = ('id', 'title', 'year', 'genre')


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@app.route('/movies', methods=['GET'])
def get_all_movies():
    '''function to return all movies in database'''
    return movies_schema.jsonify(Movie.query.all())

@app.route('/movies/<int:id>', methods=['GET'])
def get_movie_by_id(id):
    '''function to get movie by id'''
    movie = Movie.query.get(id)
    if not movie:
        return Response('Movie not found', status=404)
    return movie_schema.jsonify(Movie.query.get(id))

@app.route('/movies', methods=['POST'])
def add_movie():
    '''function to add movie to database using _title, _year, _genre
    as parameters'''
    # creating an instance of our Movie constructor
    title = request.json['title']
    year = request.json['year']
    genre = request.json['genre']
                        
    new_movie = Movie(title=title, year=year, genre=genre)
    db.session.add(new_movie)  # add new movie to database session
    db.session.commit()  # commit changes to session

    return movie_schema.jsonify(new_movie), 201


@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    '''function to update movie by id'''
    movie = Movie.query.get(id)
    if not movie:
        return Response('Movie not found', status=404)

    movie.title = request.json['title']
    movie.year = request.json['year']
    movie.genre = request.json['genre']
    db.session.commit()

    return movie_schema.jsonify(movie)

@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    '''function to delete movie by id'''
    movie = Movie.query.get(id)
    if not movie:
        return Response('Movie not found', status=404)

    db.session.delete(movie)
    db.session.commit()

    return movie_schema.jsonify(movie)


if __name__ == '__main__':
    app.run(debug=True)


