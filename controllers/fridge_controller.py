from crypt import methods
from unittest import result
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

    # get image from selected ingredients
    checked_items = request.args.getlist("selected_ingredients")
    if not checked_items:
        return render_template('index.html', fridge_items=fridge_items, bin_items=bin_items)

    listToStr = ','.join([str(elem) for elem in checked_items])
    url = f'https://api.spoonacular.com/recipes/complexSearch?query={listToStr}&number=3&apiKey={SPOONACULAR_KEY}'
    source_response = requests.get(url)
    source_info = source_response.json()
    recipe_name1 = source_info["results"][0]["title"]
    recipe_image_url1 = source_info["results"][0]["image"]
    recipe_name2 = source_info["results"][1]["title"]
    recipe_image_url2 = source_info["results"][1]["image"]
    recipe_name3 = source_info["results"][2]["title"]
    recipe_image_url3 = source_info["results"][2]["image"]
    #
    source_id = source_info["results"][0]["id"]
    url = f'https://api.spoonacular.com/recipes/{source_id}/information?apiKey={SPOONACULAR_KEY}'
    recipe_response = requests.get(url)
    recipe_info = recipe_response.json()

    return render_template('index.html', fridge_items=fridge_items, bin_items=bin_items, url=url, recipe_name1=recipe_name1, recipe_name2=recipe_name2, recipe_name3=recipe_name3, recipe_image_url2=recipe_image_url2, recipe_image_url3=recipe_image_url3, recipe_image_url1=recipe_image_url1, recipe_info=recipe_info)


@fridge_controller.route('/fridge/create', methods=["GET"])
def create():
    return render_template('create.html')


@fridge_controller.route('/fridge', methods=["POST"])
def insert():
    ingredient_name = request.form.get('name')
    url = f'https://api.spoonacular.com/food/ingredients/search?query={ingredient_name}&apiKey={SPOONACULAR_KEY}'

    image_response = requests.get(url)
    image_info = image_response.json()
    if image_info["results"] == []:
        spoonacular_url = f'https://spoonacular.com/cdn/ingredients_50x50/null.jpg'
    else:
        spoonacular_url = f'https://spoonacular.com/cdn/ingredients_100x100/{image_info["results"][0]["image"]}'

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

    image_response = requests.get(url)
    image_info = image_response.json()
    if image_info["results"] == []:
        spoonacular_url = f'https://spoonacular.com/cdn/ingredients_50x50/null.jpg'
    else:
        spoonacular_url = f'https://spoonacular.com/cdn/ingredients_100x100/{image_info["results"][0]["image"]}'
    # print(image_info["results"])
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
