from app import db


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    isVeggy = db.Column(db.Boolean, default=False)
    price = db.Column(db.Numeric)

    def __repr__(self):
        return '<Pizza %r>' % self.name
