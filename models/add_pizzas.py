from flask_sqlalchemy import SQLAlchemy

import app
from models.sqlite_model import Courier

db = SQLAlchemy(app)

# TODO: In this file all the important basis info is inserted into the db
# only needs to be called once, but nice to have as file if something goes wrong with db

def add_everything():
    add_toppings()
    add_pizzas()
    add_items()
    add_districts()
    add_couriers()

def add_couriers():
    # TODO once relation to district is established each one is assigned a district
    db.session.add(Courier("Pieter"))
    db.session.add(Courier("Tom"))
    db.session.add(Courier("Christof"))
    db.session.add(Courier("Noah"))
    db.session.add(Courier("Filip"))
    db.session.add(Courier("PizzaBoy #1"))


def add_districts():
    pass


def add_pizzas():
    pass


def add_toppings():
    pass

def add_items():
    pass