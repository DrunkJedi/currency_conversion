import os
import requests

from flask import Flask, send_from_directory
from flask_restful import Resource, Api
from webargs import fields
from webargs.flaskparser import use_args
from apscheduler.schedulers.background import BackgroundScheduler

rates_token = "token must be here"
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return send_from_directory(static_file_dir, 'index.html')


class ApiResource(Resource):
    currency_args = {
        'from': fields.Str(required=True),
        'to': fields.Str(required=True),
        'value': fields.Float(required=True),
    }

    @use_args(currency_args)
    def get(self, args):
        rate_from = rates_data.get(args['from'])
        rate_to = rates_data.get(args['to'])
        value = args['value']
        return {'value': value * rate_to / rate_from}


api.add_resource(ApiResource, '/api/')


class RatesStore:
    def __init__(self):
        self.rates_data = None
        self.update_rates()
        sched = BackgroundScheduler(daemon=True)
        sched.add_job(self.update_rates, 'interval', hours=24)
        sched.start()

    def update_rates(self):
        params = {'app_id': rates_token}
        r = requests.get('https://openexchangerates.org/api/latest.json', params=params)
        self.rates_data = r.json()

    def get(self, arg):
        return self.rates_data.get('rates').get(arg)


if __name__ == '__main__':
    rates_data = RatesStore()
    app.run(debug=False)
