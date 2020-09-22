from marshmallow import fields, Schema
from flask_marshmallow import Marshmallow

from lib.models.order import Order


ma = Marshmallow()

class OrdersPerUser(Schema):
    user_name = fields.String()
    item_description = fields.String()
    item_price = fields.Float()
    order_quantity = fields.Float()
    order_total = fields.Float()

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order

def init_app(app):
    ma.init_app(app)