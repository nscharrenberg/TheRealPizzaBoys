from flask import jsonify

from models.model import Pizza, Item


class MenuController():
    @staticmethod
    def get_menu():
        pizzas = Pizza.query.all()
        items = Item.query.all()

        return jsonify({
            "Pizzas":pizzas,
            "Items":items
        })

