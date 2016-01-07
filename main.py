from flask import Flask, request, session, g, redirect, url_for, abort, render_template, jsonify
import httplib, signal, sys, os
import RPi.GPIO as GPIO
import random

PORT = os.getenv('BIKE_PORT', 5000)

# Configuring GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(22, GPIO.IN)

# Main Flask application
app = Flask(__name__)

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/')
def index(name=None):
    """Getting index.html"""
    return render_template('index.html')

@app.route('/watt')
@crossdomain('*')
def watt():
    """Returns the GPIO12 value with a json serialization"""
    value = GPIO.input(12) | GPIO.input(16) << 1 | GPIO.input(22) << 2
    if value != 0:
        value = value + random.random()
        value = value * 6
    return str(value)

if __name__ == "__main__":
    app.run('0.0.0.0', PORT)
