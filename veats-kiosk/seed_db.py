from server import app, db, MenuItem

# The V-Eats Starter Menu
canteen_menu = [
    MenuItem(name="Vada Pav", price=15.0, category="Snacks"),
    MenuItem(name="Samosa", price=15.0, category="Snacks"),
    MenuItem(name="Masala Dosa", price=45.0, category="Meals"),
    MenuItem(name="Misal Pav", price=50.0, category="Meals"),
    MenuItem(name="Cutting Chai", price=10.0, category="Drinks"),
    MenuItem(name="Cold Coffee", price=30.0, category="Drinks")
]

with app.app_context():
    # Check if the menu is already populated so we don't duplicate items
    if MenuItem.query.first() is None:
        db.session.add_all(canteen_menu)
        db.session.commit()
        print("Success: V-Eats Menu loaded into PostgreSQL!")
    else:
        print("Menu already exists in the database.")