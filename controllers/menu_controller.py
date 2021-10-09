from flask import jsonify

from models.sqlite_model import Pizza, Item


def get_pizzas():
    return Pizza.query.all()

def get_items():
    return Item.query.all()

def create_order():
    pass

