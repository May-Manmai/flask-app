from flask import Blueprint, request, session, redirect, render_template


fridge_controller = Blueprint(
    "fridge_controller", __name__, template_folder="../templates/fridge")


@fridge_controller.route('/fridge')
def index():
    return render_template('index.html')
