#!/usr/bin/env python 3
""" flask app """
from flask import Flask
from flask import jsonify
 
app = Flask(__name__)
 
@app.route('/', methods=["GET"], strict_slashes=False)
def message():
    """ returns form payload """
    response = jsonify({"message": "Bienvenue"})
    return response
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
