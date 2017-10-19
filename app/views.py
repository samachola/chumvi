from flask import render_template, redirect, url_for, request, session, flash
from app import app

@app.route('/')
def index():
    session['show'] = True
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    session['show'] = False
    if request.method == 'POST':
        if request.form['username'] :
            session['logged_in'] = True
            flash('Logged in successfully')
            return redirect(url_for('index'))
    else:
        session['logged_in'] = True
        
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    session['show'] = False
    error = None
    if request.method == 'POST':        
        if not request.form['fname'] or not request.form['lname'] or not request.form['email'] or not request.form['password']:
            error = "All input fields are required"
        else:
            return redirect(url_for('login'))

    return render_template("register.html", error = error)