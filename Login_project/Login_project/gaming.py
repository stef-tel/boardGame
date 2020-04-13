from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from .models import User

gaming = Blueprint('gaming', __name__)

@gaming.route('/play')
@login_required
def play():
    return render_template('game.html')