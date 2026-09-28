from flask import Flask, jsonify, request

import os
from dotenv import load_dotenv
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

@app.route("/db-test")
def db_test():
    connection = get_db_connection()

    if connection.is_connected():
        connection.close()
        return jsonify({
            "status": "success",
            "message": "MySQL connection successful"
        })

@app.route("/")
def home():
    return jsonify({
        "message": "Python E-Commerce API is running"
    })

@app.route("/health")
def health():
    try:
        connection = get_db_connection()

        if connection.is_connected():
            connection.close()

            return jsonify({
                "status": "healthy",
                "database": "connected"
            }), 200

    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected"
        }), 503

@app.route("/products")
def products():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(products)

@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    name = data["name"]
    price = data["price"]

    connection = get_db_connection()
    cursor = connection.cursor()

    query = "INSERT INTO products (name, price) VALUES (%s, %s)"
    cursor.execute(query, (name, price))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Product added successfully"
    }), 201

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()

    name = data["name"]
    price = data["price"]

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        UPDATE products
        SET name = %s, price = %s
        WHERE id = %s
    """

    cursor.execute(query, (name, price, product_id))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Product updated successfully"
    })

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "DELETE FROM products WHERE id = %s"
    cursor.execute(query, (product_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Product deleted successfully"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
