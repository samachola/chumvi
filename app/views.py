from flask import render_template, redirect, url_for, request, session, flash, json, g
from app import app, recipe, category, user
import re
from functools import wraps

Recipe = user.Recipe
User = user.User
Lecipe = user.Recipe
Category = user.Category

user_list = []
current_person = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if bool(current_person) is False:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    session['show'] = True
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    session['show'] = False
    message = None
    if request.method == 'POST':
        if request.form['email'] == '' or request.form['password'] == '' or request.form['email'].isspace() or request.form['password'].isspace():
            message = "Email and Password Fields are Required"
            return render_template("login.html", message = message) 
        elif not check_mail(request.form['email']):
            message = "Enter a valid email address"
            return render_template("login.html", message = message)
        else: 
            if len(user_list) > 0:          
                for person in user_list:
                    if person.email == request.form['email'] and person.password == request.form['password']:
                        session['logged_in'] = True
                        print("***********************person***************************")
                        print(person.name)
                        current_person['email'] = person.email
                        current_person['categories'] = person.categories
                        current_person['recipes'] = person.recipes
                        print("***********************person***************************")
                        return redirect(url_for('index'))
                    
                    message = "Username and Password incorrect"
                session['logged_in'] = False
                return render_template("login.html", message = message)
            else:
                message = "User not available! Please register"
                return render_template("login.html", message = message)
                
    else:
        session['logged_in'] = False

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    current_person = None
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ 
    This method is creating a new user and 
    adding the user to the list of users in session.
    """
    session['show'] = False
    message = None   
    
    if request.method == 'POST':
                
        if not request.form['password'] or request.form['password'] == "":
            message = "Password is required"

        elif request.form['name'] == "" or request.form['name'].isspace():
            message = "Name cannot be an empty string"
        elif not check_mail(request.form['email']) or request.form['email'] == "":
            message = "Email provided is not valid"            
        else:
            for person in user_list:
                if person.email == request.form['email']:
                    message = 'User with the provided email already exists'
                    return render_template("register.html", error=message)


            new_user = User(request.form['name'], request.form['email'], request.form['password'])
            user_list.append(new_user)

            print(new_user.name)
            print(user_list)

            if new_user:
                return redirect(url_for('login'))
            else:
                return render_template("register.html", error = message)
            
    return render_template("register.html", error = message)

@app.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    session['show'] = True
    if request.method == 'GET':
        categories = current_person['categories']
        return render_template('add_category.html', categories = categories)
    else:
        new_category = Category(request.form['title'])
        if new_category:
            current_person['categories'].append(new_category)
            return render_template('add_category.html', categories = current_person['categories'])
            
        
    return render_template("add_category.html")


        
@app.route('/category/<int:id>')
@login_required
def deleteCategory(id):
    current_person['categories'].pop(id)
    return redirect(url_for('category'))


@app.route('/recipes')
@login_required
def recipes():
    session['show'] = True
    return render_template("recipes.html", recipes = current_person['recipes'])

@app.route('/addrecipe', methods=['GET', 'POST'])
@login_required
def recipe():
    session['show'] = True
    if request.method == 'POST':
        new_recipe = Recipe(request.form['title'], request.form['category'], request.form['ingredients'], request.form['process'])
        if new_recipe:
            current_person['recipes'].append(new_recipe)
            return redirect(url_for('recipes'))
        else:
            return render_template("add.html", error = "Could not add recipe")

    else:                   
        return render_template("add.html", categories = current_person['categories'])


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    session['show'] = True
    recipe = current_person['recipes'][id]
    if request.method == 'GET':
        return render_template("edit.html", recipe = recipe, id = id)
    else:
        current_person['recipes'].pop(id)
        update_recipe = Recipe(request.form['title'], request.form['category'], request.form['ingredients'], request.form['process'])
        if update_recipe:
            current_person['recipes'].append(update_recipe)
            return redirect(url_for('recipes'))
        else:
            return render_template("edit.html", recipe = recipe, id = id)
                     

@app.route('/view/<int:id>')
@login_required
def view(id):
    session['show'] = True
    print(id)
    resp = Recipe.viewRecipe(id)
    print(resp)
    #return render_template("view.html")
    
    if resp['status']:
        print(resp['title'])
        return render_template("view.html", recipe = resp)
    else:
        return redirect(url_for('recipes'))


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    resp = Recipe.deleteRecipe(id)

    if resp['status']:
        session['recipes'] = resp['recipes']
    
    return redirect(url_for('recipes'))

 

def check_mail(user_email):    
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', user_email)

    if match == None:
        return False
    else:
        return True

    
