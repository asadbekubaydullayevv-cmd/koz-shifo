from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    CORS(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    
    from app.routes import main
    app.register_blueprint(main)
    
    with app.app_context():
        db.create_all()
        _create_default_users()
    
    return app

def _create_default_users():
    from app.models import Foydalanuvchi
    from werkzeug.security import generate_password_hash
    if not Foydalanuvchi.query.first():
        users = [
            Foydalanuvchi(username='direktor', parol=generate_password_hash('direktor123'), rol='direktor'),
            Foydalanuvchi(username='kassa', parol=generate_password_hash('kassa123'), rol='kassa'),
        ]
        db.session.add_all(users)
        db.session.commit()
        print("Default foydalanuvchilar yaratildi")
