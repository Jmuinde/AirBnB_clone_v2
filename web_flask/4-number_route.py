#!/usr/bin/python3
'''Setting up a simple flask web application
'''
from flask import Flask
from markupsafe import escape

app = Flask(__name__)
'''Instancitiate the flask application'''
app.url_map.strict_slashes = False
@app.route('/')
def index():
	# The home page. 
	return "Hello HBNB!"

@app.route('/hbnb')
def hbnb():
	return "HBNB"
@app.route('/c/<text>')
def c (text):
	return f"C {escape(text)}".replace('_', ' ')

@app.route('/python/<text>')
@app.route('/python', defaults={'text': 'is cool'})
def python (text):
	return f"Python {escape(text)}".replace('_', ' ')


@app.route('/number/<int:n>')
def n(n):
	return f"{n} is a number"
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)
