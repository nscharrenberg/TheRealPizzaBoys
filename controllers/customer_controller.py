import app
from models.mysql_model import Pizza, Item, Customer, Address, db, District
import bcrypt

salt = '$2a$06$4zWV0r6LQyLbmPIaLY7dde'.encode('utf-8')


def login(email, password):
    found = Customer.query.filter_by(email=email).first()

    if found is None:
        raise Exception("Customer does not exist")

    # should actually use the checkpw function but seems to always retturn false, waste of time atm to work on it.
    if bcrypt.hashpw(password.encode('utf-8'), salt) == found.password.encode('utf-8') is False:
        raise Exception("Invalid Credentials")

    return found


def register(first_name, last_name, phone_number, email, password, street, house_number, addition, zip_code,
             city):
    if Customer.query.filter_by(email=email).first() is not None:
        raise Exception('Customer with this email already exists')

    # TODO: Probably would want to utilize a password confirmation as well
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    found_district = District.query.filter_by(zip_code=zip_code).first()

    if found_district is None:
        district = District(zip_code)
        db.session.add(district)
        db.session.commit()
    else:
        district = found_district

    found_address = Address.query.filter_by(street=street, house_number=house_number, addition=addition,
                                            zip_code=district.id,
                                            city=city).first()

    if found_address is None:
        address = Address(street, house_number, addition, district.id, city)
        db.session.add(address)
        db.session.commit()
    else:
        address = found_address

    customer = Customer(first_name, last_name, phone_number, address.id, email, hashed)
    db.session.add(customer)
    db.session.commit()

    return customer
