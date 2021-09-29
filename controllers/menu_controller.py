from flask import jsonify

from models.sqlite_model import Pizza, Item


def get_menu():
    pizzas = Pizza.query.all()
    items = Item.query.all()

    return jsonify({"Pizzas":pizzas,"Items":items})

def create_order():
    pass

