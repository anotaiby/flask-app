# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app = Flask(__name__, static_url_path="/static")
    UPLOAD_FOLDER = 'static/uploads/'
    DOWNLOAD_FOLDER = 'static/downloads/'
    ALLOWED_EXTENSIONS = {'jpg', 'png', '.jpeg'}
    # APP CONFIGURATIONS
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
    # limit upload size to 2mb
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

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

    return app
