from flask_app import app # import app to run routes
from flask import render_template, redirect, session, request, flash # flask modules for routes to work
from flask_app.models import user, recipe # import models

@app.route('/recipes')
def show_all_recipes():
    # database call to get all recipes and their owners
    all_data = recipe.Recipe.get_all_recipes()
    # if logged in user doesn't have any recipes get user info to personalize webpage
    # if not all_data:
    #     current_user = user.User.get_user_by_id({'id': session['user_id']}) 
    #     return render_template('all_recipes.html', current_user = current_user, all_recipes = 0)
    
    current_user = all_data['users'][session['user_id']]
    all_recipes = all_data['recipes'] if len(all_data['recipes']) > 0 else 0

    return render_template('all_recipes.html', current_user = current_user, all_recipes = all_recipes)

@app.route('/recipes/new')
def new_recipe():
    return render_template('new_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def process_new_recipe():
    print(request.form)
    if 'user_id' not in session: # user needs to be logged in to access
        return redirect('/')
    # validate new recipe form
    if not recipe.Recipe.validate_new_recipe(request.form):
        return redirect('/recipes/new')
    # dictionary to send to model to insert into database
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
        'under_30': request.form['under_30'],
        'user_id': session['user_id']
    }
    new_recipe_id = recipe.Recipe.add_recipe(data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>') # view on selected recipe
def show_one_recipe(id):
    if 'user_id' not in session: # must be logged in to access page
        return redirect('/')
    this_user = user.User.get_user_by_id({'id': session['user_id']}) # get user info for page personalization
    this_recipe = recipe.Recipe.get_recipe_by_id({'id': id}) # get recipe from db
    return render_template('show_one_recipe.html', this_user = this_user, this_recipe = this_recipe)

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session: # user must be logged in to edit page
        return redirect('/')
    this_recipe = recipe.Recipe.get_recipe_by_id({'id': id}) # get recipe from db
    if this_recipe.owner.id != session['user_id']: # if user doesn't own the recipe, return without doing damage
        return redirect('recipes')
    
    return render_template('edit_recipe.html', this_recipe = this_recipe)

@app.route('/recipes/edit/process', methods=['POST'])
def process_edited_recipe():
    if 'user_id' not in session: # gotta be logged in...still
        return redirect('/recipes')
    # validate new recipe form
    if not recipe.Recipe.validate_new_recipe(request.form):
        return redirect(f"/recipes/edit/{request.form['id']}")
    data = {
        'id': request.form['id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
        'under_30': request.form['under_30'],
        'user_id': session['user_id']
    }
    recipe.Recipe.edit_recipe(data)
    return redirect('/recipes')

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session: # user must be logged in to edit page
        return redirect('/')
    this_recipe = recipe.Recipe.get_recipe_by_id({'id': id}) # get recipe from db
    if this_recipe.owner.id != session['user_id']: # if user doesn't own the recipe, return without doing damage
        return redirect('recipes')
    print('id: ', id)
    recipe.Recipe.delete_recipe({'id': id})
    return redirect('/recipes')