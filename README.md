# VIT Campus Solutions Ecosystem

This is the project for our CDAC credit transfer program of web development with python, we have created two projects. First is a student manager using django framework and the Second project is a Tkinter + Flask based  ordering kiosk for an existing project of ours 'VEats' a canteen ordering system.

## Project Structure

This monorepo is divided into two distinct environments:

### 1. V-Eats Kiosk System (`/veats-kiosk`)
A complete, real-time POS and Kitchen Display System built to reduce student queuing times.
* **Frontend:** Tkinter Touch-Screen Kiosk (Student UI) & Kitchen Display Screen (Staff UI)
* **Backend:** Flask REST API
* **Database:** PostgreSQL
* **Features:** Real-time state management, digital cart calculation, and auto-refreshing network requests.

### 2. Django Campus Manager (`/django-campus-manager`)
A secure, scalable administrative web portal for managing campus data.
* **Framework:** Django (MVT Architecture)
* **Frontend:** Bootstrap 5, HTML/CSS
* **Database:** PostgreSQL
* **Features:** Secure user authentication, session-based routing, and complex Many-to-Many relational database mapping (Students to Courses).

---

## Installation & Setup

Because this repository contains two separate applications, you will need to set up two virtual environments.

### Setting up V-Eats
1. `cd veats-kiosk`
2. `python -m venv venv`
3. Activate the environment (Windows: `.\venv\Scripts\activate` | Mac/Linux: `source venv/bin/activate`)
4. `pip install -r requirements.txt`
5. Seed the database: `python seed_db.py`
6. Run the server: `python server.py`
7. Run the clients: `python gui_client.py` and `python kitchen_display.py` 
    (all three on different terminals)

### Setting up Campus Manager
1. `cd django-campus-manager`
2. `python -m venv venv`
3. Activate the environment.
4. `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`
7. Navigate to `http://127.0.0.1:8000/`

---
*Developed by Pranit Waghmare (24101A0053) and Martand Jadhav (24101A0054)*