from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Initialize the database
db = SQLAlchemy()

# Initialize login manager
login_manager = LoginManager()

# Initialize CSRF protection
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a random secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize components with the app
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Configure Login Manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # User loader callback
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Import here to avoid circular dependencies
        return User.query.get(int(user_id))

    # Register Blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
