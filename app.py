from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "stock123"

# MySQL Database Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mahi@9020",
        database="stock_management"
    )

# Dashboard
@app.route("/")
def index():
    con = get_connection()
    cur = con.cursor(dictionary=True)

    cur.execute("SELECT COUNT(*) AS total FROM Products")
    total = cur.fetchone()["total"]

    cur.execute("SELECT COALESCE(SUM(quantity),0) AS stock FROM Products")
    stock = cur.fetchone()["stock"]

    cur.close()
    con.close()

    return render_template(
        "index.html",
        total=total,
        stock=stock
    )

# Display and Add Products
@app.route("/products", methods=["GET", "POST"])
def products():
    con = get_connection()
    cur = con.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["product_name"]
        category = request.form["category_id"]
        supplier = request.form["supplier_id"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        cur.execute("""
            INSERT INTO Products
            (product_name, category_id, supplier_id, price, quantity)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, category, supplier, price, quantity))

        con.commit()
        cur.close()
        con.close()

        flash("Product added successfully!")
        return redirect(url_for("products"))

    cur.execute("""
        SELECT p.*, c.category_name, s.supplier_name
        FROM Products p
        INNER JOIN Categories c
        ON p.category_id = c.category_id
        INNER JOIN Suppliers s
        ON p.supplier_id = s.supplier_id
        ORDER BY p.product_id
    """)
    products = cur.fetchall()

    cur.execute("SELECT * FROM Categories")
    categories = cur.fetchall()

    cur.execute("SELECT * FROM Suppliers")
    suppliers = cur.fetchall()

    cur.close()
    con.close()

    return render_template(
        "products.html",
        products=products,
        categories=categories,
        suppliers=suppliers
    )

# Update Product
@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        UPDATE Products
        SET product_name=%s,
            category_id=%s,
            supplier_id=%s,
            price=%s,
            quantity=%s
        WHERE product_id=%s
    """, (
        request.form["product_name"],
        request.form["category_id"],
        request.form["supplier_id"],
        request.form["price"],
        request.form["quantity"],
        id
    ))

    con.commit()
    cur.close()
    con.close()

    flash("Product updated successfully!")
    return redirect(url_for("products"))

# Delete Product
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "DELETE FROM Products WHERE product_id=%s",
        (id,)
    )

    con.commit()
    cur.close()
    con.close()

    flash("Product deleted successfully!")
    return redirect(url_for("products"))


if __name__ == "__main__":
    app.run(debug=True)

