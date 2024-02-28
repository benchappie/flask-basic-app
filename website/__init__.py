from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

#this is the function that is being called in main.py
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'apples'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #calls logic from view.py
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #calls data objects from models.py
    from .models import User, Note, Exercise

    #creates database
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app) 

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app



     