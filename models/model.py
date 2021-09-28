from app import db


class Topping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    is_veggie = db.Column(db.Boolean, default=False)
    price = db.Column(db.Numeric, default=0.00)
    pizzas = db.relationship('PizzaTopping', backref='topping')


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    is_veggie = db.Column(db.Boolean, default=False)
    price = db.Column(db.Numeric, default=0.00)
    toppings = db.relationship('PizzaTopping', backref='pizza')
    orders = db.relationship('OrderedPizza', backref='pizza')


class OrderStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)
    ordered_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)


class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.String(255), nullable=False, primary_key=True)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    addition = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.Integer, db.ForeignKey('district.zip_code'), nullable=False)
    city = db.Column(db.String(255), nullable=False)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.Numeric)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    birthday = db.Column(db.Date, nullable=True)


class Courier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), nullable=False, primary_key=True, unique=True)
    is_used = db.Column(db.Boolean, default=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('order_status.id'))
    discount_code = db.Column(db.String(255), db.ForeignKey('discount.code'))
    pizzas = db.relationship('OrderedPizza', backref='order')
    items = db.relationship('OrderedItem', backref='order')


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric, default=0.00)
    orders = db.relationship('OrderedItem', backref='item')


class PizzaTopping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    topping_id = db.Column(db.Integer, db.ForeignKey('topping.id'))
    quantity = db.Column(db.Integer, default=1)


class OrderedItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    quantity = db.Column(db.Integer, default=1)


class OrderedPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    quantity = db.Column(db.Integer, default=1)
