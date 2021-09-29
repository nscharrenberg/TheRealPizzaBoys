from app import ma
from models.sqlite_model import Topping


class SimpleToppingDto(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Topping
        include_fk = True
