from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user # import other models to create instances from here
from flask import flash # use flash to store validation messages


class Recipe:
    DB = 'recipes_schema'
    def __init__(self, data) -> None: # columns in database match instance attributes
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None

    # CRUD
    # CREATE
    @classmethod
    def add_recipe(cls, data):
        query = """INSERT INTO recipes (name, description, instructions, date_cooked, under_30, user_id)
                VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30)s, %(user_id)s)"""
        return connectToMySQL(cls.DB).query_db(query, data) # returns row ID of new user
    # READ
    @classmethod
    def get_recipe_by_id(cls, data): # get db row from recipe id
        query = """SELECT * FROM recipes
                JOIN users on users.id = user_id
                WHERE recipes.id = %(id)s"""
        results = connectToMySQL(cls.DB).query_db(query,data)
        db_row = results[0]
        # dictionary to send to model to create user instance
        this_row_user = {
                    'id': db_row['users.id'],
                    'first_name': db_row['first_name'],
                    'last_name': db_row['last_name'],
                    'email': db_row['email'],
                    'password': db_row['password'],
                    'created_at': db_row['users.created_at'],
                    'updated_at': db_row['users.updated_at'],
                }
        # dictionary to send to model to create recipe instance
        this_row_recipe = {
                    'id': db_row['id'],
                    'name': db_row['name'],
                    'description': db_row['description'],
                    'instructions': db_row['instructions'],
                    'date_cooked': db_row['date_cooked'],
                    'under_30': 'Yes' if db_row['under_30'] == 1 else 'No',
                    'created_at': db_row['created_at'],
                    'updated_at': db_row['updated_at']
                }
        # link recipe and user
        this_recipe = cls(this_row_recipe)
        this_recipe.owner = user.User(this_row_user)
        return this_recipe
    @classmethod
    def get_all_recipes(cls): # get all recipes using a join table for recipes and users
        # right join includes users who don't have any recipes...essentially getting all users!!!!
        query = """SELECT * FROM recipes
                RIGHT JOIN users ON user_id = users.id
                ORDER BY recipes.id DESC"""
        results = connectToMySQL(cls.DB).query_db(query) # results returned to a list
        if len(results) == 0:
            return 0
        all_recipes = []
        user_hash = {} # create a dictionary to store users
        for db_row in results:
            if db_row['users.id'] not in user_hash:

                # make instance of recipe owner if it doesn't exist already
                this_row_user = {
                    'id': db_row['users.id'],
                    'first_name': db_row['first_name'],
                    'last_name': db_row['last_name'],
                    'email': db_row['email'],
                    'password': db_row['password'],
                    'created_at': db_row['users.created_at'],
                    'updated_at': db_row['users.updated_at'],
                }
                user_hash[db_row['users.id']]= user.User(this_row_user) # add user to hash 
            # make instance of recipe if it exists
            if db_row['id']:
                this_row_recipe = {
                    'id': db_row['id'],
                    'name': db_row['name'],
                    'description': db_row['description'],
                    'instructions': db_row['instructions'],
                    'date_cooked': db_row['date_cooked'],
                    'under_30': 'Yes' if db_row['under_30'] == 1 else 'No',
                    'created_at': db_row['created_at'],
                    'updated_at': db_row['updated_at']
                }
                this_recipe = cls(this_row_recipe)
                # link the classes
                this_recipe.owner = user_hash[db_row['users.id']]
                user_hash[db_row['users.id']].recipes.append(this_recipe)
                all_recipes.append(this_recipe)
        return {
            'users': user_hash,
            'recipes': all_recipes
        }
    # UPDATE
    @classmethod
    def edit_recipe(cls, data): # nothing special here, just an update query
        query = """UPDATE recipes
                SET name = %(name)s, description = %(description)s, instructions = %(instructions)s,
                date_cooked = %(date_cooked)s, under_30 = %(under_30)s, user_id = %(user_id)s
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    # DELETE
    @classmethod
    def delete_recipe(cls,data): # delete recipe based on id
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)
    # static methods for user form validations
    @staticmethod
    def validate_new_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('Recipe name must have at least 3 characters.', 'recipe')
            is_valid = False
        if len(data['description']) < 3:
            flash('Description must have at least 3 characters.', 'recipe')
            is_valid = False
        if len(data['instructions']) < 3:
            flash('Instructions must have at least 3 characters.', 'recipe')
            is_valid = False
        if not data['date_cooked']:
            flash('Please enter a valid date cooked.', 'recipe')
            is_valid = False
        if 'under_30' not in data:
            flash('Missing response for Cooked Under 30 minutes.', 'recipe')
            is_valid = False
        return is_valid