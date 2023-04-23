from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RequestForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = {'username': 'Hannah'}
    form = RequestForm()
    if form.validate_on_submit():
        flash('Query requested: {}'.format(form.query.data))
        return redirect(url_for('index'))
    return render_template('index.html', user=current_user, title='Ask a Question', form=form,)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, year=form.year.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))