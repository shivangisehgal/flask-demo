#pip install -r requirements.txt
from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import random
import math

app = Flask(__name__)


metrics = PrometheusMetrics(app)

visit_counter = metrics.counter(
    'visit_requests_total', 'Total number of visit requests', labels={'endpoint': lambda: request.endpoint}
)
task_duration_histogram = metrics.histogram(
    'task_duration_seconds', 'Time taken to complete tasks', labels={'endpoint': lambda: request.endpoint}
)
latest_random_number_gauge = metrics.gauge(
    'latest_random_number', 'The latest random number generated'
)

@app.route('/hello', methods=['GET'])
@visit_counter
@task_duration_histogram
def greet():
    name = request.args.get('name', 'Guest')
    message = f"Hello, {name}!"
    return jsonify({'message': message}), 200

@app.route('/add', methods=['GET'])
@visit_counter
@task_duration_histogram
def add():

   # /add?num1=5&num2=10
    try:
        num1 = float(request.args.get('num1'))
        num2 = float(request.args.get('num2'))
        result = num1 + num2
        return jsonify({'result': result}), 200
    except (TypeError, ValueError):
        return jsonify({'error': 'Please provide valid numbers for num1 and num2'}), 400

@app.route('/random', methods=['GET'])
@visit_counter
@task_duration_histogram
def generate_random():

    # random number

    number = random.randint(1, 100)
    latest_random_number_gauge.set(number)
    return jsonify({'random_number': number}), 200

@app.route('/factorial', methods=['GET'])
@visit_counter
@task_duration_histogram
def factorial():
    """
    Calculates the factorial of a provided number.
    Example: /factorial?number=5
    """
    try:
        number = int(request.args.get('number'))
        if number < 0:
            return jsonify({'error': 'Please provide a non-negative integer'}), 400
        result = math.factorial(number)
        return jsonify({'number': number, 'factorial': result}), 200
    except (TypeError, ValueError):
        return jsonify({'error': 'Please provide a valid integer for number'}), 400

# Default metrics endpoint
metrics.info('app_info', 'Application info', version='1.0.0')

if __name__ == '__main__':
    app.run(debug=True, port=5000)


# from flask import Flask, request, jsonify
# from prometheus_flask_exporter import PrometheusMetrics
# import random
# import time

# app = Flask(__name__)

# # Initialize PrometheusMetrics
# metrics = PrometheusMetrics(app)

# # Custom metrics
# order_counter = metrics.counter(
#     'total_orders', 'Total number of food orders', labels={'item': lambda: request.args.get('item', 'unknown')}
# )
# task_duration_histogram = metrics.histogram(
#     'task_duration_seconds', 'Time taken to complete tasks', labels={'endpoint': lambda: request.endpoint}
# )
# latest_bill_gauge = metrics.gauge(
#     'latest_bill_amount', 'The latest bill amount calculated'
# )
# error_counter = metrics.counter(
#     'order_errors', 'Total number of errors in ordering', labels={'error_type': lambda: request.args.get('error_type', 'unknown')}
# )
# success_ratio = metrics.summary(
#     'order_success_ratio', 'Ratio of successful orders'
# )
# active_customers_gauge = metrics.gauge(
#     'active_customers', 'Number of customers currently in the canteen'
# )

# # Track active customers (for demo purposes)
# active_customers = 0

# @app.before_request
# def before_request():
#     global active_customers
#     active_customers += 1
#     active_customers_gauge.set(active_customers)

# @app.after_request
# def after_request(response):
#     global active_customers
#     active_customers -= 1
#     active_customers_gauge.set(active_customers)
#     return response

# @app.route('/menu', methods=['GET'])
# @task_duration_histogram
# def get_menu():
#     """
#     Returns the canteen menu with prices.
#     """
#     menu = {
#         'Samosa': 10,
#         'Masala Dosa': 50,
#         'Chai': 5,
#         'Pav Bhaji': 40,
#         'Gulab Jamun': 20
#     }
#     return jsonify({'menu': menu}), 200

# @app.route('/order', methods=['GET'])
# @order_counter
# @task_duration_histogram
# def place_order():
#     """
#     Places an order for a given food item.
#     Example: /order?item=Samosa&quantity=2
#     """
#     menu = {
#         'Samosa': 10,
#         'Masala Dosa': 50,
#         'Chai': 5,
#         'Pav Bhaji': 40,
#         'Gulab Jamun': 20
#     }

#     item = request.args.get('item')
#     quantity = request.args.get('quantity', type=int)

#     if item not in menu:
#         error_counter.inc(error_type='invalid_item')
#         success_ratio.observe(0)
#         return jsonify({'error': f'Item {item} not found in menu'}), 400

#     if quantity <= 0:
#         error_counter.inc(error_type='invalid_quantity')
#         success_ratio.observe(0)
#         return jsonify({'error': 'Quantity must be greater than zero'}), 400

#     total = menu[item] * quantity
#     latest_bill_gauge.set(total)
#     success_ratio.observe(1)
#     return jsonify({'item': item, 'quantity': quantity, 'total': total}), 200

# @app.route('/bill', methods=['GET'])
# @task_duration_histogram
# def calculate_bill():
#     """
#     Calculates the total bill for a list of items and their quantities.
#     Example: /bill?items=Samosa,Chai&quantities=2,3
#     """
#     menu = {
#         'Samosa': 10,
#         'Masala Dosa': 50,
#         'Chai': 5,
#         'Pav Bhaji': 40,
#         'Gulab Jamun': 20
#     }

#     items = request.args.getlist('items')
#     quantities = request.args.getlist('quantities', type=int)

#     if len(items) != len(quantities):
#         error_counter.inc(error_type='mismatch')
#         return jsonify({'error': 'Items and quantities list must be of the same length'}), 400

#     total_bill = 0
#     for item, quantity in zip(items, quantities):
#         if item not in menu:
#             error_counter.inc(error_type='invalid_item')
#             return jsonify({'error': f'Item {item} not found in menu'}), 400

#         if quantity <= 0:
#             error_counter.inc(error_type='invalid_quantity')
#             return jsonify({'error': f'Quantity for {item} must be greater than zero'}), 400

#         total_bill += menu[item] * quantity

#     latest_bill_gauge.set(total_bill)
#     success_ratio.observe(1)
#     return jsonify({'total_bill': total_bill}), 200

# @app.route('/chai_break', methods=['GET'])
# @task_duration_histogram
# def chai_break():
#     """
#     Simulates a chai break with a random delay.
#     """
#     delay_time = random.uniform(1, 5)
#     time.sleep(delay_time)
#     success_ratio.observe(1)
#     return jsonify({'message': f'Chai break completed in {delay_time:.2f} seconds'}), 200

# # Default metrics endpoint
# metrics.info('canteen_info', 'Canteen application info', version='1.0.0')

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
