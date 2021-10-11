from flask_sqlalchemy import SQLAlchemy

import app
from models.mysql_model import Courier, District, Pizza, Topping, Item, db
from controllers.admin_controller import create_pizza


# In this file all the important basis info is inserted into the db
# only needs to be called once, but nice to have as file if something goes wrong with db

def add_everything():
    add_toppings()
    add_pizzas()
    add_items()
    add_districts()
    add_couriers()
    db.session.commit()


def add_districts():
    db.session.add(District(zip_code="6216"))  # noah
    db.session.add(District(zip_code="6217"))
    db.session.add(District(zip_code="6218"))
    db.session.add(District(zip_code="6219"))
    db.session.add(District(zip_code="6220"))
    db.session.add(District(zip_code="6221"))  # filip


def add_couriers():
    db.session.add(Courier("Noah", District.query.filter_by(zip_code="6216").first().id))
    db.session.add(Courier("Pieter", District.query.filter_by(zip_code="6217").first().id))
    db.session.add(Courier("Tom", District.query.filter_by(zip_code="6218").first().id))
    db.session.add(Courier("Christof", District.query.filter_by(zip_code="6219").first().id))
    db.session.add(Courier("PizzaBoy #1", District.query.filter_by(zip_code="6220").first().id))
    db.session.add(Courier("Filip", District.query.filter_by(zip_code="6221").first().id))
    db.session.add(Courier("PizzaBoy #2", District.query.filter_by(zip_code="6220").first().id))
    db.session.add(Courier("PizzaBoy #3", District.query.filter_by(zip_code="6220").first().id))
    db.session.add(Courier("PizzaBoy #4", District.query.filter_by(zip_code="6218").first().id))


def add_pizzas():
    sauce = Topping.query.filter_by(name="Marinara sauce").first()
    mozza = Topping.query.filter_by(name="Mozzarella").first()
    dough = Topping.query.filter_by(name="Dough").first()
    oregano = Topping.query.filter_by(name="Oregano").first()
    salami = Topping.query.filter_by(name="Salami").first()
    ham = Topping.query.filter_by(name="Prosciutto").first()
    sals = Topping.query.filter_by(name="Salsiccia").first()
    onions = Topping.query.filter_by(name="Onions").first()
    corn = Topping.query.filter_by(name="Corn").first()
    peppers = Topping.query.filter_by(name="Peppers").first()
    garlic = Topping.query.filter_by(name="Crushed garlic").first()
    mushroom = Topping.query.filter_by(name="Mushrooms").first()
    gold = Topping.query.filter_by(name="Gold leafs").first()
    truffel = Topping.query.filter_by(name="Tartufo").first()
    tuna = Topping.query.filter_by(name="Tonno").first()
    olives = Topping.query.filter_by(name="Olives").first()
    jala = Topping.query.filter_by(name="Jalapeños").first()

    create_pizza("Pizza Margarita", {sauce, mozza, dough, oregano})
    create_pizza("Pizza Salami", {sauce, mozza, dough, oregano, salami})
    create_pizza("Pizza Prosciutto", {sauce, mozza, dough, oregano, ham})
    create_pizza("Pizza 'Best Pizza of the world'", {sauce, mozza, dough, oregano, corn, jala, peppers})
    create_pizza("Vegetarian Pizza", {sauce, mozza, dough, oregano, peppers, corn, mushroom})
    create_pizza("Meatlovers Pizza", {sauce, mozza, dough, oregano, salami, salami, ham, sals, olives})
    create_pizza("Pizza del Jefe", {sauce, mozza, dough, oregano, peppers, onions, sals})
    create_pizza("Pizza della Casa",
                 {sauce, mozza, dough, oregano, salami, ham, sals, onions, corn, peppers, garlic, mushroom,
                  tuna, olives, jala})
    create_pizza("Pizza Tonno", {sauce, mozza, dough, oregano, tuna})
    create_pizza("Pizza Tonno e Cipolla", {sauce, mozza, dough, oregano, tuna, onions})
    create_pizza("Pizza Tonno e Oliva", {sauce, mozza, dough, oregano, tuna, olives})
    create_pizza("Pizza Databa$e", {sauce, mozza, dough, oregano, truffel})
    create_pizza("Pizza Melano", {sauce, mozza, dough, oregano, gold, truffel})


def add_toppings():
    db.session.add(Topping("Marinara sauce", True, 1.13))
    db.session.add(Topping("Mozzarella", True, 2.5))
    db.session.add(Topping("Dough", True, 1.5))
    db.session.add(Topping("Oregano", True, 0.5))
    db.session.add(Topping("Salami", False, 2.0))
    db.session.add(Topping("Prosciutto", False, 2.0))
    db.session.add(Topping("Tonno", False, 2.0))
    db.session.add(Topping("Salsiccia", False, 2.5))
    db.session.add(Topping("Onions", True, 1.0))
    db.session.add(Topping("Jalapeños", True, 1.0))
    db.session.add(Topping("Olives", True, 1.0))
    db.session.add(Topping("Corn", True, 1.0))
    db.session.add(Topping("Peppers", True, 1.0))
    db.session.add(Topping("Crushed garlic", True, 1.0))
    db.session.add(Topping("Mushrooms", True, 1.0))
    db.session.add(Topping("Gold leafs", True, 100.0))
    db.session.add(Topping("Tartufo", True, 69.0))


def add_items():
    db.session.add(Item("Coca Cola 0.3l", 3.0))
    db.session.add(Item("Coca Cola 0.5l", 3.5))
    db.session.add(Item("Fanta 0.3l", 3.0))
    db.session.add(Item("Fanta 0.5l", 3.5))
    db.session.add(Item("Coca Cola Light 0.3l", 3.0))
    db.session.add(Item("Coca Cola Light 0.5l", 3.5))
    db.session.add(Item("Coca Cola Zero 0.3l", 3.0))
    db.session.add(Item("Coca Cola Zero 0.5l", 3.5))
    db.session.add(Item("Fanta Cassis 0.3l", 3.0))
    db.session.add(Item("Fanta Cassis 0.5l", 3.5))
    db.session.add(Item("Pisang Ambon 1 jiggers", 3.0))
    db.session.add(Item("Pisang Ambon 3 jiggers", 3.5))
    db.session.add(Item("Beer 0.3l", 3.0))
    db.session.add(Item("Beer 0.5l", 3.5))
    db.session.add(Item("Kebab Sandwich", 5.5))
    db.session.add(Item("Dürüm", 6.0))
    db.session.add(Item("Sushi small portion", 10.0))
    db.session.add(Item("Sushi big portion", 22.5))
    db.session.add(Item("Opor Ayam Tahu Telur", 8.5))
    db.session.add(Item("Ice Cream Chocolate", 3.0))
    db.session.add(Item("Ice Cream Vanilla", 3.0))
    db.session.add(Item("Tiramisu", 5.5))
    db.session.add(Item("Limoncello", 2.0))
    db.session.add(Item("Chocolate Cake", 3.0))
