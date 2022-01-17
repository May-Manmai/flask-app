from flask import Blueprint, request, session, redirect, render_template
from models.fridge import get_all_ingredients, get_ingredient, insert_ingredient, update_ingredients

fridge_controller = Blueprint(
    "fridge_controller", __name__, template_folder="../templates/fridge")


@fridge_controller.route('/fridge')
def fridge():
    fridge_items = get_all_ingredients()

    return render_template('index.html', fridge_items=fridge_items)


@fridge_controller.route('/fridge/create', methods=["GET"])
def create():
    return render_template('create.html')


@fridge_controller.route('/fridge', methods=["POST"])
def insert():
    # INSERT INTO DB
    insert_ingredient(
        session.get("user_id"),
        request.form.get("name"),
        request.form.get("purchased_date"),
        request.form.get("expiry_date"),
    )

    return redirect('/')


@fridge_controller.route('/fridge/<id>', methods=["POST"])
def update(id):
    update_ingredients(
        id,
        request.form.get("name"),
        request.form.get("purchased_date"),
        request.form.get("expiry_date"),

    )

    return redirect('/')


@fridge_controller.route('/fridge/<id>/edit', methods=["GET"])
def edit(id):
    ingredient = get_ingredient(id)
    return render_template('edit.html', ingredient=ingredient)
