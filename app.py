#!/usr/bin/env python3
"""Basic flask app
"""
from os import getenv
import os
from views.auth.auth import Auth
from flask import Flask, jsonify, request, abort, redirect, render_template, url_for, make_response, flash, session
from sqlalchemy.orm.exc import NoResultFound
from flask_mail import Mail, Message


app = Flask(__name__)

AUTH = Auth()


app.secret_key = 'your_secret_key_here'

# Configure email settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # e.g., smtp.gmail.com for Gmail
app.config['MAIL_PORT'] = 587  # Port for TLS (587 for Gmail)
app.config['MAIL_USE_TLS'] = True  # Use TLS (True for Gmail)
app.config['MAIL_USE_SSL'] = False  # Use SSL (False for Gmail)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Your email address
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Your email password

mail = Mail(app)

@app.route('/')
def index() -> str:
    """Returns a simple JSONIFY request
    """
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

@app.route('/about')
def about() -> str:
    """Returns a simple JSONIFY request
    """
    return render_template('about_us.html')

@app.route('/admin_dashboard')
def admin_dashboard() -> str:
    """Returns a simple JSONIFY request
    """
    # Get the details for rendering the page
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)

    return render_template('admin_dashboard.html', user=user)
@app.route('/user_dashboard')
def user_dashboard() -> str:
    """Returns a simple JSONIFY request
    """
    # Get the details for rendering the page
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)

    return render_template('user_dashboard.html', user=user)

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
    repeatPassword = request.form.get('repeatPassword')
    first_name = request.form.get('first_name')
    second_name = request.form.get('second_name')
    phone_number = request.form.get('phone_number')     

    if not first_name or not second_name or not email or not password or not repeatPassword or not phone_number:
        flash("No field should be left empty", "error")

    if password != repeatPassword:
        flash ("The passwords do not match", "error")

    # If there are flash messages, redirect to the signup page with the messages
    if "_flashes" in session:
        return redirect(url_for('signup'))
    
    # register user if user does not exist
    try:
        AUTH.register_user(email, password, first_name, second_name, phone_number)
    except Exception:
        flash ("The email already exists")
        # If there are flash messages, redirect to the signup page with the messages
        if "_flashes" in session:
            return redirect(url_for('signup'))
        
    return redirect(url_for('login_route'))
    
@app.route('/login', methods=['POST'])
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

    # If there are flash messages, redirect to the signup page with the messages
    if not email or not password:
        flash("No field should be left empty", "error")
        return redirect(url_for('login'))

    if not AUTH.valid_login(email, password):
        flash("Invalid email or password.", "error")
        return redirect(url_for('login'))
        
    # create a new session
    session_id = AUTH.create_session(email)

    user = AUTH.get_user_from_session_id(session_id)

    if user.first_name == "ADMIN":
        response = make_response(render_template('admin_dashboard.html', user=user))
        response.set_cookie('session_id', session_id)
        return response

    response = make_response(render_template('user_dashboard.html', user=user))
    response.set_cookie('session_id', session_id)
    
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
    
@app.route('/booking_dashboard', methods=['POST'])
def create_booking() -> str:
    """A function that impiments a POST method on the users table.

    Args:
        None

    Return:
        Return: A jsonify message
    """
    # Store form data in variables
    pickup_date = request.form.get('datePicker')
    pickup_time = request.form.get('pickupTime')
    delivery_time = request.form.get('deliveryTime')
    location = request.form.get('location')

    # Validate form data
    if not pickup_date or not pickup_time or not delivery_time or not location:
        flash("No field should be left empty", "error")

    # Aquire the users details from the current session ID
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)

    # This is used  to show aall the bookings based on the users email
    bookings = AUTH.find_all_bookings(user.email)

    # This function creates the booking instance
    created_booking = AUTH.create_booking(user.email, pickup_date, pickup_time, delivery_time, location)

    if created_booking == None:
        flash ("Cannot create a new booking unless the previos one is completed")
    
    if "_flashes" in session:
        return redirect(url_for('view_booking'))

    return render_template('booking_dahsboard.html', user=user, bookings=bookings)

@app.route('/view_booking', methods=['GET'])
def view_booking() -> str:
    """A function that impiments a POST method on the users table.

    Args:
        None

    Return:
        Return: A jsonify message
    """
    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        return redirect(url_for('login_route'))
    
    print(session_id)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
    # If the user is not found (e.g., session_id is invalid), also redirect to the login page
        return redirect(url_for('login_route'))
    
    print(user.first_name)
    
    bookings = AUTH.find_all_bookings(user.email)
    print(bookings)
    
    return render_template('booking_dahsboard.html', user=user, bookings=bookings)

@app.route('/view_user_bookings', methods=['POST'])
def view_user_bookings() -> str:
    """A function that impiments a POST method on the users table.

    Args:
        None

    Return:
        Return: A jsonify message
    """
    
    status = request.form.get('status')
    print(status)

    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    
    bookings = AUTH.find_all_users_bookings(status)
    print(bookings)
    
    return render_template('admin_booking_dahsboard.html', user=user, bookings=bookings)

@app.route('/update_bookings', methods=['POST'])
def update_bookings() -> str:
    """A function that impiments a POST method on the users table.

    Args:
        None

    Return:
        Return: A jsonify message
    """
    id = request.form.get('bookingID')
    expected_date = request.form.get('datePicker')
    status = request.form.get('status')
    cost = request.form.get('cost')
    
    AUTH.update_bookings(id, status, expected_date, cost)

    # Get the details for rendering the page
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    bookings = AUTH.find_all_users_bookings(status)

    if not id or not expected_date or not status or not cost:
        flash("No field should be left empty", "error")
        return render_template('admin_booking_dahsboard.html', user=user, bookings=bookings)
    
    return render_template('admin_booking_dahsboard.html', user=user, bookings=bookings)

@app.route('/send_email', methods=['POST'])
def send_email():
        
    recipient = request.form['recipient_email']
    status = request.form.get('status')

    subject = "The laundry status has been updated"

    msg = Message(subject=subject,
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[recipient])
    
    print(status)
    # Set the email body
    msg.body = "The laundry status has been updated. Please log in and check your dashboard"

    mail.send(msg)

    # Get the details for rendering the page
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    bookings = AUTH.find_all_users_bookings(status)

    return render_template('admin_booking_dahsboard.html', user=user, bookings=bookings)

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)