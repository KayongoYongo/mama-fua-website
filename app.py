#!/usr/bin/env python3
"""Basic flask app
"""
from os import getenv
from views.auth.auth import Auth
from flask import Flask, jsonify, request, abort, redirect, render_template, url_for, make_response
from sqlalchemy.orm.exc import NoResultFound


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

@app.route('/login')
def login_route() -> str:
    """Returns a simple JSONIFY request
    """
    return render_template('log_in.html')

@app.route('/location')
def location() -> str:
    """Returns a simple JSONIFY request
    """
    return render_template('our_location.html')

@app.route('/contact')
def contact() -> str:
    """Returns a simple JSONIFY request
    """
    return render_template('contact.html')

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

    if not email:
        return jsonify({"email": "The email cannot be empty"})
        
    if not password:
        return jsonify({"password": "The password cannot be empty"})

    # register user if user does not exist
    try:
        user = AUTH.register_user(email, password)
    except Exception:
        return jsonify({"message": "email already registered"}), 400
    return redirect(url_for('login_route'))
    
@app.route('/sessions', methods=['POST'])
def login() -> str:
    """A function theat impliments a log in functionality

    Args:
        None

    Return:
        A JSONIFY message and return response
    """
    # Get the form data
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        # create a neww session
        session_id = AUTH.create_session(email)

        user = AUTH.get_user_from_session_id(session_id)
        response = make_response(render_template('user_dashboard.html', user=user))
        response.set_cookie('session_id', session_id)
        # print(session_id)
    
    return response

@app.route('/logout', methods=['POST'])
def logout() -> str:
    """This function impliments a log out function by
    deleting a session

    Args:
        None

    Return:
        Redirect request
    """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None or session_id is None:
        abort(403)

    print(session_id)
    print(user.id)
    
    try:
        AUTH.destroy_session(user.id)
    except NoResultFound:
        abort(403)
    else:
        return redirect(url_for('index'))
    
@app.route('/bookings', methods=['POST'])
def create_booking() -> str:
    """A function that impiments a POST method on the users table.

    Args:
        None

    Return:
        Return: A jsonify message
    """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)

    AUTH.create_booking(user.email)
    print(user.email)
    return render_template('user_dashboard.html', user=user)

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)