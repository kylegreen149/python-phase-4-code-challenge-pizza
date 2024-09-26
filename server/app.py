#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=["GET"])
def get_all_restaurants():
    if request.method == 'GET':
        return [r.to_dict(rules=['-restaurant_pizzas']) for r in Restaurant.query.all()], 200

@app.route("/restaurants/<int:id>", methods=["GET", "DELETE"])
def get_restaurant_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    if restaurant is None:
        return {"error": "Restaurant not found"}, 404
    if request.method == 'GET':
        return restaurant.to_dict(), 200
    elif request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204
    

@app.route("/pizzas", methods=["GET"])
def get_all_pizzas():
    if request.method == 'GET':
        return [p.to_dict(rules=['-restaurant_pizzas']) for p in Pizza.query.all()], 200

@app.route("/restaurant_pizzas", methods=["POST"])
def add_price():
    # if request.method == 'GET':
    #     return [rp.to_dict(rules=['-pizza', '-restaurant']) for rp in RestaurantPizza.query.all()], 200
    if request.method == 'POST':
        data = request.get_json()
        try:
            add_price = RestaurantPizza(
                price=data.get('price'),
                restaurant_id=data.get('restaurant_id'),
                pizza_id=data.get('pizza_id')
            )
        except ValueError:
            return {"errors": ["validation errors"]}, 400
        db.session.add(add_price)
        db.session.commit()
        return add_price.to_dict(), 201

if __name__ == "__main__":
    app.run(port=5555, debug=True)
