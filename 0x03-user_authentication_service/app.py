#!/usr/bin/env python 3
""" flask app """
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def message():
    """ returns form payload """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
