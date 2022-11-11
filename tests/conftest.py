import pytest
from app import create_app, db # refers to the create_app in the __init__.py in the broader app folder
from flask.signals import request_finished # decorator to run code after something happens
from app.models.breakfast import Breakfast

@pytest.fixture
def app():
    app = create_app({"TESTING": True}) # Flask convention to pass a dictionary with TESTING = True

    @request_finished.connect_via(app) # checks if request is finished, so removes session. makes sure all data is most up to date
    def expire_session(sender, response, **extra): # **extra refers to any extra variables with unknown quantity
        db.session.remove()

    with app.app_context():
        db.create_all() # creating a test table with model that we specify
        yield app # request is made 
    
    with app.app_context():
        db.drop_all() # after the request is finished, all databases are dropped


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def three_breakfasts(app):
    cereal = Breakfast(name="cereal", rating=5, prep_time=1)
    oatmeal = Breakfast(name="oatmeal", rating=2, prep_time=5)
    french_toast = Breakfast(name="french toast", rating=4, prep_time=20)

    db.session.add_all([cereal, oatmeal, french_toast])
    db.session.commit()
