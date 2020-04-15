from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'NOTSTEAL'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qtkcvpmkvldwfy:7b437f1ac7cb1468ce4273af05b9a2ce8276d3b82a584eab157e6e51b4aa9e1a@ec2-3-91-112-166.compute-1.amazonaws.com:5432/d8ufsgg72h6v8h"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from .auth import auth as auth_blueprint 
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint 
    app.register_blueprint(main_blueprint)
    
  
    with app.app_context():
        db.create_all()
        return app


