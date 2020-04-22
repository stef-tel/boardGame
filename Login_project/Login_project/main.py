from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from flask_table import Table, Col
from . import db
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/users')
@login_required
def users():
    userList = User.query.all()

    # Declare your table
    class ItemTable(Table):
        classes = ['table','is-bordered','is-striped','is-narrow','is-hoverable','is-fullwidth']
        id = Col('DB id')
        email = Col('email')
        name = Col('name')
        is_active = Col('status')
        is_authenticated = Col('status 2')

    table = ItemTable(userList)
    return render_template('users.html', userTable=table, room='general_room', name=current_user.name)
    