import database
# All Database functionality relating to our fridge

# -- Create
# -- Read
# -- Update
# -- Delete

# INSERT ingredients INTO DB


def insert_ingredient(user_id, name, purchased_date, expiry_date):
    database.sql_write("INSERT into ingredients  (user_id, name, purchased_date, expiry_date) VALUES (%s, %s, %s, %s);", [
        user_id,
        name,
        purchased_date,
        expiry_date
    ])

# SELECT ingredient FROM DB to display and edit the ingredient


def get_ingredient(id):
    results = database.sql_select(
        'SELECT id, name, purchased_date, expiry_date FROM ingredients WHERE id = %s', [id])
    result = results[0]
    return result

# SELECT ALL INGREDIENTS FROM DB


def get_all_ingredients():
    results = database.sql_select(
        "SELECT * FROM ingredients", [])
    return results

# UPDATE INGREDIENTS IN DB


def update_ingredients(id, name, purchased_date, expiry_date):
    database.sql_write("UPDATE ingredients set name = %s, purchased_date = %s, expiry_date = %s WHERE id = %s", [
        name,
        purchased_date,
        expiry_date,
        id,
    ])
