from app import db

class Breakfast(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    rating = db.Column(db.Float)
    prep_time = db.Column(db.Integer)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), default=None)
    menu = db.relationship('Menu', back_populates='breakfast_items')
    ingredients = db.relationship('Ingredient', secondary='breakfast_ingredient', back_populates='breakfast_items')

    def to_dict(self):
        breakfast_dict = {
            "id": self.id,
            "name": self.name,
            "rating": self.rating,
            "prep_time": self.prep_time
        }
        if self.menu:
            breakfast_dict["menu_id"] = self.menu_id
            # breakfast_dict["restaurant"] = self.menu.restaurant

        if self.ingredients:
            breakfast_dict["ingredients"] = self.get_all_ingredients()

        return breakfast_dict

    def get_all_ingredients(self):
        return [ingredient.to_dict() for ingredient in self.ingredients]

    @classmethod
    def from_dict(cls, breakfast_dict):
        return cls(
            name=breakfast_dict["name"],
            rating=breakfast_dict["rating"],
            prep_time=breakfast_dict["prep_time"],
            menu_id=breakfast_dict.get("menu_id")
        )