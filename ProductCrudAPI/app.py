from flask import Flask , request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.String(500))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','desciption','price','qty')


product_schema = ProductSchema() 
products_schema = ProductSchema(many=True) # many=True will return a list of products


# endpoint to create new product
@app.route("/product", methods=["POST"])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    if Product.query.filter_by(name=name):
        return jsonify({"message": "Product already exists"}), 400
    new_product = Product(name,description,price,qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

@app.route("/product/<string:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)
    if product:
        product.name = request.json['name']
        product.description = request.json['description']
        product.price = request.json['price']
        product.qty = request.json['qty']

        db.session.commit()
        return product_schema.jsonify(product), 200

    return jsonify({"message": f"Product with id {id} does not exists"}), 400


@app.route("/product/<string:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": f"Product with id {id} deleted"}), 200

    return jsonify({"message": f"Product with id {id} does not exists"}), 400


@app.route("/products", methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result), 200



@app.route("/product/<string:id>", methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product), 200





if __name__ == '__main__':
    app.run(debug=True)