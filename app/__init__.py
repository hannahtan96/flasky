from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# setting up initial objects for us to use later in app
db = SQLAlchemy()
migrate = Migrate() 

def create_app():
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/breakfasts_development'
    app.config['SQUALCHEMY_ECHO'] = True
    
    # connecting app to classes, which manage sqlalchemy and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.breakfast import Breakfast

    from .routes.breakfast import breakfast_bp # register the breakfast blueprint / endpoint
    app.register_blueprint(breakfast_bp)

    return app