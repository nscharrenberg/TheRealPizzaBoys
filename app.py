import flask
import flask_login
from flask import Flask, render_template, make_response, request

app = Flask(__name__)
app.secret_key = 'topsecretkeythatonlyweknow'  # would usually store this as an environmental variable

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

from models.sqlite_model import Customer

@login_manager.user_loader
def user_loader(email):
    user = Customer.query.filter_by(email=email).first()

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
        customer = customer_controller.register(request.form['first_name'], request.form['last_name'],
                                                request.form['phone_number'], request.form['birthday'],
                                                request.form['email'],
                                                request.form['password'], request.form['street'],
                                                request.form['house_number'],
                                                request.form['addition'], request.form['zipcode'],
                                                request.form['city'])

        flask_login.login_user(customer)
        return flask.redirect(flask.url_for('home'))
    except Exception as ex:
        return make_response(ex, 500)


@app.route("/register", methods=["GET"])
def register_screen():
    return render_template("Register.html")


@app.route("/register", methods=["POST"])
def register():
    try:
        customer = customer_controller.register(request.form['first_name'], request.form['last_name'],
                                                request.form['phone_number'], request.form['birthday'],
                                                request.form['email'],
                                                request.form['password'], request.form['street'],
                                                request.form['house_number'],
                                                request.form['addition'], request.form['zipcode'],
                                                request.form['city'])

        flask_login.login_user(customer)
        return flask.redirect(flask.url_for('home'))
    except Exception as ex:
        return make_response(ex, 500)


@app.route("/menu", methods=["GET"])
def show_menu():
    return render_template("Menu.html", pizzas=menu_controller.get_pizzas(), items=menu_controller.get_items())


@app.route("/card", methods=["POST"])
def add_to_card():
    # TODO: Create logic and adding to card
    return make_response({"result": "success"}, 200)


@app.route("/card", methods=["DELETE"])
def remove_from_card():
    # TODO: Create logic and remove from card
    return make_response({"result": "success"}, 200)


@app.route("/order", methods=["GET"])
@flask_login.login_required
def show_order():
    return render_template("Order.html", order=[])


@app.route("/order/confirmation", methods=["GET"])
@flask_login.login_required
def show_order_confirm():
    # TODO: Order Confirmation screen instead of Order screen
    return render_template("Order.html", order=[])


@app.route("/order", methods=["POST"])
@flask_login.login_required
def place_order():
    # TODO: Create logic and view for placing orders
    return make_response({"result": "success"}, 200)


@app.route("/order/cancel", methods=["PUT"])
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
    return flask.redirect(flask.url_for('home'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect(flask.url_for('login'))
