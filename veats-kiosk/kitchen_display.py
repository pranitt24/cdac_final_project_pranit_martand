import tkinter as tk
import requests

SERVER_URL = "http://127.0.0.1:5000"

def fetch_and_draw_tickets():
    """Pulls orders from the server and draws the ticket cards."""
    # 1. Wipe the current screen clean
    for widget in ticket_board.winfo_children():
        widget.destroy()
        
    try:
        response = requests.get(f"{SERVER_URL}/api/orders/pending")
        if response.status_code == 200:
            orders = response.json()
            
            if not orders:
                tk.Label(ticket_board, text="No pending orders. Kitchen is clear!", font=("Helvetica", 18), bg="#f4f4f9").pack(pady=50)
            else:
                row_num, col_num = 0, 0
                
                # 2. Draw a visual "Card" for every active order
                for order in orders:
                    card = tk.Frame(ticket_board, bg="#fff9c4", relief="solid", bd=2, padx=15, pady=15)
                    card.grid(row=row_num, column=col_num, padx=15, pady=15, sticky="n")
                    
                    # Order Number
                    tk.Label(card, text=f"Order #{order['id']}", font=("Helvetica", 16, "bold"), bg="#fff9c4", fg="#d35400").pack(anchor="w", fill="x", pady=(0, 10))
                    
                    # The Food List
                    for item in order['items']:
                        tk.Label(card, text=item, font=("Courier", 14, "bold"), bg="#fff9c4").pack(anchor="w")
                        
                    # The 'Done' Button
                    tk.Button(
                        card, text="DONE", font=("Helvetica", 12, "bold"), bg="#2ed573", fg="white", 
                        command=lambda oid=order['id']: mark_ticket_done(oid)
                    ).pack(pady=(15, 0), fill="x")
                    
                    # Layout math (4 tickets per row)
                    col_num += 1
                    if col_num > 3:
                        col_num = 0
                        row_num += 1
                        
    except requests.exceptions.ConnectionError:
        tk.Label(ticket_board, text="Offline: Cannot reach server.", font=("Helvetica", 18), bg="#f4f4f9", fg="red").pack(pady=50)

    # 3. THE SECRET SAUCE: Tell Tkinter to run this exact function again in 3000 milliseconds (3 seconds)
    root.after(3000, fetch_and_draw_tickets)

def mark_ticket_done(order_id):
    """Tells the server the food is ready."""
    try:
        requests.post(f"{SERVER_URL}/api/orders/{order_id}/complete")
        # Instantly refresh the screen so the cook sees it disappear
        fetch_and_draw_tickets() 
    except Exception as e:
        print("Failed to clear order:", e)

# --- UI SETUP ---
root = tk.Tk()
root.title("V-Eats Kitchen Display")
root.geometry("1000x600")
root.configure(bg="#f4f4f9")

# Header
tk.Label(root, text="KITCHEN TICKETS - LIVE", font=("Helvetica", 22, "bold"), bg="#353b48", fg="white", pady=15).pack(fill="x")

# The board where the tickets will stick
ticket_board = tk.Frame(root, bg="#f4f4f9")
ticket_board.pack(fill="both", expand=True, padx=20, pady=20)

# Start the infinite looping refresh cycle
fetch_and_draw_tickets()

root.mainloop()