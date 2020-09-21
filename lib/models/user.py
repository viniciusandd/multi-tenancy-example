from lib.models.base import BaseModel, db
from lib.models.item import Item
from lib.models.order import Order


class User(BaseModel):
    __tablename__ = "users"
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Unicode(), primary_key=True)
    name = db.Column(db.Unicode(), nullable=False)
    mail = db.Column(db.Unicode(), nullable=False)
    password = db.Column(db.Unicode(), nullable=False)
    organization_id = db.Column(db.Unicode(), nullable=False)

    @classmethod
    def _get_user_priced_orders(cls):
        return cls.session.query(
            User.name,
            Item.description,
            Item.price,
            Order.quantity,
            (Order.quantity * Item.price).label('Total')
            ).join(Order).join(Item)

    def get_my_priced_orders(self):
        query = self._get_user_priced_orders()
        orders = query.filter(User.id == self.id).all()
        return orders

    def get_my_priced_orders_jsonified(self):
        return [
            {
                "user_name": result[0],
                "item_description": result[1],
                "item_price": result[2],
                "order_quantity": result[3],
                "order_total": result[4]
            } for result in self.get_my_priced_orders()
        ]
