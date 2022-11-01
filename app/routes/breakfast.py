from app import db
from flask import abort, Blueprint, jsonify, make_response, request
from app.models.breakfast import Breakfast

# class Breakfast:
#     def __init__(self, id, name, rating, prep_time):
#         self.id = id
#         self.name = name
#         self.rating = rating
#         self.prep_time = prep_time

# all_breakfasts = [
#     Breakfast(1, "omelette", 4, 10),
#     Breakfast(2, "french toast", 3, 15),
#     Breakfast(3, "cereal", 1, 1),
#     Breakfast(4, "oatmeal", 3, 10)

breakfast_bp = Blueprint("breakfast", __name__, url_prefix="/breakfast") # /breakfast will be the first part of the url

def get_breakfast_from_id(breakfast_id):
    try:
        breakfast_id = int(breakfast_id)
    except ValueError:
        return abort(make_response({"msg": f"invalid data type: {type(breakfast_id)}"}, 400)) # abort requires a make_response
    
    chosen_breakfast = Breakfast.query.get(breakfast_id) # equivalent to SELECT * FROM breakfast WHERE id=breakfast_id;
    if chosen_breakfast is None:
        return abort(make_response({"msg": f"Could not find breakfast item with id: {breakfast_id}"}, 404))

    return chosen_breakfast

@breakfast_bp.route('', methods=['GET'])
def get_all_breakfast():
    result = []
    all_breakfasts = Breakfast.query.all() # SELECT * FROM breakfast;

    for item in all_breakfasts:
        result.append(item.to_dict())

    return jsonify(result), 200


@breakfast_bp.route('/<breakfast_id>', methods=['GET'])
def get_one_breakfast(breakfast_id):
    chosen_breakfast = get_breakfast_from_id(breakfast_id)
    return jsonify(chosen_breakfast.to_dict()), 200


@breakfast_bp.route("", methods=["POST"])
def create_one_breakfast():
    request_body = request.get_json()
    new_breakfast = Breakfast(
        # id=request_body["id"], # do not pass in b/c id is autoincremented
        name=request_body["name"],
        rating=request_body["rating"],
        prep_time=request_body["prep_time"]
        )

    db.session.add(new_breakfast)
    db.session.commit()

    return jsonify({"msg": f"Breakfast {new_breakfast.name} successfully created"}), 201


@breakfast_bp.route("/<breakfast_id>", methods=["PUT"]) # require all fields to pass into json
def update_one_breakfast(breakfast_id):
    chosen_breakfast = get_breakfast_from_id(breakfast_id)
    
    request_body = request.get_json()
    try:
        chosen_breakfast.name = request_body["name"]
        chosen_breakfast.rating = request_body["rating"]
        chosen_breakfast.prep_time = request_body["prep_time"]
    except KeyError:
        return jsonify({"msg": "missing needed data"}), 400

    db.session.commit()

    return jsonify({"msg": f"Breakfast {chosen_breakfast.name} successfully updated"}), 200


@breakfast_bp.route("/<breakfast_id>", methods=["PATCH"])
def update_one_breakfast_with_partial_data(breakfast_id):
    chosen_breakfast = get_breakfast_from_id(breakfast_id)

    request_body = request.get_json()
    print(request_body)
    for data in request_body:
        if data == "name":
            chosen_breakfast.name = request_body['name']
        elif data == "rating":
            chosen_breakfast.rating = request_body['rating']
        elif data == "prep_time":
            chosen_breakfast.prep_time = request_body['prep_time']

    db.session.commit()

    return jsonify({"msg": f"Breakfast {chosen_breakfast.name} successfully updated"}), 200


@breakfast_bp.route("/<breakfast_id>", methods=["DELETE"])
def delete_one_breakfast(breakfast_id):
    chosen_breakfast = get_breakfast_from_id(breakfast_id)

    db.session.delete(chosen_breakfast)
    db.session.commit()

    return jsonify({"msg": f"Breakfast {chosen_breakfast.name} successfully deleted"}), 200