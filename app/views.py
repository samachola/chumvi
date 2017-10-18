from flask import render_template, redirect, url_for, request, session, flash
from app import app

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] :
            session['logged_in'] = True
            flash('Logged in successfully')
            return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")