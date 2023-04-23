from flask_app import app # import app to run routes
from flask import render_template, redirect, session, request, jsonify # flask modules for routes to work
from flask_app.models import user # import models
from flask_bcrypt import Bcrypt # import bcrypt to hash and encrypt passwords

bcrypt = Bcrypt(app) # create an object called bcrypt using app as the argument

@app.route('/') # loads default registration/login page
def load_login_page():
    if 'user_id' not in session: # if session hasn't been set, load the login page
        return render_template('login.html')
    return redirect('/recipes') # otherwise go to the user's wall page

@app.route('/register', methods=['POST'])
def register_user():
    validation = user.User.validate_registration(request.form) # validate user input to match required criteria
    if not validation['is_valid']: 
        return jsonify(messages = validation['messages'])
    pw_hash = bcrypt.generate_password_hash(request.form['password']) # create a password hash
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email'],
        'password' : pw_hash # store password hash rather than the actual password
    }
    session['user_id'] = user.User.add_user(data) # set user id to what is returned from query
    return redirect('/recipes')
@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    user_in_db = user.User.get_user_by_email({'email': request.form['email']})
    if not user_in_db:
        return jsonify(message = 'Invalid username/password')
    # compare hash of entered password to hash saved in database
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        print('password is incorrect')
        return jsonify(message = 'Invalid username/password')
    session['user_id'] = user_in_db.id
    return redirect('/recipes')
@app.route('/logout') # log out user by clearing session and redirecting to /
def logout():
    session.clear()
    return redirect('/')
