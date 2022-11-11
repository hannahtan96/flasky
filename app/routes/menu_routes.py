from app import db
from flask import abort, Blueprint, jsonify, make_response, request
from app.models.breakfast import Breakfast
from app.models.menu import Menu
from app.routes.breakfast_routes import get_model_from_id

menu_bp = Blueprint("menu", __name__, url_prefix="/menu")

@menu_bp.route("", methods=["GET"])
def get_all_menus():
    menus = Menu.query.all()
    
    result = [menu.to_dict() for menu in menus]
    return jsonify(result), 200


@menu_bp.route("", methods=["POST"])
def create_a_menu():
    request_body = request.get_json()
    new_menu = Menu(
        restaurant=request_body.get("restaurant_name"),
        meal=request_body.get("meal")
    )

    return jsonify({"msg": f"Successfully created menu for {new_menu.restaurant}"}), 200


@menu_bp.route("/<menu_id>/breakfasts", methods=["GET"])
def get_breakfasts_for_menu(menu_id):
    chosen_menu = get_model_from_id(Menu, menu_id)
    breakfasts = chosen_menu.get_breakfast_list()
    return jsonify(breakfasts), 200


@menu_bp.route("/<menu_id>", methods=["DELETE"])
def delete_menu(menu_id):
    menu = get_model_from_id(Menu, menu_id)

    for breakfast in menu.breakfast_items:
        breakfast.menu = None
    
    db.session.delete(menu)
    db.session.commit()

    return jsonify({"msg": f"Menu for restaurant {menu.restaurant} was successfully deleted"}), 200