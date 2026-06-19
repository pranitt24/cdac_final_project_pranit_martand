import tkinter as tk
from tkinter import messagebox
import requests

# --- CONSTANTS & STATE ---
SERVER_URL = "http://127.0.0.1:5000"
cart = {} # This dictionary holds the student's current order

def fetch_menu():
    """Talks to the Flask kitchen and grabs the menu."""
    try:
        response = requests.get(f"{SERVER_URL}/api/menu")
        return response.json()
    except requests.exceptions.ConnectionError:
        print("Backend is offline!")
        return []

def add_to_cart(name, price):
    """Adds items to the cart dictionary and refreshes the receipt."""
    if name in cart:
        cart[name]['quantity'] += 1
    else:
        cart[name] = {'price': price, 'quantity': 1}
    
    update_cart_display()

def update_cart_display():
    """Clears the old receipt and redraws the current cart items."""
    # 1. Wipe the current text screen clean
    cart_receipt.config(state="normal")
    cart_receipt.delete("1.0", tk.END)
    
    total = 0
    receipt_text = ""

    # 2. Loop through the cart and calculate costs
    for item_name, details in cart.items():
        qty = details['quantity']
        cost = details['price'] * qty
        total += cost
        receipt_text += f"{qty}x {item_name.ljust(15)} ₹{cost}\n"

    # 3. Write the new text and lock the screen so users can't type in it
    cart_receipt.insert(tk.END, receipt_text)
    cart_receipt.config(state="disabled")
    
    # 4. Update the big total label
    total_label.config(text=f"Total: ₹{total}")

def place_order():
    """Packages the cart data and sends it to the Flask kitchen."""
    if not cart:
        messagebox.showwarning("Empty Cart", "Please add some food to your cart first!")
        return

    # Calculate the final total one last time
    final_total = sum(details['price'] * details['quantity'] for details in cart.values())
    
    # Package the data exactly how the kitchen expects it
    order_data = {
        "cart": cart,
        "total": final_total
    }
    
    try:
        # Shoot the POST request to the server
        response = requests.post(f"{SERVER_URL}/api/orders", json=order_data)
        
        if response.status_code == 201:
            order_id = response.json().get('order_id')
            # Show a success pop-up!
            messagebox.showinfo("Success!", f"Your order has been sent to the kitchen!\n\nYour Order Number is: #{order_id}")
            
            # Wipe the screen for the next student
            cart.clear()
            update_cart_display()
        else:
            messagebox.showerror("Error", "The kitchen rejected the order. Please try again.")
            
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Offline", "Cannot reach the kitchen! Is the server running?")


# ==========================================
#               UI SETUP 
# ==========================================
root = tk.Tk()
root.title("V-Eats Kiosk Terminal")
root.geometry("900x600") # Made it a bit wider to fit the cart!
root.configure(bg="#f4f4f9")

# --- HEADER ---
header_frame = tk.Frame(root, bg="#ff4757", pady=20)
header_frame.pack(fill="x")

title_label = tk.Label(header_frame, text="Welcome to V-Eats", font=("Helvetica", 24, "bold"), bg="#ff4757", fg="white")
title_label.pack()

# --- MAIN SPLIT CONTAINER ---
# This frame holds BOTH the menu (left) and the cart (right)
main_frame = tk.Frame(root, bg="#f4f4f9")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# ------------------------------------------
# LEFT SIDE: MENU GRID
# ------------------------------------------
menu_frame = tk.Frame(main_frame, bg="#f4f4f9")
menu_frame.pack(side="left", fill="both", expand=True)

menu_items = fetch_menu()
row_num, col_num = 0, 0

for item in menu_items:
    btn = tk.Button(
        menu_frame, 
        text=f"{item['name']}\n₹{item['price']}", 
        font=("Helvetica", 14, "bold"),
        bg="white",
        width=15, 
        height=4,
        command=lambda name=item['name'], price=item['price']: add_to_cart(name, price)
    )
    btn.grid(row=row_num, column=col_num, padx=10, pady=10)
    
    col_num += 1
    if col_num > 2: # 3 items per row
        col_num = 0
        row_num += 1

# ------------------------------------------
# RIGHT SIDE: LIVE CART
# ------------------------------------------
cart_frame = tk.Frame(main_frame, bg="white", width=300, relief="ridge", bd=2)
cart_frame.pack(side="right", fill="y", padx=10)

cart_title = tk.Label(cart_frame, text="Your Order", font=("Helvetica", 16, "bold"), bg="white")
cart_title.pack(pady=10)

# The "Receipt Paper"
cart_receipt = tk.Text(cart_frame, width=30, height=10, font=("Courier", 12), bg="#fafafa")
cart_receipt.pack(padx=10, pady=10)
cart_receipt.config(state="disabled") # Prevents the user from typing in it

total_label = tk.Label(cart_frame, text="Total: ₹0.0", font=("Helvetica", 18, "bold"), bg="white", fg="#2ed573")
total_label.pack(pady=5)

checkout_btn = tk.Button(cart_frame, text="Place Order", font=("Helvetica", 16, "bold"), bg="#2ed573", fg="white", pady=10, command=place_order)
checkout_btn.pack(side="bottom", fill="x", padx=10, pady=20)

# --- START RUNNING ---
root.mainloop()