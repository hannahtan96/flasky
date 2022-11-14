from app import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String,)
    breakfast_items = db.relationship('Breakfast', secondary='breakfast_ingredient', back_populates='ingredients')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "breakfast_items": self.get_all_breakfast_items()
        }

    def get_all_breakfast_items(self):
        return [item.to_dict() for item in self.breakfast_items]

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"]
        )