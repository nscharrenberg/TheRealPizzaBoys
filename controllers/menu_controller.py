from models.sqlite_model import Pizza, Item, Order, db, OrderStatus, OrderedPizza
from datetime import datetime


def get_pizzas():
    return Pizza.query.all()


def get_items():
    return Item.query.all()


def add_pizza_to_card(customer, pizza):
    order = Order.query.filter(Order.customer_id == customer.id, Order.status.any(OrderStatus.status == 0)).first()

    if order is None:
        order_status = OrderStatus(0, datetime.now())
        db.session.add(order_status)
        db.session.commit()
        order = Order(customer.id, order_status.id)
        db.session.add(order)
        db.session.commit()
        order_status.order_id = order.id
        db.session.commit()

    order_pizza = OrderedPizza.query.filter_by(pizza_id=pizza, order_id=order.id).first()

    if order_pizza is None:
        order_pizza = OrderedPizza(pizza, order.id)
        db.session.add(order_pizza)
    else:
        order_pizza.quantity = order_pizza.quantity + 1

    db.session.commit()


def create_order():
    pass
