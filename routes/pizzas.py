from flask import Blueprint

from resources import pizza_resource

PREFIX = "pizzas"

PIZZA_BLUEPRINT = Blueprint(PREFIX, __name__)


@PIZZA_BLUEPRINT.route('/', methods=['GET'])
def all():
    return pizza_resource.all()
