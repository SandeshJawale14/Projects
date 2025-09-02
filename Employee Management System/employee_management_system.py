import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),  
    "database": os.getenv("DB_DATABASE", "employee_db")
}ss

EMPLOYEE_FIELDS = [
    ("Name", 100, True, True),    
    ("Email", 100, True, True),
    ("Phone", 15, True, False),
    ("Address", 255, False, False),
    ("Post", 50, True, False),
    ("Salary", None, True, False),   
]
PROMOTE_AMOUNT = 5000

EMAIL_REGEX = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
PHONE_REGEX = re.compile(r'^(0|91)?[7-9]\d{9}$')

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    con = get_connection()
    cur = con.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS employees (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            phone VARCHAR(15) NOT NULL,
            address VARCHAR(255),
            post VARCHAR(50) NOT NULL,
            salary INT NOT NULL CHECK (salary >= 0)
        )
    """)
    con.commit()
    cur.close()
    con.close()

def fetch_all_employees():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM employees ORDER BY id")
    data = cur.fetchall()
    cur.close()
    con.close()
    return data

def insert_employee(values):
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO employees (name, email, phone, address, post, salary)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(values))
    con.commit()
    cur.close()
    con.close()

def update_employee(emp_id, values):
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        UPDATE employees
        SET name=%s, email=%s, phone=%s, address=%s, post=%s, salary=%s
        WHERE id=%s
    """, (*values, emp_id))
    con.commit()
    cur.close()
    con.close()

def delete_employee(emp_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM employees WHERE id=%s", (emp_id,))
    con.commit()
    cur.close()
    con.close()

def promote_employee(emp_id, amount):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE employees SET salary = salary + %s WHERE id=%s", (amount, emp_id))
    con.commit()
    cur.close()
    con.close()

def search_employee_by_name(name):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM employees WHERE name LIKE %s", (f"%{name}%",))
    data = cur.fetchall()
    cur.close()
    con.close()
    return data

class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("1000x660")
        self.selected_id = None
        self.create_widgets()
        self.refresh_tree()

    def create_widgets(self):
       
        ttk.Label(self.root, text="Employee Management System", font=('Segoe UI', 18, 'bold')).pack(pady=12)

        self.tree = ttk.Treeview(self.root, columns=["ID"] + [f[0] for f in EMPLOYEE_FIELDS], show='headings', selectmode='browse')
        for col in ["ID"] + [f[0] for f in EMPLOYEE_FIELDS]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120 if col != "Address" else 220)
        self.tree.pack(padx=18, pady=8, fill='x')
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        frame = ttk.Labelframe(self.root, text="Employee Details")
        frame.pack(pady=10, padx=20, fill='both', expand=False)
        self.entries = {}
        for idx, (label, maxlen, required, unique) in enumerate(EMPLOYEE_FIELDS):
            ttk.Label(frame, text=f"{label}:").grid(row=0, column=idx*2, padx=4, pady=8, sticky='e')
            ent = ttk.Entry(frame, width=18)
            ent.grid(row=0, column=idx*2+1, padx=4, pady=8)
            self.entries[label.lower()] = ent

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill='x', padx=30, pady=10)
        ttk.Button(btn_frame, text="Add", command=self.add_employee).pack(side='left', padx=8)
        ttk.Button(btn_frame, text="Update", command=self.update_employee).pack(side='left', padx=8)
        ttk.Button(btn_frame, text="Delete", command=self.delete_employee).pack(side='left', padx=8)
        ttk.Button(btn_frame, text=f"Promote (+₹{PROMOTE_AMOUNT})", command=self.promote).pack(side='left', padx=8)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).pack(side='right', padx=8)

        # Search bar
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=0)
        ttk.Label(search_frame, text="Search Name:").pack(side='left', padx=5)
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_employee).pack(side='left')

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())
        self.selected_id = None

    def refresh_tree(self, data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if data is None:
            data = fetch_all_employees()
        for rec in data:
            self.tree.insert('', 'end', values=rec)

    def get_form_data(self):
        vals = []
        for name, maxlen, required, unique in EMPLOYEE_FIELDS:
            value = self.entries[name.lower()].get().strip()
            if required and not value:
                messagebox.showerror("Input Error", f"{name} is required.")
                return None
            if maxlen and len(value) > maxlen:
                messagebox.showerror("Input Error", f"{name} is too long (max {maxlen} chars).")
                return None
            vals.append(value)
        
        if not EMAIL_REGEX.fullmatch(vals[1]):
            messagebox.showerror("Input Error", "Invalid Email.")
            return None
        if not PHONE_REGEX.match(vals[2]):
            messagebox.showerror("Input Error", "Invalid Phone.")
            return None
        try:
            salary = int(vals[5])
            if salary < 0: raise ValueError
            vals[5] = salary
        except:
            messagebox.showerror("Input Error", "Salary must be a non-negative integer.")
            return None
        return vals

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            self.clear_form()
            return
        values = self.tree.item(selected[0], "values")[1:]
        for idx, key in enumerate(self.entries.keys()):
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, values[idx])
        self.selected_id = self.tree.item(selected[0], "values")[0]

    def add_employee(self):
        vals = self.get_form_data()
        if not vals:
            return
        try:
            insert_employee(vals)
            self.refresh_tree()
            messagebox.showinfo("Success", "Employee added!")
            self.clear_form()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Duplicate Error", "Name or Email already exists in database.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not add employee:\n{e}")

    def update_employee(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Select an employee from the table first.")
            return
        vals = self.get_form_data()
        if not vals:
            return
        try:
            update_employee(self.selected_id, vals)
            self.refresh_tree()
            messagebox.showinfo("Success", "Employee updated.")
            self.clear_form()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Duplicate Error", "Name or Email already exists in database.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not update employee:\n{e}")

    def delete_employee(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Select an employee from the table first.")
            return
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"): return
        try:
            delete_employee(self.selected_id)
            self.refresh_tree()
            messagebox.showinfo("Deleted", "Employee deleted.")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete employee:\n{e}")

    def promote(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Select an employee from the table first.")
            return
        try:
            promote_employee(self.selected_id, PROMOTE_AMOUNT)
            self.refresh_tree()
            messagebox.showinfo("Promoted", f"Salary increased by ₹{PROMOTE_AMOUNT}.")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Could not promote employee:\n{e}")

    def search_employee(self):
        name = self.search_entry.get().strip()
        if not name:
            self.refresh_tree()
            return
        data = search_employee_by_name(name)
        if not data:
            messagebox.showinfo("No Results", f"No employee found with name matching '{name}'.")
        self.refresh_tree(data)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()
