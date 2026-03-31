import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import pymongo
# SQLite is used instead of pymongo for local development without dependencies.

app = Flask(__name__)
app.secret_key = 'super_secret_cracker_key'

def get_image_for_product(name, category):
    safe_name = name.replace(' ', '_').replace('/', '_') + '.jpg'
    return f'/static/images/products/{safe_name}'

RAW_PRODUCTS = [
    ("Common Crackers", ["Atom Bomb", "Lakshmi Bomb", "Hydrogen Bomb", "Bullet Bomb", "Deluxe Bomb", "King Bomb", "Thunder Bomb", "Electric Bomb", "Classic Bomb", "Sound Bomb", "Red Bijili", "Green Bijili", "Electric Bijili", "Mini Bijili", "Super Bijili"]),
    ("Sparklers", ["7 cm Sparklers", "10 cm Sparklers", "12 cm Sparklers", "15 cm Sparklers", "30 cm Sparklers", "Colour Sparklers", "Gold Sparklers", "Electric Sparklers", "Twinkling Sparklers", "Super Deluxe Sparklers"]),
    ("Flower Pots", ["Small Flower Pot", "Big Flower Pot", "Deluxe Flower Pot", "Colour Flower Pot", "Giant Flower Pot", "Crackling Flower Pot", "Colour Changing Flower Pot", "Mega Flower Pot", "Electric Flower Pot", "Peacock Flower Pot"]),
    ("Ground Spinners", ["Ground Chakra", "Deluxe Chakra", "Colour Chakra", "Electric Chakra", "Mega Chakra", "Giant Wheel", "Super Deluxe Chakra", "Crackling Chakra"]),
    ("Rockets", ["Baby Rocket", "Whistling Rocket", "Colour Rocket", "Electric Rocket", "Moon Rocket", "Deluxe Rocket", "Crackling Rocket", "Multi Colour Rocket", "Sky Rocket", "Mega Rocket"]),
    ("Fancy Crackers", ["Peacock Dance", "Colour Smoke", "Disco Wheel", "Magic Pop", "Butterfly", "Colour Fountain", "Rainbow Fountain", "Disco Flash", "Electric Stone", "Mini Magic Show"]),
    ("Fancy Sky Shots", ["7 Shot", "10 Shot", "12 Shot", "15 Shot", "30 Shot", "60 Shot", "120 Shot", "Multi Colour Shot", "Crackling Shot", "Deluxe Shot"]),
    ("Kids Special Crackers", ["Snake Tablet", "Pencil Crackers", "Magic Pencil", "Party Popper", "Colour Matches", "Mini Rocket", "Ground Bloom Flower"]),
    ("Special Effects", ["Dragon Egg", "Colour Ball", "Silver Rain", "Golden Rain", "Crackling Balls", "Electric Stone Fountain", "Colour Smoke Bomb", "Thunder Wheel", "Rainbow Wheel", "Magic Fountain"]),
    ("Premium Fancy Crackers", ["Golden Peacock", "Colour King Fountain", "Super Deluxe Fountain", "Mega Crackling Fountain", "Rainbow Sky Shot", "Galaxy Shot", "Diamond Fountain", "Laser Show Crackers", "Royal Fountain", "Silver Star Shot", "Colour Meteor Shot", "Golden Galaxy Shot", "Fire Ring Wheel", "King of Sky Shot", "Mega Festival Shot"])
]

import pymysql

# ─── DATABASE SETUP ──────────────────────────────────────────────────────────

def get_db():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='tiger',
        database='crackers',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

