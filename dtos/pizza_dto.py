from app import ma
from models.model import Pizza


class PizzaDto(ma.SQLAlchemySchema):
    class Meta:
        model = Pizza

    id = ma.auto_field()
    name = ma.auto_field()
    is_veggy = ma.auto_field()
    price = ma.auto_field()
    toppings = ma.auto_field
