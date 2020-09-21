import os

from flask import Flask, jsonify, request
from lib.models import User, Order, init_app as models_init_app
from lib.schema import setup as setup_schema_selection
from lib.serealizer import OrdersPerUser, OrderSchema, init_app as serealizer_init_app


app = Flask(__name__)

models_init_app(app)
setup_schema_selection(app)
serealizer_init_app(app)

@app.route('/orders', methods=["POST"])
def user_orders():
	user_id = request.json.get("user_id")
	user = User.get_by_id(user_id)
	orders = user.get_my_priced_orders_jsonified()
	return OrdersPerUser(many=True).dumps(orders)

@app.route("/order", methods=["POST"])
def order_by_id():
	order_id = request.json.get("order_id")
	order = Order.get_by_id(order_id)
	return OrderSchema().jsonify(order)

@app.route('/order/add', methods=["POST"])
def add_order():
	id = request.json.get("id")
	user_id = request.json.get("user_id")
	item_id = request.json.get("item_id")
	quantity = request.json.get("quantity")
	order = Order(
		id=id,
		user_id=user_id, 
		item_id=item_id, 
		quantity=quantity)
	order.save()
	return OrderSchema().jsonify(order)
	
@app.route('/')
def health_check():
    return "Api is up and running :)", 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
