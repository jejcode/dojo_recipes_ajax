from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user,recipe # import other models to create instances from here
from flask import flash # use flash to store validation messages

import re # import regex to validate email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') # string to ensure valid email address
PASS_REGEX = re.compile(r'^(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9!@#$%^&*()]{8,})$') # string to check password for letters and numbers

class User:
    DB = 'recipes_schema'
    def __init__(self, data) -> None: # columns in database match instance attributes
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    # CRUD
    # CREATE
    @classmethod
    def add_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s)"""
        return connectToMySQL(cls.DB).query_db(query, data) # returns row ID of new user
    # READ
    @classmethod
    def get_user_by_id(cls, data): # get user info to personalize web page
        query = "SELECT * FROM users where id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data) # results is a one item list
        # make an instance of user and return
        return cls(results[0])
    @classmethod
    def get_user_by_email(cls, data): # get db row from user email
        query = "SELECT * FROM users where email = %(email)s"
        results = connectToMySQL(cls.DB).query_db(query, data) # results in a list of one
        if len(results) < 1:
            return 0
        return cls(results[0]) # create an instance from db row and return it
    # static methods for user form validations
    @staticmethod
    def validate_registration(data):
        json_data = {
            'is_valid': True,
            'messages': []
        }
        if len(data['fname']) < 2:
            json_data['messages'].append('First name must have at least 2 characters.')
            json_data['is_valid'] = False
        if len(data['lname']) < 2:
            json_data['messages'].append('Last name must have at least 2 characters.')
            json_data['is_valid'] = False
        if not EMAIL_REGEX.match(data['email']): 
            json_data['messages'].append('Invalid email address!')
            json_data['is_valid'] = False
        if User.get_user_by_email({'email': data['email']}):
            json_data['messages'].append('Email is already in use.')
            json_data['is_valid'] = False
        if not PASS_REGEX.match(data['password']):
            json_data['messages'].append('Password must contain at least one letter, one number, and be at least 8 characters long.')
            json_data['is_valid'] = False
        if data['confirm'] != data['password']:
            json_data['messages'].append('Password does not match confirm password')
            json_data['is_valid'] = False
        return json_data