import decimal

import flask
import flask_login
from flask import Flask, render_template, make_response, request
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import session

app = Flask(__name__)
app.secret_key = 'topsecretkeythatonlyweknow'  # would usually store this as an environmental variable
app.config['SCHEDULER_API_ENABLED'] = True
login_manager = flask_login.LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

from models.mysql_model import Order, db, OrderStatus, District, Address, Courier, Discount, Pizza


@scheduler.task('interval', id='check_if_pizza_goes_out', seconds=10, misfire_grace_time=900)
def check_if_pizza_goes_out():
    current_date = datetime.now() - timedelta(seconds=30)
    # Retrieve all orders older then 5 minutes that are still pending for delivery (status 1)
    order_statuses = OrderStatus.query.filter(OrderStatus.ordered_at <= current_date, OrderStatus.status == 1).all()

    for status in order_statuses:
        if status.order.courier_id is not None:
            status.status = 2
            db.session.commit()
        else:
            assign_delivery_person(status)


@scheduler.task('interval', id='deliver_pizza', minutes=1, misfire_grace_time=900)
def check_if_pizza_goes_out():
    current_date = datetime.now() - timedelta(minutes=1)

    order_statuses = OrderStatus.query.filter(OrderStatus.ordered_at <= current_date).all()

    for status in order_statuses:
        status.status = 3
        db.session.commit()


@scheduler.task('interval', id='remove_old_unordered_orders', minutes=1, misfire_grace_time=900)
def remove_old_unordered_orders():
    current_date = datetime.now() - timedelta(minutes=15)

    # Retrieve all orders older then 15 minutes that have not been officially ordered yet. (status 0)
    order_statuses = OrderStatus.query.filter(OrderStatus.created_at <= current_date, OrderStatus.status == 0).all()

    if bool(order_statuses):
        return

    for status in order_statuses:
        db.session.delete(status.order)
        db.session.commit()


from models.mysql_model import Customer


@login_manager.user_loader
def user_loader(id):
    user = Customer.query.filter_by(id=id).first()

    if user is None:
        return

    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user = Customer.query.filter_by(email=email).first()

    if user is None:
        return

    return user


from controllers import menu_controller, add_pizzas, customer_controller


@app.route("/", methods=["GET"])
def home():
    return render_template("Home.html")


@app.route("/contact", methods=["GET"])
def contact():
    return render_template("Contact.html")


@app.route("/login", methods=["GET"])
def login_screen():
    return render_template("Login.html")


@app.route("/login", methods=["POST"])
def login():
    try:
        customer = customer_controller.login(request.form['email'],
                                             request.form['password'])

        flask_login.login_user(customer)
        return flask.redirect('/menu')
    except Exception as ex:
        return make_response(ex, 500)


@app.route("/register", methods=["GET"])
def register_screen():
    return render_template("Register.html")


@app.route("/register", methods=["POST"])
def register():
    customer_controller.register(request.form['first_name'], request.form['last_name'],
                                 request.form['phone_number'],
                                 request.form['email'],
                                 request.form['password'], request.form['street'],
                                 request.form['house_number'],
                                 request.form['addition'], request.form['zipcode'],
                                 request.form['city'])

    return flask.redirect('/menu')


@app.route("/menu", methods=["GET"])
def show_menu():
    return render_template("Menu.html", pizzas=menu_controller.get_pizzas(), items=menu_controller.get_items())


@app.route("/card-pizza-add", methods=["POST"])
@flask_login.login_required
def add_pizza_to_card():
    menu_controller.add_pizza_to_card(flask_login.current_user, request.form['pizza_id'])
    return flask.redirect('menu')


@app.route("/card-pizza-delete", methods=["POST"])
@flask_login.login_required
def remove_pizza_from_card():
    menu_controller.remove_pizza_to_card(flask_login.current_user, request.form['pizza_id'])
    return flask.redirect('menu')


@app.route("/card-item-add", methods=["POST"])
@flask_login.login_required
def add_item_to_card():
    menu_controller.add_item_to_card(flask_login.current_user, request.form['item_id'])
    return flask.redirect('menu')


@app.route("/card-item-delete", methods=["POST"])
@flask_login.login_required
def remove_item_from_card():
    menu_controller.remove_item_to_card(flask_login.current_user, request.form['item_id'])
    return flask.redirect('menu')


