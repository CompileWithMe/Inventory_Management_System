from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = 'database.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home - View all products
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Add product
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO products (name, category, quantity, price) VALUES (?, ?, ?, ?)",
                  (name, category, quantity, price))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_product.html')

# Edit product
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']
        c.execute("UPDATE products SET name=?, category=?, quantity=?, price=? WHERE id=?",
                  (name, category, quantity, price, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    c.execute("SELECT * FROM products WHERE id=?", (id,))
    product = c.fetchone()
    conn.close()
    return render_template('edit_product.html', product=product)

# Delete product
@app.route('/delete/<int:id>')
def delete_product(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)