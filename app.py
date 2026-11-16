
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "change-this-to-a-long-random-secret"


# ==========================================
# MYSQL DATABASE CONNECTION
# ==========================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sujal3319",
        database="stock_management"
    )


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT COUNT(*) AS total_products
            FROM Products
        """)
        total_products = cursor.fetchone()["total_products"]

        cursor.execute("""
            SELECT COALESCE(SUM(quantity), 0) AS total_stock
            FROM Products
        """)
        total_stock = cursor.fetchone()["total_stock"]

        cursor.execute("""
            SELECT COUNT(*) AS total_categories
            FROM Categories
        """)
        total_categories = cursor.fetchone()["total_categories"]

        cursor.execute("""
            SELECT COUNT(*) AS total_suppliers
            FROM Suppliers
        """)
        total_suppliers = cursor.fetchone()["total_suppliers"]

        cursor.execute("""
            SELECT COALESCE(SUM(price * quantity), 0) AS stock_value
            FROM Products
        """)
        stock_value = cursor.fetchone()["stock_value"]

        cursor.execute("""
            SELECT product_id, product_name, quantity
            FROM Products
            WHERE quantity <= 5
            ORDER BY quantity ASC
        """)
        low_stock = cursor.fetchall()

        cursor.execute("""
            SELECT
                p.product_id,
                p.product_name,
                p.price,
                p.quantity,
                c.category_name
            FROM Products p
            LEFT JOIN Categories c
                ON p.category_id = c.category_id
            ORDER BY p.product_id DESC
            LIMIT 5
        """)
        recent_products = cursor.fetchall()

        cursor.execute("""
            SELECT
                c.category_name,
                COALESCE(SUM(p.quantity), 0) AS total_quantity
            FROM Categories c
            LEFT JOIN Products p
                ON c.category_id = p.category_id
            GROUP BY c.category_id, c.category_name
            ORDER BY c.category_name
        """)
        category_data = cursor.fetchall()

        return render_template(
            "index.html",
            total_products=total_products,
            total_stock=total_stock,
            total_categories=total_categories,
            total_suppliers=total_suppliers,
            stock_value=stock_value,
            low_stock=low_stock,
            recent_products=recent_products,
            category_data=category_data
        )

    finally:
        cursor.close()
        conn.close()


# ==========================================
# PRODUCTS - VIEW AND ADD
# ==========================================

@app.route("/products", methods=["GET", "POST"])
def products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if request.method == "POST":
            product_name = request.form.get("product_name", "").strip()
            category_id = request.form.get("category_id")
            supplier_id = request.form.get("supplier_id")
            price = request.form.get("price")
            quantity = request.form.get("quantity")

            try:
                if not product_name:
                    raise ValueError("Product name is required.")

                category_id = int(category_id)
                supplier_id = int(supplier_id)
                price = float(price)
                quantity = int(quantity)

                if price <= 0 or quantity < 0:
                    raise ValueError("Enter a positive price and non-negative quantity.")

                cursor.execute("""
                    INSERT INTO Products
                    (product_name, category_id, supplier_id, price, quantity)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    product_name,
                    category_id,
                    supplier_id,
                    price,
                    quantity
                ))

                conn.commit()
                flash("Product added successfully!", "success")

            except (ValueError, TypeError):
                conn.rollback()
                flash("Please enter valid product details.", "danger")

            return redirect(url_for("products"))

        cursor.execute("""
            SELECT
                p.product_id,
                p.product_name,
                p.category_id,
                p.supplier_id,
                p.price,
                p.quantity,
                c.category_name,
                s.supplier_name
            FROM Products p
            LEFT JOIN Categories c
                ON p.category_id = c.category_id
            LEFT JOIN Suppliers s
                ON p.supplier_id = s.supplier_id
            ORDER BY p.product_id DESC
        """)
        product_list = cursor.fetchall()

        cursor.execute("""
            SELECT category_id, category_name
            FROM Categories
            ORDER BY category_name
        """)
        categories = cursor.fetchall()

        cursor.execute("""
            SELECT supplier_id, supplier_name
            FROM Suppliers
            ORDER BY supplier_name
        """)
        suppliers = cursor.fetchall()

        return render_template(
            "products.html",
            products=product_list,
            categories=categories,
            suppliers=suppliers
        )

    finally:
        cursor.close()
        conn.close()


# ==========================================
# EDIT PRODUCT
# ==========================================

@app.route("/edit/<int:id>", methods=["POST"])
def edit_product(id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        product_name = request.form.get("product_name", "").strip()
        category_id = int(request.form.get("category_id"))
        supplier_id = int(request.form.get("supplier_id"))
        price = float(request.form.get("price"))
        quantity = int(request.form.get("quantity"))

        if not product_name or price <= 0 or quantity < 0:
            raise ValueError("Invalid product details.")

        cursor.execute("""
            UPDATE Products
            SET product_name = %s,
                category_id = %s,
                supplier_id = %s,
                price = %s,
                quantity = %s
            WHERE product_id = %s
        """, (
            product_name,
            category_id,
            supplier_id,
            price,
            quantity,
            id
        ))

        conn.commit()
        flash("Product updated successfully!", "success")

    except (ValueError, TypeError):
        conn.rollback()
        flash("Invalid product details. Please check your inputs.", "danger")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("products"))


# ==========================================
# DELETE PRODUCT
# ==========================================

@app.route("/delete/<int:id>", methods=["POST"])
def delete_product(id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM Products
            WHERE product_id = %s
        """, (id,))

        conn.commit()

        if cursor.rowcount:
            flash("Product deleted successfully!", "success")
        else:
            flash("Product not found.", "warning")

    except mysql.connector.Error:
        conn.rollback()
        flash("Unable to delete this product.", "danger")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("products"))


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)
