from flask import Flask, render_template, make_response, request
from config import Config
from controllers import menu_controller

app = Flask(__name__)


@app.route("/login", methods=["GET"])
def login_screen():
    return render_template("Login.html")


@app.route("/login", methods=["POST"])
def login():
    # TODO: Login logic connect to authentification system
    email = request.form["email"]
    password = request.form["password"]
    return make_response({"result": "success"}, 200);


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
    return make_response({"result": "success"}, 200);


@app.route("/order", methods=["GET"])
def show_menu():
    return render_template("Order.html", menu=menu_controller.get_menu())

@app.route("/order", methods=["POST"])
def place_order():
    # TODO: Create logic and view for placing orders
    return make_response({"result": "success"}, 200);
