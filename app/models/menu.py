from app import db

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant = db.Column(db.String)
    meal = db.Column(db.String)
    breakfast_items = db.relationship('Breakfast', back_populates='menu')

    def to_dict(self):
        return {
            "id": self.id,
            "restaurant_name": self.restaurant,
            "meal": self.meal,
            "breakfast_items": self.get_breakfast_list()
        }

    def get_breakfast_list(self):
        list_of_breakfast = []
        for item in self.breakfast_items:
            list_of_breakfast.append(item.to_dict())
        return list_of_breakfast

