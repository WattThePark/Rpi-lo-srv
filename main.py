from flask import Flask, request, session, g, redirect, url_for, abort, render_template, jsonify
import httplib, signal, sys
import RPi.GPIO as GPIO

# Configuring GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(22, GPIO.IN)

# Main Flask application
app = Flask(__name__)

@app.route('/')
def index(name=None):
    """Getting index.html"""
    return render_template('index.html')

@app.route('/value')
def value():
    """Returns the GPIO12 value with a json serialization"""
    print 'value12:', GPIO.input(12)
    print 'value16:', GPIO.input(16)
    print 'value22:', GPIO.input(22)
    return jsonify(value12=GPIO.input(12),
        value16=GPIO.input(16),
        value22=GPIO.input(22))

@app.route('/sendInfo', methods=['POST'])
def sendInfo():
    personId = request.form.get('personId')
    time = request.form.get('time')
    value = request.form.get('value')
    score = request.form.get('score')
    feedback = request.form.get('feedback')
    print personId, time, value
    conn = httplib.HTTPConnection("0.0.0.0:3000")
    conn.request("GET", "/insert/Result?idMachine=1&nameUser="+personId+"&time="+time+"&currentGenerated="+value+"&score="+score)
    res = conn.getresponse()
    return jsonify(status=res.status, reason=res.reason)

if __name__ == "__main__":
    app.run('0.0.0.0')
