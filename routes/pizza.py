from flask import Blueprint, jsonify

from models import Pizza

PREFIX = "pizzas"

PIZZA_BLUEPRINT = Blueprint(PREFIX, __name__)


@PIZZA_BLUEPRINT.route('/', methods=['GET'])
def get_all():
    return jsonify({
        "pizzas": Pizza.query.all()
    })
