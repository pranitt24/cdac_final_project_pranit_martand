import tkinter as tk
import requests

def check_backend():
    try:
        # Ping the Flask route in server.py
        response = requests.get('http://127.0.0.1:5000/api/health')
        status_label.config(text=response.json()['status'], fg="green")
    except requests.exceptions.ConnectionError:
        status_label.config(text="Backend offline. Start server.py first!", fg="red")

# ui
root = tk.Tk()
root.title("V-Eats Kiosk Terminal")
root.geometry("400x300")

title_label = tk.Label(root, text="V-Eats Touch Kiosk", font=("Helvetica", 16))
title_label.pack(pady=20)

status_label = tk.Label(root, text="Hit the button to connect to the kitchen", font=("Helvetica", 12))
status_label.pack(pady=10)

test_button = tk.Button(root, text="Ping Server", command=check_backend)
test_button.pack(pady=20)

root.mainloop()