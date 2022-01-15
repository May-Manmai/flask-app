import database
import bcrypt


def insert_user(name, email, password):
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    database.sql_write("INSERT INTO users (name, email, password)" +
                       " VALUES(%s, %s, %s)", [name, email, password])


def get_user_by_id(id):
    results = database.sql_select(
        'SELECT * FROM users WHERE id = %s;', [id])
    results = results[0]
    return results


def get_user_by_email(email):
    results = database.sql_select(
        "SELECT * FROM users WHERE email = %s", [email])
    if len(results) > 0:
        return results[0]
    else:
        return None
