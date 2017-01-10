#! /bin/usr/python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return "Hello I am working Here!"
if __name__=="__main__":
	app.run()

