from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Hannah'}
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('Registration requested for user {}, remember_me={}'.format(form.username.data, form.year.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('register.html', title='Sign Up', form=form)