from flask import Blueprint, request, redirect, render_template
from models.user import get_user_by_email, insert_user

user_controller = Blueprint(
    "user_controller", __name__, template_folder="../templates/users")


@user_controller.route('/signup')
def signup():
    error = request.args.get('error', None)
    return render_template('signup.html', error=error)


@user_controller.route('/users', methods=["POST"])
def create_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    user = get_user_by_email(email)
    if user:
        return redirect('/signup?error=username+already+exist')

    insert_user(name, email, password)

    return redirect('/')
