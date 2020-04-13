from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from flask_socketio import SocketIO


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    #login_manager.remember_cookie_durarion = delta
    #login_manager.remember_cookie_refresh_each_request = True

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for socket.io of app
    from .events import events as events_blueprint
    app.register_blueprint(events_blueprint)

    # blueprint for gaming app
    from .gaming import gaming as gaming_blueprint
    app.register_blueprint(gaming_blueprint)

    #starting socket.io
    socketio.init_app(app)

    return app