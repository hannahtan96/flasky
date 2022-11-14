from app import db

class BreakfastIngredient(db.Model):
    __tablename__ = 'breakfast_ingredient'
    breakfast_id = db.Column(db.Integer, ForeignKey='breakfast.id', primary_key=True, nullable=False)
    ingredient_id = db.Column(db.Integer, ForeignKey='ingredient.id', primary_key=True, nullable=False)