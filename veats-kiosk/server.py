from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import datetime

# Load the database password
load_dotenv() 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# database tables
class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    is_available = db.Column(db.Boolean, default=True)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending') 
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

# api routes
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "V-Eats backend is running smoothly!"}), 200

@app.route('/api/menu', methods=['GET'])
def get_menu():
    # Fetch all available food items from the database
    items = MenuItem.query.filter_by(is_available=True).all()
    # Format them into a neat JSON list
    menu_list = [{"id": item.id, "name": item.name, "price": item.price, "category": item.category} for item in items]
    return jsonify(menu_list), 200

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        # 1. Grab the digital receipt sent by the kiosk
        data = request.json
        cart_items = data.get('cart', {})
        total_amount = data.get('total', 0.0)

        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400

        # 2. Create the main Order receipt in the database
        new_order = Order(total_amount=total_amount, status='Pending')
        db.session.add(new_order)
        db.session.flush() # This safely generates the new Order ID before committing!

        # 3. Loop through the cart and link the specific foods to the new Order ID
        for item_name, details in cart_items.items():
            # Find the actual database ID for the food item
            menu_item = MenuItem.query.filter_by(name=item_name).first()
            if menu_item:
                order_item = OrderItem(
                    order_id=new_order.id,
                    menu_item_id=menu_item.id,
                    quantity=details['quantity']
                )
                db.session.add(order_item)

        # 4. Save everything permanently
        db.session.commit()
        return jsonify({"message": "Order placed successfully!", "order_id": new_order.id}), 201

    except Exception as e:
        db.session.rollback() # If anything crashes, cancel the transaction so the DB doesn't break
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/pending', methods=['GET'])
def get_pending_orders():
    """Fetches all incomplete orders for the kitchen screen."""
    # Note: Assuming you have your Order and OrderItem models set up!
    orders = Order.query.filter_by(status='Pending').all()
    
    pending_list = []
    for order in orders:
        # Grab the foods linked to this specific order
        items = OrderItem.query.filter_by(order_id=order.id).all()
        item_details = []
        for item in items:
            food = MenuItem.query.get(item.menu_item_id)
            if food:
                item_details.append(f"{item.quantity}x {food.name}")
                
        pending_list.append({
            "id": order.id,
            "items": item_details
        })
        
    return jsonify(pending_list), 200

@app.route('/api/orders/<int:order_id>/complete', methods=['POST'])
def complete_order(order_id):
    """The cook clicks 'Done', and this clears the ticket."""
    order = Order.query.get(order_id)
    if order:
        order.status = 'Completed'
        db.session.commit()
        return jsonify({"message": "Order cleared!"}), 200
    return jsonify({"error": "Order not found"}), 404

# initialization
if __name__ == '__main__':
    # create the tables in pgAdmin
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    #runs the server on port 5000
    app.run(port=5000, debug=True)