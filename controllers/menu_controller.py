from models.sqlite_model import Pizza, Item, Order, db, OrderStatus, OrderedPizza, OrderedItem
from datetime import datetime


def get_pizzas():
    return Pizza.query.all()


def get_items():
    return Item.query.all()


def remove_pizza_to_card(customer, pizza):
    order = Order.query.filter(Order.customer_id == customer.id, Order.status.any(OrderStatus.status == 0)).first()

    if order is None:
        return

    order_pizza = OrderedPizza.query.filter_by(pizza_id=pizza, order_id=order.id).first()

    if order_pizza is None:
        return

    if order_pizza.quantity == 1:
        db.session.delete(order_pizza)
        db.session.commit()

    order_pizza.quantity = order_pizza.quantity - 1
    db.session.commit()


def remove_item_to_card(customer, item):
    order = Order.query.filter(Order.customer_id == customer.id, Order.status.any(OrderStatus.status == 0)).first()

    if order is None:
        return

    order_item = OrderedItem.query.filter_by(item_id=item, order_id=order.id).first()

    if order_item is None:
        return

    if order_item.quantity == 1:
        db.session.delete(order_item)
        db.session.commit()

    order_item.quantity = order_item.quantity - 1
    db.session.commit()


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


def add_item_to_card(customer, item):
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

    order_item = OrderedItem.query.filter_by(item_id=item, order_id=order.id).first()

    if order_item is None:
        order_item = OrderedItem(item, order.id)
        db.session.add(order_item)
    else:
        order_item.quantity = order_item.quantity + 1

    db.session.commit()


def create_order():
    pass
