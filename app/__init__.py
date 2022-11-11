from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# setting up initial objects for us to use later in app
db = SQLAlchemy()
migrate = Migrate() 
load_dotenv() # load in the variables from .env file


def create_app(test_config=None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQUALCHEMY_ECHO'] = True # pytest doesn't run when this is True
    if not test_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
    
    # connecting app to classes, which manage sqlalchemy and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.breakfast import Breakfast
    from app.models.menu import Menu

    from .routes.breakfast_routes import breakfast_bp # register the breakfast blueprint / endpoint
    app.register_blueprint(breakfast_bp)

    from .routes.menu_routes import menu_bp
    app.register_blueprint(menu_bp)

    return app