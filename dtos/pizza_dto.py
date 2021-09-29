from app import ma
from models.sqlite_model import Pizza


class PizzaDto(ma.SQLAlchemySchema):
    class Meta:
        model = Pizza

    id = ma.auto_field()
    name = ma.auto_field()
    is_veggie = ma.auto_field()
    price = ma.auto_field()
    toppings = ma.auto_field
