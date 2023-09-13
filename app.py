#!/usr/bin/env python3
"""Basic flask app
"""
from os import getenv
from views.auth.auth import Auth
from flask import Flask, jsonify, request, abort, redirect, render_template


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index() -> str:
    """Returns a simple JSONIFY request
    """
    # return jsonify({"message": "Bienvenue"})
    return render_template('index.html')


@app.route('/signup')
def signup() -> str:
    """Returns a simple JSONIFY request
    """
    return render_template('sign_up.html')


@app.route('/users', methods=['POST'])
def register() -> str:
    """A function that impiments a POST method on the users table.

    Args:
        None

    Return:
        Return: A jsonify message
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # register user if user does not exist
    try:
        user = AUTH.register_user(email, password)
    except Exception:
        return jsonify({"message": "email already registered"}), 400
    
    return jsonify({"email": f"{email}", "message": "user created"}), 200


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)