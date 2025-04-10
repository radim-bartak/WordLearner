from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    try:
        config = Config("config.json")
    except Exception as e:
        app.logger.error(f"Configuration error: {e}")
        raise

    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["DEBUG"] = config.DEBUG

    db.init_app(app)

    from .models import User 

    with app.app_context():
        db.create_all()

    from .auth_routes import auth_bp
    from .main_routes import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
