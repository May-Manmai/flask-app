from crypt import methods
from flask import Blueprint, request, session, redirect, render_template
from models.fridge import get_all_ingredients, get_ingredient, insert_ingredient, update_ingredients, delete_ingredients, get_expired_ingredients, get_not_expired_ingredients
import os
import requests

SPOONACULAR_KEY = os.environ.get("SPOONACULAR_KEY", "")

fridge_controller = Blueprint(
    "fridge_controller", __name__, template_folder="../templates/fridge")


@fridge_controller.route('/fridge')
def fridge():
    user_id = session.get("user_id")
    fridge_items = get_not_expired_ingredients(user_id)
    bin_items = get_expired_ingredients(user_id)

    return render_template('index.html', fridge_items=fridge_items, bin_items=bin_items)


@fridge_controller.route('/fridge/create', methods=["GET"])
def create():
    return render_template('create.html')


@fridge_controller.route('/fridge', methods=["POST"])
def insert():
    ingredient_name = request.form.get('name')
    url = f'https://api.spoonacular.com/food/ingredients/search?query={ingredient_name}&apiKey={SPOONACULAR_KEY}'
    print(url)
    image_response = requests.get(url)
    image_info = image_response.json()
    if image_info["results"] == []:
        spoonacular_url = f'https://spoonacular.com/cdn/ingredients_50x50/null.jpg'
    else:
        spoonacular_url = f'https://spoonacular.com/cdn/ingredients_100x100/{image_info["results"][0]["image"]}'
    print(image_info)
    # INSERT INTO DB
    insert_ingredient(
        session.get("user_id"),
        request.form.get("name"),
        request.form.get("purchased_date"),
        request.form.get("expiry_date"),
        spoonacular_url,
    )

    return redirect('/')


@fridge_controller.route('/fridge/<id>', methods=["POST"])
def update(id):
    ingredient_name = request.form.get('name')
    url = f'https://api.spoonacular.com/food/ingredients/search?query={ingredient_name}&apiKey={SPOONACULAR_KEY}'
    print(url)
    image_response = requests.get(url)
    image_info = image_response.json()
    if image_info["results"] == []:
        spoonacular_url = f'https://spoonacular.com/cdn/ingredients_50x50/null.jpg'
    else:
        spoonacular_url = f'https://spoonacular.com/cdn/ingredients_100x100/{image_info["results"][0]["image"]}'
    print(image_info["results"])
    update_ingredients(
        id,
        request.form.get("name"),
        request.form.get("purchased_date"),
        request.form.get("expiry_date"),
        spoonacular_url,

    )

    return redirect('/')


@fridge_controller.route('/fridge/<id>/edit', methods=["GET"])
def edit(id):
    ingredient = get_ingredient(id)
    return render_template('edit.html', ingredient=ingredient)


@fridge_controller.route('/fridge/<id>', methods=["GET"])
def show(id):
    ingredient = get_ingredient(id)
    return render_template('show.html', ingredient=ingredient)


@fridge_controller.route('/fridge/<id>/delete', methods=["POST"])
def delete(id):
    delete_ingredients(id)
    return redirect('/')
