#!/usr/bin/env python3
""" flask app """
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=["GET"])
def hello():
    """ Base route """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def new_users():
    email = request.form['email']
    password = request.form['password']

    try:
        new_user = AUTH.register(email, password)
        return jsonify({'email': new_user.email, 'message': 'User Created'})
    except Exception as e:
        return jsonify({'message': 'Email already registered'}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
