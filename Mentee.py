import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# SQLite database connection setup
db_name = "mentee_management.db"

# Establishing connection to the SQLite database
def connect_db():
    return sqlite3.connect(db_name)

# Create tables if they do not exist
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mentees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            urn TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            dob TEXT NOT NULL,
            hobbies TEXT,
            strengths TEXT,
            achievements TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

    check_and_create_default_user()  # Check and create default user

def check_and_create_default_user():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = 'user'")
    user = cursor.fetchone()
    
    if user is None:  # If the user does not exist
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('user', 'user1234'))
        conn.commit()
    
    cursor.close()
    conn.close()

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            global current_user
            current_user = username
            login_window.destroy()  # Close login window after successful login
            open_dashboard()  # Open dashboard window
        else:
            messagebox.showerror("Login Error", "Invalid username or password")
        cursor.close()
        conn.close()
    except sqlite3.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to create the Login window
def open_login_window():
    global username_entry, password_entry, login_window

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x300")

    tk.Label(login_window, text="Username", font=("Arial", 14)).pack(pady=10)
    username_entry = tk.Entry(login_window, font=("Arial", 14))
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password", font=("Arial", 14)).pack(pady=10)
    password_entry = tk.Entry(login_window, font=("Arial", 14), show="*")
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", font=("Arial", 14), command=login).pack(pady=20)

    login_window.mainloop()

# Function to create the Dashboard after login
def open_dashboard():
    dashboard_window = tk.Tk()
    dashboard_window.title("Dashboard")
    dashboard_window.geometry("800x600")

    tk.Label(dashboard_window, text=f"Welcome, {current_user}", font=("Arial", 16)).pack(pady=20)

    # Buttons for different features
    button_frame = tk.Frame(dashboard_window)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Mentee Details", font=("Arial", 14), width=20, height=2, command=open_mentee_dashboard).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Exit", font=("Arial", 14), width=20 , height=2, command=dashboard_window.quit).pack(side=tk.LEFT, padx=10)

    dashboard_window.mainloop()

# Function to handle Mentee Details
def open_mentee_dashboard():
    mentee_dashboard = tk.Toplevel()
    mentee_dashboard.title("Mentee Details")

    # Buttons for Mentee Actions
    mentee_button_frame = tk.Frame(mentee_dashboard)
    mentee_button_frame.pack(pady=20)

    tk.Button(mentee_button_frame, text="Add Mentee", font=("Arial", 14), width=20, height=2, command=open_add_mentee).pack(side=tk.LEFT, padx=10)
    tk.Button(mentee_button_frame, text="View Mentees", font=("Arial", 14), width=20, height=2, command=view_mentees).pack(side=tk.LEFT, padx=10)

# Function to Add Mentee
def open_add_mentee():
    add_mentee_window = tk.Toplevel()
    add_mentee_window.title("Add Mentee Details")

    # Mentee form fields
    tk.Label(add_mentee_window, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(add_mentee_window, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_mentee_window, text="Roll No:").grid(row=1, column=0, padx=10, pady=5)
    roll_no_entry = tk.Entry(add_mentee_window, width=30)
    roll_no_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_mentee_window, text="URN:").grid(row=2, column=0, padx=10, pady=5)
    urn_entry = tk.Entry(add_mentee_window, width=30)
    urn_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_mentee_window, text="Email:").grid(row=3, column=0, padx=10, pady=5)
    email_entry = tk.Entry(add_mentee_window, width=30)
    email_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(add_mentee_window, text="Department:").grid(row=4, column=0, padx=10, pady=5)
    department_entry = tk.Entry(add_mentee_window, width=30)
    department_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(add_mentee_window, text="Date of Birth:").grid(row=5, column=0, padx=10, pady=5)
    dob_entry = tk.Entry(add_mentee_window, width=30)
    dob_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(add_mentee_window, text="Hobbies:").grid(row=6, column=0, padx=10, pady=5)
    hobbies_entry = tk.Entry(add_mentee_window, width=30)
    hobbies_entry.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(add_mentee_window, text="Strengths:").grid(row=7, column=0, padx=10, pady=5)
    strengths_entry = tk.Entry(add_mentee_window, width=30)
    strengths_entry.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(add_mentee_window, text="Special Achievements:").grid(row=8, column=0, padx=10, pady=5)
    achievements_entry = tk.Entry(add_mentee_window, width=30)
    achievements_entry.grid(row=8, column=1, padx=10, pady=5)

    # Save Mentee Button
    def save_mentee():
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO mentees (name, roll_no, urn, email, department, dob, hobbies, strengths, achievements)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name_entry.get(), roll_no_entry.get(), urn_entry.get(), email_entry.get(),
                  department_entry.get(), dob_entry.get(), hobbies_entry.get(),
                  strengths_entry.get(), achievements_entry.get()))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Mentee added successfully!")
            add_mentee_window.destroy()
        except sqlite3.Error as err:
            messagebox.showerror ("Database Error", f"Error: {err}")

    tk.Button(add_mentee_window, text="Save Mentee", command=save_mentee).grid(row=9, column=1, padx=10, pady=20)

# Function to View Mentees
def view_mentees():
    view_window = tk.Toplevel()
    view_window.title("View Mentees")

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM mentees")
        mentees = cursor.fetchall()

        if not mentees:
            messagebox.showinfo("No Mentees", "No mentees found.")
            return

        # Mentee Data Table
        columns = ("ID", "Name", "Roll No", "URN", "Email", "Department", "Date of Birth", "Hobbies", "Strengths", "Special Achievements")
        mentee_table = ttk.Treeview(view_window, columns=columns, show="headings", height=10)
        mentee_table.pack(pady=20)

        for col in columns:
            mentee_table.heading(col, text=col)
            mentee_table.column(col, width=120, anchor="w")

        for mentee in mentees:
            mentee_table.insert('', 'end', values=mentee)

        cursor.close()
        conn.close()

    except sqlite3.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Run the application
create_tables()  # Ensure tables are created before running the app
open_login_window()