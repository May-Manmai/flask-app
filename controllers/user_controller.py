from flask import Blueprint, request, redirect, render_template
from models.user import insert_user

user_controller = Blueprint(
    "user_controller", __name__, template_folder="../templates/users")


@user_controller.route('/signup')
def signup():
    return render_template('signup.html')


@user_controller.route('/users', methods=["POST"])
def create_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    insert_user(name, email, password)

    return redirect('/')
