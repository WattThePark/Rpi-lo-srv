from flask import Flask, render_template, jsonify
from random import randint
import RPi.GPIO as GPIO

# Configuring GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)

# Main Flask application
app = Flask(__name__)

@app.route('/')
def index(name=None):
    """Getting index.html"""
    return render_template('index.html')

@app.route('/value')
def value():
    """Returns the GPIO12 value with a json serialization"""
    print 'value:', GPIO.input(12)
    return jsonify(value=GPIO.input(12))

if __name__ == "__main__":
  app.run('0.0.0.0')
