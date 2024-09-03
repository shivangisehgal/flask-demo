#https://github.com/rycus86/prometheus_flask_exporter
#Flask-HTTPAuth==4.7.0

from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth
from prometheus_flask_exporter import PrometheusMetrics
import time

app = Flask(__name__)
auth = HTTPBasicAuth()
metrics = PrometheusMetrics(app, metrics_decorator=auth.login_required)

@auth.verify_password
def verify_password(username, password):
    return username == 'admin' and password == 'securepassword'

metrics.info('simple_app', 'Simple Flask Application', version='1.0.0')

@app.route('/')
@metrics.counter('page_visits', 'Total number of visits to the home page')
def home():
    return "Hello! This is the Home Page."

@app.route('/enter')
@metrics.gauge('people_online', 'Number of people currently online')
def enter():
    return "Someone entered. People online gauge increased."

@app.route('/exit')
@metrics.gauge('people_online', 'Number of people currently online')
def exit():
    return "Someone exited. People online gauge decreased."

@app.route('/data')
@metrics.histogram('data_response_time', 'Response time for data requests')
def get_data():
    time.sleep(0.3)
    return "Here is your data!"

@app.route('/greet/<name>')
@metrics.summary('greet_time_summary', 'Summary of response times for greeting requests')
def greet(name):
    time.sleep(0.1)
    return f"Hello, {name}!"

@app.route('/metrics')
def custom_metrics():
    response_data, content_type = metrics.generate_metrics()
    return Response(response=response_data, content_type=content_type)

@app.route('/items/<item_type>')
@metrics.counter('item_access_count', 'Count of item access by type', labels={'item_type': lambda: request.view_args['item_type']})
def get_item(item_type):
    return f"Item type: {item_type}"

@app.route('/long-task')
@metrics.gauge('long_task_in_progress', 'Number of long-running tasks in progress')
def long_task():
    time.sleep(5)
    return "Long-running task completed!"

@app.route('/ignore')
@metrics.do_not_track()
def ignore():
    return "This route is not tracked by Prometheus."

@app.route('/health')
def health():
    return "Health check OK - Not tracked by Prometheus"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
