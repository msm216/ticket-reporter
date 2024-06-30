from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config



db = SQLAlchemy()


def create_app():
    
    app = Flask(__name__)
    
    # Load configurations from config.py
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    with app.app_context():
        from . import models, views
    
    return app