from flask import Flask, render_template, jsonify
from random import randint
import RPi.GPIO as GPIO

# Configuring GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)


app = Flask(__name__)

@app.route('/')
def index(name=None):
    return render_template('index.html')

@app.route('/value')
def value():
    #TODO: inject GPIO value
    print 'value:', GPIO.input(12)
    return jsonify(value=GPIO.input(12))

if __name__ == "__main__":
  app.run('0.0.0.0')
