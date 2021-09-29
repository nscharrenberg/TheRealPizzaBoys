from flask import Blueprint, jsonify

from dtos.pizza_dto import PizzaDto
from models.sqlite_model import Pizza

PREFIX = "pizzas"

PIZZA_BLUEPRINT = Blueprint(PREFIX, __name__)


@PIZZA_BLUEPRINT.route('/', methods=['GET'])
def get_all():
    formatter = PizzaDto(many=True);
    pizzas = Pizza.query.all()
    response = formatter.dumps(pizzas)

    return response.data
