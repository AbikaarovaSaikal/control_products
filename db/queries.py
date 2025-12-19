CREATE_PRODUCTS = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT NOT NULL,
        purchased INTEGER DEFAULT 0
    )
"""

INSERT_PRODUCTS = "INSERT INTO products (product) VALUES (?)"

SELECT_PRODUCTS = 'SELECT id, product, purchased FROM products'

SELECT_PRODUCTS_PURCHASED = 'SELECT id, product, purchased FROM products WHERE purchased = 1'
SELECT_PRODUCTS_NONPURCHASED = 'SELECT id, product, purchased FROM products WHERE purchased = 0'

UPDATE_PRODUCTS = 'UPDATE products SET product = ? WHERE id = ?'

DELETE_PRODUCTS = "DELETE FROM products WHERE id = ?"

DELETE_PRODUCTS_PURCHASED = "DELETE FROM products WHERE purchased = 1"