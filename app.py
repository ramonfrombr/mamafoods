from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os


app = Flask(__name__)

diretoriobase = os.path.abspath(os.path.dirname(__file__))

# Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(diretoriobase, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa banco de dados
db = SQLAlchemy(app)

# Inicializa serializador
ma = Marshmallow(app)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128))

    #vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))

    """
    vendor = db.relationship(
        'Vendor',
        backref=db.backref("orders", cascade="all, delete-orphan")
    )
    """

    variant = db.Column(db.String(64))

    status = db.Column(db.String(64))
    requires_shipping = db.Column(db.Boolean)
    taxable = db.Column(db.Boolean)

    discount_code = db.Column(db.String(64))
    total_discount = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    paid_by_mama = db.Column(db.Boolean)

    quantity = db.Column(db.Integer)
    
    notes = db.Column(db.String(256))

    client_name = db.Column(db.String(64))

    requested_to_caterer = db.Column(db.Boolean)
    request_confirmed = db.Column(db.Boolean)

    picked_from_caterer = db.Column(db.Boolean)
    picked_up_temperature = db.Column(db.Float)
    pickup_datetime_end = db.Column(db.DateTime)
    pickup_datetime_start = db.Column(db.DateTime)

    billing_name = db.Column(db.String(64))
    billing_address = db.Column(db.String(64))
    billing_city = db.Column(db.String(64))
    billing_province = db.Column(db.String(64))
    billing_zip = db.Column(db.String(64))


# Schema do Order
class OrderSchema(ma.Schema):

    class Meta:

        fields = ('id', 'name', 'subtotal', 'quantity', 'notes')

# Inicializa os schemas
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


# API Routes

@app.route('/orders', methods=['GET'])
def orders():

    orders = Order.query.all()
    return orders_schema.jsonify(orders)


@app.route('/orders/<int:id>')
def order(id):

    order = Order.query.get(id)
    return order_schema.jsonify(order)


@app.route('/orders', methods=['POST'])
def add_order():

    order = Order(**request.json)
    db.session.add(order)
    db.session.commit()
    return order_schema.jsonify(order)


@app.route('/orders/<int:id>', methods=['PUT'])
def edit_order(id):

    order = Order.query.get(id)

    order.name = request.json['name']
    order.subtotal = request.json['subtotal']
    order.quantity = request.json['quantity']
    order.notes = request.json['notes']

    db.session.add(order)
    db.session.commit()
    return order_schema.jsonify(order)


@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):

    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()
    return order_schema.jsonify(order)




# Ativa o servidor
if __name__ == '__main__':
    app.run(debug=True)