def init_db():
    try:
        sys_conn = pymysql.connect(host='127.0.0.1', user='root', password='tiger')
        sys_c = sys_conn.cursor()
        sys_c.execute("CREATE DATABASE IF NOT EXISTS crackers")
        sys_conn.commit()
        sys_conn.close()

        conn = get_db()
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS products (
            ID INT PRIMARY KEY,
            Category VARCHAR(255),
            Name VARCHAR(255),
            Price FLOAT,
            Stock INT,
            Image VARCHAR(255)
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(255),
            Email VARCHAR(255),
            Password VARCHAR(255)
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS orders (
            `Order ID` VARCHAR(255) PRIMARY KEY,
            `Customer Name` VARCHAR(255),
            Phone VARCHAR(255),
            Address TEXT,
            `Delivery Date` VARCHAR(255),
            Items TEXT,
            `Total Amount` FLOAT,
            Date VARCHAR(255),
            Time VARCHAR(255),
            Status VARCHAR(255)
        )''')
        
        c.execute("SELECT COUNT(*) as count FROM products")
        result = c.fetchone()
        if result and result['count'] == 0:
            print("Seeding MySQL with default products...")
            pid = 1
            price = 50
            for cat, items in RAW_PRODUCTS:
                for item in items:
                    img = get_image_for_product(item, cat)
                    c.execute('''INSERT INTO products (ID, Category, Name, Price, Stock, Image)
                                 VALUES (%s, %s, %s, %s, %s, %s)''', (pid, cat, item, price, 150, img))
                    pid += 1
                    price = (price + 15) if price < 1500 else 50
            print("Seeded successfully!")
            
        conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()

# ─── DB HELPER FUNCTIONS ─────────────────────────────────────────────────────

def get_products():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(e)
        return []

def get_product_by_id(pid):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE ID = %s", (int(pid),))
        row = c.fetchone()
        conn.close()
        return row
    except:
        return None

def get_users():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        conn.close()
        return rows
    except:
        return []

def add_user(user_data):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO users (Username, Email, Password) VALUES (%s, %s, %s)", 
                  (user_data.get('Username'), user_data.get('Email'), user_data.get('Password')))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

def get_orders():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT `Order ID`, `Customer Name`, Phone, Address, `Delivery Date`, Items, `Total Amount`, Date, Time, Status FROM orders')
        rows = c.fetchall()
        conn.close()
        return rows
    except:
        return []

def add_order(order_data):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('''INSERT INTO orders (`Order ID`, `Customer Name`, Phone, Address, `Delivery Date`, Items, `Total Amount`, Date, Time, Status)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                  (order_data.get('Order ID'), order_data.get('Customer Name'), order_data.get('Phone'),
                   order_data.get('Address'), order_data.get('Delivery Date'), order_data.get('Items'),
                   order_data.get('Total Amount'), order_data.get('Date'), order_data.get('Time'), order_data.get('Status')))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

def update_stock(cart):
    try:
        conn = get_db()
        c = conn.cursor()
        for pid_str, item in cart.items():
            qty = item['quantity']
            c.execute("UPDATE products SET Stock = Stock - %s WHERE ID = %s", (qty, int(pid_str)))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Failed to update stock: {e}")


# ─── AUTH ROUTES ─────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check Admin First
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            session['user'] = 'Admin'
            flash("Welcome to the Admin Dashboard", "success")
            return redirect(url_for('admin_dashboard'))

        # Check Regular User
        users = get_users()
        user = next((u for u in users if u.get('Username') == username and str(u.get('Password')) == password), None)

        if user:
            session['user'] = username
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials or user does not exist", "danger")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        users = get_users()
        if any(u.get('Username') == username for u in users):
            flash("Username already exists", "danger")
        else:
            add_user({"Username": username, "Email": email, "Password": password})
            session['user'] = username
            flash("Account created successfully!", "success")
            return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('admin_logged_in', None)
    flash("You have been logged out", "info")
    return redirect(url_for('home'))


# ─── CORE ROUTES ─────────────────────────────────────────────────────────────

@app.route('/')
def home():
    products = get_products()
    offers = [p for p in products if p.get('Category') in ['Premium Fancy Crackers', 'Fancy Sky Shots']][:6]
    return render_template('home.html', offers=offers)

@app.route('/shop')
def shop():
    products = get_products()
    categorized_products = {}
    for p in products:
        cat = p.get('Category')
        if not cat: continue
        if cat not in categorized_products:
            categorized_products[cat] = []
        categorized_products[cat].append(p)
    return render_template('shop.html', categories=categorized_products)

