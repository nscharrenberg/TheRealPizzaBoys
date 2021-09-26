from flask import Blueprint

PREFIX = "pizzas"

PIZZA_BLUEPRINT = Blueprint(PREFIX, __name__)


@PIZZA_BLUEPRINT.route('/', methods=['GET'])
def all():
    return 'hello'