from flask import Flask, render_template, make_response, request

app = Flask(__name__)

from controllers import menu_controller


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
    # TODO: Login logic connect to authentification system
    email = request.form["email"]
    password = request.form["password"]
    return make_response({"result": "success"}, 200)


@app.route("/register", methods=["GET"])
def register_screen():
    return render_template("Register.html")


@app.route("/register", methods=["POST"])
def register():
    # TODO: Register logic connect to authentification system
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    phone_number = request.form["phone_number"]
    birthday = request.form["birthday"]
    street = request.form["street"]
    addition = request.form["addition"]
    zip_code = request.form["zip_code"]
    city_name = request.form["city_name"]
    return make_response({"result": "success"}, 200)


@app.route("/menu", methods=["GET"])
def show_menu():
    return render_template("Menu.html", menu=menu_controller.get_menu())


@app.route("/card", methods=["POST"])
def add_to_card():
    # TODO: Create logic and adding to card
    return make_response({"result": "success"}, 200)


@app.route("/card", methods=["DELETE"])
def remove_from_card():
    # TODO: Create logic and remove from card
    return make_response({"result": "success"}, 200)


@app.route("/order", methods=["GET"])
def show_order():
    return render_template("Order.html", order=[])


@app.route("/order/confirmation", methods=["GET"])
def show_order_confirm():
    # TODO: Order Confirmation screen instead of Order screen
    return render_template("Order.html", order=[])


@app.route("/order", methods=["POST"])
def place_order():
    # TODO: Create logic and view for placing orders
    return make_response({"result": "success"}, 200)


@app.route("/order/cancel", methods=["PUT"])
def cancel_order():
    # TODO: Create logic and view for placing orders
    return make_response({"result": "success"}, 200)