@app.route('/api/add-to-cart', methods=['POST'])
def api_add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}

    data = request.json
    product_id = data.get('product_id')
    product = get_product_by_id(product_id)

    if product:
        pid_str = str(product_id)
        if pid_str in session['cart']:
            session['cart'][pid_str]['quantity'] += 1
        else:
            session['cart'][pid_str] = {
                'name': product.get('Name'),
                'price': float(product.get('Price', 0)),
                'quantity': 1,
                'category': product.get('Category')
            }
        session.modified = True

        cart_count = sum(item['quantity'] for item in session['cart'].values())
        return jsonify({
            'status': 'success',
            'message': f"{product.get('Name')} added to cart!",
            'cart_count': cart_count
        })

    return jsonify({'status': 'error', 'message': 'Product not found'}), 404

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'cart' not in session:
        session['cart'] = {}

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        action = request.form.get('action')

        if action == 'remove':
            pid_str = str(product_id)
            if pid_str in session['cart']:
                del session['cart'][pid_str]
                session.modified = True
                flash("Item removed from cart.", "info")
        elif action == 'update':
            pid_str = str(product_id)
            qty = int(request.form.get('quantity', 1))
            if pid_str in session['cart'] and qty > 0:
                session['cart'][pid_str]['quantity'] = qty
                session.modified = True
        elif action == 'apply_discount':
            code = request.form.get('discount_code', '').strip()
            percents = {
                '000000000000': 10,
                '111111111111111': 20,
                '333333333333333': 30,
                '444444444444444': 40,
                '555555555555555': 50
            }
            if code in percents:
                session['discount'] = percents[code]
                session['discount_code'] = code
                flash(f"Coupon applied: {percents[code]}% off!", "success")
            elif code.isdigit() and 0 < int(code) < 100:
                session['discount'] = int(code)
                session['discount_code'] = code + "% off"
                flash(f"Discount applied: {code}% off!", "success")
            else:
                session['discount'] = 0
                session.pop('discount_code', None)
                flash("Invalid or missing coupon code.", "danger")
        elif action == 'remove_discount':
            session['discount'] = 0
            session.pop('discount_code', None)
            flash("Coupon removed.", "info")
        return redirect(url_for('cart'))

    base_total = sum(item['price'] * item['quantity'] for item in session['cart'].values())
    discount_pct = session.get('discount', 0)
    discount_amount = base_total * (discount_pct / 100.0)
    total = base_total - discount_amount
    discount_code = session.get('discount_code')

    return render_template('cart.html', cart=session['cart'], base_total=base_total, discount_pct=discount_pct, discount_amount=discount_amount, total=total, discount_code=discount_code)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'cart' not in session or not session['cart']:
        return redirect(url_for('shop'))

    base_total = sum(item['price'] * item['quantity'] for item in session['cart'].values())
    discount_pct = session.get('discount', 0)
    total = base_total - (base_total * (discount_pct / 100.0))

    if request.method == 'POST':
        session['checkout_info'] = {
            'name': request.form.get('name'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'delivery_date': request.form.get('delivery_date'),
            'recommended_date': request.form.get('recommended_date'),
            'total': total
        }
        return redirect(url_for('payment'))

    from datetime import timedelta
    rec_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
    return render_template('checkout.html', total=total, rec_date=rec_date)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'checkout_info' not in session:
        return redirect(url_for('cart'))

    if request.method == 'POST':
        info = session['checkout_info']
        items_str = ", ".join([f"{v['name']} (x{v['quantity']})" for k, v in session['cart'].items()])

        order_data = {
            "Order ID": f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "Customer Name": info.get('name'),
            "Phone": info.get('phone'),
            "Address": info.get('address'),
            "Delivery Date": info.get('delivery_date', 'Not Specified') + " (Rec: " + info.get('recommended_date', '') + ")",
            "Items": items_str,
            "Total Amount": info.get('total'),
            "Date": datetime.now().strftime('%Y-%m-%d'),
            "Time": datetime.now().strftime('%H:%M:%S'),
            "Status": "Paid & Processing"
        }

        add_order(order_data)
        update_stock(session['cart'])

        session.pop('cart', None)
        session.pop('checkout_info', None)
        return redirect(url_for('order_success', order_id=order_data['Order ID']))

    return render_template('payment.html', total=session['checkout_info'].get('total', 0))

@app.route('/order-success/<order_id>')
def order_success(order_id):
    return render_template('order_success.html', order_id=order_id)

@app.route('/track-order', methods=['GET', 'POST'])
def track_order():
    order = None
    if request.method == 'POST':
        order_id = request.form.get('order_id').strip()
        orders = get_orders()
        order = next((o for o in orders if o.get('Order ID') == order_id), None)
        if not order:
            flash("Order ID not found.", "danger")
    return render_template('track_order.html', order=order)

@app.route('/prev-orders')
def prev_orders():
    if 'user' not in session:
        flash("Please login to view your previous orders.", "warning")
        return redirect(url_for('login'))
    
    username = session['user']
    all_orders = get_orders()
    # Filter orders by current logged in user
    # If the database doesn't have a specific 'Username' column, we match by 'Customer Name'
    # but for a real app we'd use a foreign key. Here we'll check if the schema handles it or match by name.
    user_orders = [o for o in all_orders if o.get('Customer Name') == username]
    
    return render_template('prev_orders.html', orders=user_orders)

@app.route('/contact')
def contact():
    location = "Sivakasi Main Road, Virudhunagar District, Tamil Nadu, 626123, India"
    return render_template('contact.html', location=location)


# ─── ADMIN ROUTES ─────────────────────────────────────────────────────────────

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    orders = get_orders()
    products = get_products()

    daily_revenue = {}
    total_sales = 0

    for order in orders:
        date = order.get('Date', 'Unknown')
        amount = float(order.get('Total Amount', 0))
        total_sales += amount

        if date not in daily_revenue:
            daily_revenue[date] = {'total': 0, 'order_count': 0, 'orders': []}

        daily_revenue[date]['total'] += amount
        daily_revenue[date]['order_count'] += 1
        daily_revenue[date]['orders'].append(order)

    sorted_dates = sorted(daily_revenue.keys(), reverse=True)

    return render_template('admin_dashboard.html',
                           orders=orders,
                           products=products,
                           daily_revenue=daily_revenue,
                           sorted_dates=sorted_dates,
                           total_sales=total_sales)

@app.route('/admin/products/add', methods=['POST'])
def add_product():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    category = request.form.get('category')
    name = request.form.get('name')
    price = float(request.form.get('price'))
    stock = int(request.form.get('stock'))
    image = get_image_for_product(name, category)
    
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT MAX(ID) as max_id FROM products")
        max_id_row = c.fetchone()
        new_id = (max_id_row['max_id'] + 1) if max_id_row and max_id_row.get('max_id') is not None else 1
        
        c.execute('''INSERT INTO products (ID, Category, Name, Price, Stock, Image)
                     VALUES (%s, %s, %s, %s, %s, %s)''', (new_id, category, name, price, stock, image))
        conn.commit()
        conn.close()
        flash("Product added successfully", "success")
    except Exception as e:
        flash(f"Error adding product: {e}", "danger")
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/products/delete/<int:pid>')
def delete_product(pid):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE ID = %s", (int(pid),))
        conn.commit()
        conn.close()
        flash("Product deleted successfully", "success")
    except Exception as e:
        flash(f"Error deleting product: {e}", "danger")
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/orders/update-status', methods=['POST'])
def update_order_status():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    order_id = request.form.get('order_id')
    new_status = request.form.get('status')
    
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE orders SET Status = %s WHERE `Order ID` = %s", (new_status, order_id))
        conn.commit()
        conn.close()
        flash(f"Order {order_id} updated to {new_status}", "success")
    except Exception as e:
        flash(f"Error updating order status: {e}", "danger")
        
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    # Initialize DB (creates default records if not present)
    init_db()
    
    app.run(debug=True, port=5000)
