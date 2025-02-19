import sqlite3
from tkinter import *
from tkinter import messagebox

# Database connection
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        department TEXT NOT NULL
    )
""")
conn.commit()

# Function to add an employee
def add_employee():
    name = name_entry.get()
    age = age_entry.get()
    department = dept_entry.get()

    if name and age and department:
        cursor.execute("INSERT INTO employees (name, age, department) VALUES (?, ?, ?)", (name, age, department))
        conn.commit()
        refresh_list()
        messagebox.showinfo("Success", "Employee added successfully!")
    else:
        messagebox.showwarning("Warning", "All fields are required!")

# Function to delete an employee
def delete_employee():
    selected_item = employee_list.curselection()
    if selected_item:
        emp_id = employee_list.get(selected_item).split()[0]
        cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
        conn.commit()
        refresh_list()
        messagebox.showinfo("Success", "Employee deleted!")
    else:
        messagebox.showwarning("Warning", "Select an employee to delete!")

# Function to refresh the employee list
def refresh_list():
    employee_list.delete(0, END)
    cursor.execute("SELECT * FROM employees")
    for row in cursor.fetchall():
        employee_list.insert(END, f"{row[0]} - {row[1]}, {row[2]} years, {row[3]}")

# GUI setup
root = Tk()
root.title("Employee Management System")
root.geometry("400x400")

Label(root, text="Name").pack()
name_entry = Entry(root)
name_entry.pack()

Label(root, text="Age").pack()
age_entry = Entry(root)
age_entry.pack()

Label(root, text="Department").pack()
dept_entry = Entry(root)
dept_entry.pack()

Button(root, text="Add Employee", command=add_employee).pack(pady=5)
Button(root, text="Delete Employee", command=delete_employee).pack(pady=5)

employee_list = Listbox(root, width=50)
employee_list.pack(pady=10)

refresh_list()

# Run the application
root.mainloop()
conn.close()
