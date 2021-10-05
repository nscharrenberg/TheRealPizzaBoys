from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import app
from flask_sqlalchemy import SQLAlchemy

from config import Config

app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


class Topping(db.Model):
    __tablename__ = "toppings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    is_veggie = db.Column(db.Boolean, default=False)
    price = db.Column(db.Numeric, default=0.00)
    pizzas = db.relationship('PizzaTopping', backref='topping')

    def __init__(self, name, is_veggie, price):
        self.name = name
        self.is_veggie = is_veggie
        self.price = price
        # pizzas can be nullable


class Pizza(db.Model):
    __tablename__ = "pizzas"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    is_veggie = db.Column(db.Boolean, default=False)
    price = db.Column(db.Numeric, default=0.00)
    toppings = db.relationship('PizzaTopping', backref='pizza')
    orders = db.relationship('OrderedPizza', backref='pizza')

    def __init__(self, name, toppings):
        self.name = name
        self.is_veggie = True
        self.price = 0
        for t in toppings:
            price = t.price
            if not t.is_veggie:
                self.is_veggie = False

        self.price = self.price * 1.4  # 40 % margin of profit
        self.price = self.price * 1.09  # 9 % VAT
        self.price = round(self.price, 1)


class OrderStatus(db.Model):
    __tablename__ = "order_statuses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Integer)
    ordered_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)

    def __init__(self, status, ordered_at, delivered_at, order_id):
        self.status = status
        self.ordered_at = ordered_at
        self.delivered_at = delivered_at
        self.order_id = order_id


class District(db.Model):
    __tablename__ = "districts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zip_code = db.Column(db.String(255), nullable=False, primary_key=True)
    couriers = db.relationship('Courier', backref='district')

    def __init__(self, zip_code):
        self.zip_code = zip_code


class Address(db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street = db.Column(db.String(255), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    addition = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.Integer, db.ForeignKey('districts.id'), nullable=False)
    city = db.Column(db.String(255), nullable=False)

    def __init__(self, street, house_number, addition, zip_code, city):
        self.street = street
        self.house_number = house_number
        self.addition = addition
        self.zip_code = zip_code
        self.city = city


class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.Numeric)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    birthday = db.Column(db.Date, nullable=True)
    amount_ordered = db.Column(db.Integer,
                               nullable=False)  # had to add because of reqs, is gonna be increased with every order, if amount%10 = 0, the user get´s a discount code
    discounts = relationship("Discount")
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, first_name, last_name, phone_number, address_id, birthday):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address_id = address_id
        self.birthday = birthday
        self.amount_ordered = 0


class Courier(db.Model):
    __tablename__ = "couriers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'))

    def __init__(self, name, district_id):
        self.name = name
        self.district_id = district_id


class Discount(db.Model):
    __tablename__ = "discounts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(255), nullable=False, primary_key=True, unique=True)
    is_used = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, ForeignKey('customers.id'))

    def __init__(self, code, is_used, user_id):
        self.code = code
        self.is_used = is_used
        self.user_id = user_id


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    courier_id = db.Column(db.Integer, db.ForeignKey('couriers.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('order_statuses.id'))
    discount_code = db.Column(db.String(255), db.ForeignKey('discounts.code'))
    pizzas = db.relationship('OrderedPizza', backref='order')
    items = db.relationship('OrderedItem', backref='order')

    def __init__(self, customer_id, courier_id, status_id, discount_code):
        self.customer_id = customer_id
        self.courier_id = courier_id
        self.status_id = status_id
        self.discount_code = discount_code


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric, default=0.00)
    orders = db.relationship('OrderedItem', backref='item')

    def __init__(self, name, price):
        self.name = name
        self.price = price


class PizzaTopping(db.Model):
    __tablename__ = "pizza_topping"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    topping_id = db.Column(db.Integer, db.ForeignKey('toppings.id'))
    quantity = db.Column(db.Integer, default=1)

    def __init__(self):
        pass


class OrderedItem(db.Model):
    __tablename__ = "order_item"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    quantity = db.Column(db.Integer, default=1)

    def __init__(self):
        pass


class OrderedPizza(db.Model):
    __tablename__ = "order_pizza"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    quantity = db.Column(db.Integer, default=1)

    def __init__(self):
        pass


db.create_all()
