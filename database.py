import sqlite3


connection = sqlite3.connect('base.db')
sql = connection.cursor()


def add_products_to_db(name, id, price, description, photo, notes):

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()
    sql.execute("INSERT INTO products VALUES(?, ?, ?, ?, ?, ?);", (name, id, price, description, photo, notes))
    connection.commit()


def get_users():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()
    users = sql.execute('SELECT name, id, gender FROM users;')

    return users.fetchall()


def delete_user():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()
    sql.execute('DELETE FROM users;')

    connection.commit()


def get_products_from_db(current_product):

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()
    products = sql.execute('SELECT * FROM products WHERE name=?;', (current_product, ))
    return products.fetchall()

# def get_users_from_database():
#
#     connection = sqlite3.connect('base.db')
#     sql = connection.cursor()
#
#     sql.execute('SELECT id FROM users')
#     users = sql.fetchall()
#
#     return [user[0] for user in users]


def get_product_id_from_db():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()
    product_id = sql.execute('SELECT id FROM products;')
    return product_id.fetchall()


def check_user(user_id):

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT id FROM users WHERE id=?;', (user_id,))

    if checker.fetchone():
        return True
    else:
        return False


def add_pr_to_cart(user_id, product_name, price_pr, product_count):

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    phone_number = sql.execute('select phone_number from users where id=?;', (user_id,))
    user_number = phone_number.fetchone()[0]

    sql.execute('INSERT INTO cart VALUES (?,?,?,?,?);', (user_id, product_name, user_number, price_pr*product_count, product_count))

    connection.commit()


def add_pr_to_cart2(user_id, product_name, price_pr, product_count):

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    phone_number = sql.execute('select phone_number from users where id=?;', (user_id,))
    user_number = phone_number.fetchone()[0]

    sql.execute('INSERT INTO cart2 VALUES (?,?,?,?,?);', (user_id, product_name, user_number, price_pr*product_count, product_count))

    connection.commit()


def get_all_info_product(current_product):

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    all_products = sql.execute('SELECT * FROM products WHERE name=?;', (current_product, ))

    return all_products.fetchone()


def get_user_cart(user_id):

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()
    all_products_from_cart = sql.execute('SELECT * FROM cart WHERE user_id=?;',
                                         (user_id,))
    return all_products_from_cart.fetchall()


def delete_from_cart(user_id):

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id,))

    connection.commit()


def add_user(user_id, name, phone_number, latitude, longitude, gender):

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO users VALUES (?,?,?,?,?,?);', (user_id, name, phone_number, latitude, longitude, gender))

    connection.commit()

    return add_user


def get_name_product(category_id):

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM products WHERE id=?;', (category_id,))
    return product_id.fetchall()


def auto_skoda_product():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM main.products WHERE id=15;')
    return product_id.fetchall()


def motor_skoda_product():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM products WHERE id=16;')
    return product_id.fetchall()


def accessories_product():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM products WHERE products.id=22;')
    return product_id.fetchall()


def chemical_product():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM products WHERE products.id=33;')
    return product_id.fetchall()


def filter_product():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM products WHERE products.id=44;')
    return product_id.fetchall()


def other_product():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM products WHERE products.id=55;')
    return product_id.fetchall()


def search_product(name):

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    sql.execute("SELECT * FROM products WHERE products.name LIKE ?", ('%' + name + '%',))
    rows = sql.fetchall()

    return rows


def auto_vw_product():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM main.vw WHERE id=11;')
    return product_id.fetchall()


def motor_vw_product():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM main.vw WHERE id=22;')
    return product_id.fetchall()


def vw_accessories_product():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM main.vw WHERE id=33;')
    return product_id.fetchall()


def vw_chemical_product():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM main.vw WHERE id=44;')
    return product_id.fetchall()


def vw_filter_product():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM main.vw WHERE id=55;')
    return product_id.fetchall()


def vw_other_product():

    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM main.vw WHERE id=66;')
    return product_id.fetchall()


def change_name(user_id, name):
    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    sql.execute('UPDATE users SET name=? WHERE id=?;', (name['name'], user_id))
    connection.commit()

def change_number(user_id, phone_number):
    connection = sqlite3.connect('base.db')
    sql = connection.cursor()

    sql.execute('UPDATE users SET phone_number=? WHERE id=?;', (phone_number['phone_number'], user_id))
    connection.commit()




# Запрос на создание таблицы

# sql.execute('CREATE TABLE users (id INTEGER, name INTEGER, phone_number TEXT, loc_lat REAL, loc_long REAL, gender TEXT);')
# sql.execute('CREATE TABLE vw (name INTEGER, id INTEGER, price INTEGER, description TEXT, picture TEXT, notes TEXT);')
# sql.execute('CREATE TABLE cart (user_id INTEGER, product_name TEXT, user_number TEXT, product_price INTEGER, product_count INTEGER);')

