import os

from flask import Flask, jsonify, request
from lib.models import User, Order
from lib.schema import setup as setup_schema_selection
from lib.serealizer import OrdersPerUser, OrderSchema, init_app as serealizer_init_app


app = Flask(__name__)
setup_schema_selection(app)
serealizer_init_app(app)


@app.route('/orders', methods=["POST"])
def user_orders():
	user_id = request.json.get("user_id")
	new_user = User.get_or_create(
		name="hamza3",
		mail='hamza@gmail.com',
		password='ovious',
		organization_id='client3')
	print(new_user.id)
	user = User.get_by_id(user_id)
	orders = user.get_my_priced_orders_jsonified()
	return jsonify({
		"message": "orders successfully returned",
		"results": orders
	}), 200
	
@app.route('/')
def health_check():
    return "Api is up and running :)", 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
