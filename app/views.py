from flask import render_template, redirect, url_for, request, session, flash
from app import app, recipe, category, user

Recipe = recipe.Recipe
Category = category.Category
User = user.User

@app.route('/')
def index():
    session['show'] = True
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    session['show'] = False
    message = None
    if request.method == 'POST':
        if request.form['email'] == '' or request.form['password'] == '':
            message = "Email and Password Fields are Required"
            return render_template("login.html", message = message) 
        elif request.form['email'] != session['user']['email']:
            message = "Cannot find user with the provided email"
            return render_template("login.html", message = message)
        elif request.form['password'] != session['user']['password']:
            message = "Password provided is incorrect"
            return render_template("login.html", message = message) 
        else:
                        
            session['logged_in'] = True            
            return redirect(url_for('index'))
    else:
        session['logged_in'] = False
        
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    session['show'] = False
    message = None
    
    if request.method == 'POST':        
        if not request.form['name'] or not request.form['email'] or not request.form['password']:
            message = "All input fields are required"
        else:
            response = User.registerUser(request.form['name'], request.form['email'], request.form['password'])
            if response['status']:
                session['user'] = response['user']
                return redirect(url_for('login'))
            else:
                message = response['message']
                return render_template("register.html", error = message)

    return render_template("register.html", error = message)

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

@app.route('/category', methods=['GET', 'POST'])
def category():
    session['show'] = True
    if request.method == 'GET':
        return render_template("add_category.html")
    else:        
        response = Category.addCategory(request.form['title'])
        if response['status']:
            session['categories'] = response['categories']
            return redirect(url_for('category'))
        else:
            return render_template("add_category.html", error = response['message'])

        
@app.route('/delete_category/<int:id>')
def deleteCategory(id):
    resp = Category.deleteCategory(id)
    message = None

    if resp['status']:
        session['categories'] = resp['categories']
        return redirect(url_for('category'))
    else:
        message = "Item not found"
        return render_template("add_category.html", error = message)
    

