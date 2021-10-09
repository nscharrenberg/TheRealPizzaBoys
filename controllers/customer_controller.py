from models.sqlite_model import Pizza, Item, Customer, Address, db
import bcrypt


def login(email, password):
    found = Customer.query.filter_by(email=email).first()

    if found is None:
        raise Exception("Customer does not exist")

    if bcrypt.checkpw(bcrypt.hashpw(password, bcrypt.gensalt()), found.password) is not True:
        raise Exception("Invalid Credentials")

    return found


def register(first_name, last_name, phone_number, birthday, email, password, street, house_number, addition, zip_code,
             city):
    if Customer.query.filter_by(email=email).exists().scalar():
        raise Exception('Customer with this email already exists')

    # TODO: Probably would want to utilize a password confirmation as well
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    found_address = Address.query.filter_by(street=street, hous_number=house_number, addition=addition, zip_code=zip_code,
                                         city=city).first()

    if found_address is None:
        address = Address(street, house_number, addition, zip_code, city)
        db.session.add(address)
        db.session.commit()
    else:
        address = found_address

    customer = Customer(first_name, last_name, phone_number, address.id, birthday, email, hashed)
    db.session.add(customer)
    db.session.commit()

    return customer
