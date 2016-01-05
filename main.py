from flask import Flask, render_template, jsonify
from random import randint

app = Flask(__name__)

@app.route('/')
def index(name=None):
    return render_template('index.html')

@app.route('/value')
def value():
    #TODO: inject GPIO value
    return jsonify(value=randint(0,1000))

if __name__ == "__main__":
  app.run('0.0.0.0')
