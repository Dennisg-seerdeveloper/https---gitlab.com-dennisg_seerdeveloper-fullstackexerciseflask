from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import session
from flask import request
from flask import flash
from flask import url_for
from flask import g
from functools import wraps

mod = Blueprint('default', __name__)

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        else:
            return func(*args, **kwargs)
    return wrapper 

@mod.route('/')
def index():
    if 'username' not in session:
        return redirect('/login')
    return redirect('/posts')

@mod.route('/login', methods=['GET'])
def login_page():
    if 'username' in session:
        return redirect('/posts')
    return render_template('default/login.html')

@mod.route('/login', methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']
    if g.usersdb.getUserWithPassword(username, password).count() > 0:
        session['username'] = username
        return redirect('/')
    else:
        flash('Invalid username and password.', 'signin_failure')
        return redirect('/login') 

@mod.route('/logout', methods=['GET'])
def logout_submit():
    session.pop('username', None)
    session.clear()
    return redirect('/')

@mod.route('/signup', methods=['GET'])
def signup_page():
    if 'username' in session:
        return redirect('/posts')
    return render_template('default/signup.html')

@mod.route('/signup', methods=['POST'])
def signup_submit():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if password != confirm_password:
        flash('Password did not match.', 'signup_failure')
        return redirect(url_for('.signup_page'))
    elif g.usersdb.getUser(username).count() > 0:
        flash('Username already exists.', 'signup_failure')
        return redirect(url_for('.signup_page'))
    session['username'] = username
    g.usersdb.createUser(username, password)
    return redirect('/posts')