@app.route("/order", methods=["GET"])
@flask_login.login_required
def show_order():
    order = Order.query.filter(Order.customer_id == flask_login.current_user.id,
                               Order.status.has(OrderStatus.status == 0)).first()
    discounts = Discount.query.filter(Discount.user_id == flask_login.current_user.id, Discount.is_used == False).all()
    return render_template("Order.html", order=order, discounts=discounts)


@app.route("/order/confirmation/<order_id>", methods=["GET"])
@flask_login.login_required
def show_order_confirm(order_id):
    order = Order.query.get(order_id)

    if order is None:
        return flask.redirect('/order')

    if order.status.ordered_at is None:
        order.status.ordered_at = datetime.now()
        db.session.commit()

    exp_delivery = order.status.ordered_at + timedelta(minutes=15)

    order_status = order.status.status

    status = 'SHOPPING CART'

    if order_status == 1:
        status = 'IN PROGRESS'
    elif order_status == 2:
        status = 'OUT FOR DELIVERY'
    elif order_status == 3:
        status = 'DELIVERED'
    elif order_status == 4:
        status = 'CANCELLED'

    return render_template("OrderStatus.html", order=order, expected_delivery=exp_delivery, status=status)


@app.route("/order", methods=["POST"])
@flask_login.login_required
def place_order():
    order_status = OrderStatus.query.filter(OrderStatus.status == 0, OrderStatus.order.has(
        Order.customer_id == flask_login.current_user.id)).first()

    if order_status.order.pizzas is None:
        return flask.redirect('/order')

    if len(order_status.order.pizzas) < 1:
        return flask.redirect('/order')
    discount_code = request.form['discount_code']
    dc = Discount.query.filter(Discount.code == discount_code).first()
    cur = Customer.query.filter(Customer.id == flask_login.current_user.id).first()
    # add ordered pizza to be eligible for discount codes
    for pizza in order_status.order.pizzas:
        cur.amount_ordered += 1 * pizza.quantity

    # receive discount
    while cur.amount_ordered > 10:
        create_discount_code(flask_login.current_user.id)
        cur.amount_ordered -= 10

    # discount price
    if dc is not None and not dc.is_used:
        order_status.order.discount_code = discount_code
        dc.is_used = True
        order_status.order.price *= decimal.Decimal(0.9)

    order_status.status = 1
    order_status.ordered_at = datetime.now()

    assign_delivery_person(order_status)

    db.session.commit()

    return flask.redirect('/order/confirmation/' + str(order_status.order_id))


@app.route("/order/cancel", methods=["POST"])
@flask_login.login_required
def cancel_order():
    # TODO: Create logic and view for placing orders
    return make_response({"result": "success"}, 200)


@app.route("/migrate/seed", methods=["GET"])
def seed():
    add_pizzas.add_everything()
    return make_response({"result": "success"}, 200)


@app.route('/protected', methods=['GET'])
@flask_login.login_required
def protected():
    return 'This is secret'


@app.route('/logout', methods=['GET'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('home'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect(flask.url_for('login'))


def assign_delivery_person(status):
    # Give order to delivery person
    customer_address_id = Customer.query.filter(Customer.id == status.order.customer_id).first().address_id
    customer_zipcode_id = Address.query.filter(Address.id == customer_address_id).first().zip_code
    # list of all delivery people for the district
    delivery_people_from_district = Courier.query.filter(Courier.district_id == customer_zipcode_id).all()
    for p in delivery_people_from_district:
        # need to check if p available
        orders_for_p = Order.query.filter(Order.courier_id == p.id, Order.status.has(OrderStatus.status == 2)).first()
        if orders_for_p is None:
            # they are not busy
            status.order.courier_id = p.id
            unassigned_orders = Order.query.filter(
                Order.customer.has(Address.zip_code == status.order.customer.address.zip_code),
                OrderStatus.status == 1).all()
            for unass_order in unassigned_orders:
                unass_order.courier_id = p.id
            break

    db.session.commit()


def create_discount_code(id):
    max = 3267132
    highest_discount = db.session.query(func.max(Discount.id))
    if highest_discount.scalar() is None:
        highest_discount_id = 0
    else:
        highest_discount_id = highest_discount.scalar() + 1
    to_hex = max - highest_discount_id
    hexed = hex(to_hex)
    db.session.add(Discount(user_id=id, code=hexed))
    db.session.commit()