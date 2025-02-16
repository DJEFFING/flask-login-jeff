from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()





def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    # login_manager.login_view = 'login'  # Redirige vers la page de login si non connecté
    bcrypt.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
         return User.query.get(int(user_id))
        
    from .routes import main
    from .auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
