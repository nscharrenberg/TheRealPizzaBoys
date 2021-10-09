from flask import jsonify

from models.sqlite_model import Pizza, db, PizzaTopping


def create_pizza(name, toppings):
    pizza = Pizza(name, toppings)
    db.session.add(pizza)

    new_toppings = dict()
    for topping in toppings:
        if topping in new_toppings:
            new_toppings[topping] = new_toppings.get(toppings) + 1

        new_toppings[topping] = 1

    for topping, quantity in new_toppings.items():
        pizza_topping = PizzaTopping(pizza.id, topping.id, quantity)
        db.session.add(pizza_topping)

    db.session.commit()






