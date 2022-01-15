from flask import Flask, redirect, session
# need to import other controllers
from controllers.fridge_controller import fridge_controller
from controllers.user_controller import user_controller
from controllers.session_controller import session_controller
import os
import psycopg2


SECRET_KEY = os.environ.get("SECRET_KEY", "password")
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    if "user_id" in session:
        return redirect("/fridge")
    else:
        return redirect("/login")


app.register_blueprint(fridge_controller)
app.register_blueprint(session_controller)
app.register_blueprint(user_controller)

if __name__ == "__main__":
    app.run(debug=True)
