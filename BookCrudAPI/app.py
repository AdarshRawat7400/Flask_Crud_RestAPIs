from flask import Flask,jsonify,request
from flask_restful import Api,Resource,reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from decouple import config


app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config('SQLALCHEMY_TRACK_MODIFICATIONS')


book_args_parser = reqparse.RequestParser()
book_args_parser.add_argument('title',type=str,required=True,help='Title is required')
book_args_parser.add_argument('author',type=str,required=True,help='Author is required')
book_args_parser.add_argument('year',type=int,required=True,help='Year is required')

resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String,
    'year': fields.Integer
}



class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year




class BooksListResource(Resource):

    @marshal_with(resource_fields)
    def get(self):
        return Books.query.all(), 200

    @marshal_with(resource_fields)
    def post(self):
        args = book_args_parser.parse_args()
        title = args['title']
        author = args['author']
        year = args['year']

        new_book = Books(title, author, year)

        db.session.add(new_book)
        db.session.commit()
        return new_book, 201


class BookDetailResource(Resource):
    @marshal_with(resource_fields)
    def get(self,book_id):
        book = Books.query.get(book_id)
        if book:
            return book, 200
        abort(404, message="Book not found")

    @marshal_with(resource_fields)
    def put(self,book_id):
        book = Books.query.get(book_id)
        if book:
            args = book_args_parser.parse_args()
            title = args['title']
            author = args['author']
            year = args['year']
            book.title = title
            book.author = author
            book.year = year
            db.session.commit()
            return book, 200

        return abort(404, message="Book not found")

    def delete(self,book_id):
        book = Books.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return '', 204
        abort(404, message="Book not found")


api.add_resource(BooksListResource, '/books_list')
api.add_resource(BookDetailResource, '/book_detail/<int:book_id>')





if __name__ == '__main__':
    app.run(debug=True)