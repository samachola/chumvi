from flask import render_template, redirect, url_for, request, session, flash, json
from app import app, recipe, category, user
import re

Recipe = recipe.Recipe
User = user.User
Lecipe = user.Recipe
Category = user.Category

user_list = []
user_categories = []
current_person = {}

@app.route('/')
def index():
    session['show'] = True
    print("***********************current_user***************************")
    if 'current_user' in session:
        print(session['current_user'])
    print("***********************current_user***************************")
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
    current_person = {}
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
def category():
    session['show'] = True
    if request.method == 'GET':
        for person in user_list:
            if person.email == current_person['email'] :
                categories = person.categories
                return render_template('add_category.html', categories = person.categories)
            
        return render_template("add_category.html")
    else:
        new_category = Category(request.form['title'])
        if new_category:
            for person in user_list:
                if person.email == current_person['email'] :
                    person.categories.append(new_category)
                    print(person.categories)
                    return render_template('add_category.html', categories = person.categories)
        
    return render_template("add_category.html")


        
@app.route('/categori/<id>')
def deleteCategory(id):    
    for person in user_list:
        if person.email == current_person['email'] :
            print(current_person['email'])  
            #person.categories.remove(person.categories[id])
            for cat in person.categories:
                if cat.id == id:
                    print(id)        
            
            message = "Item successfully deleted"
            return redirect(url_for('category'))
        else:
            message = "Item not found"
            return render_template("add_category.html", categories = person.categories, error = message)


@app.route('/recipes')
def recipes():
    session['show'] = True
    return render_template("recipes.html")

@app.route('/addrecipe', methods=['GET', 'POST'])
def recipe():
    session['show'] = True
    if request.method == 'POST':
        resp = Recipe.addRecipe(request.form['title'], request.form['category'], request.form['ingredients'], request.form['process'])
        if resp['status']:
            print(resp['recipes'])
            session['recipes'] = resp['recipes']
            return redirect(url_for('recipes'))
        else:
            return render_template("add.html", error = resp['msg'])

    else:                   
        return render_template("add.html")


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    session['show'] = True
    resp = Recipe.viewRecipe(id)
    if request.method == 'GET':
        return render_template("edit.html", recipe = resp)
    else:
        response = Recipe.updateRecipe(id, request.form['title'], request.form['category'], request.form['ingredients'], request.form['process'])
        if response['status']:
            session['recipes'] = response['recipes']
            return redirect(url_for('recipes'))
        else:
            return render_template("edit.html", recipe = resp)
                     

@app.route('/view/<int:id>')
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

    
