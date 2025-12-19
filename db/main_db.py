import sqlite3
from db import queries
from config import path_db

def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_PRODUCTS)
    print("База данных подключена!")
    conn.commit()
    conn.close()


def add_product(product):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_PRODUCTS, (product, ))
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    return product_id


def get_product(filter_type):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if filter_type == 'purchased':
        cursor.execute(queries.SELECT_PRODUCTS_PURCHASED)
    elif filter_type == 'nonpurchased':
        cursor.execute(queries.SELECT_PRODUCTS_NONPURCHASED)
    elif filter_type == 'all':
        cursor.execute(queries.SELECT_PRODUCTS)

    conn.commit()
    products = cursor.fetchall()
    conn.close()
    return products


def update_product(product_id, new_product=None, purchased=None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if new_product is not None:
        cursor.execute(queries.UPDATE_PRODUCTS, (new_product, product_id))
    
    if purchased is not None:
        cursor.execute("UPDATE products SET purchased = ? WHERE id = ?", (purchased, product_id))
    
    conn.commit()
    conn.close()


def delete_product(product_id=None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    
    if product_id:
        cursor.execute(queries.DELETE_PRODUCTS, (product_id, ))
    else:
        cursor.execute(queries.DELETE_PRODUCTS_PURCHASED)

    conn.commit()
    conn.close()
    