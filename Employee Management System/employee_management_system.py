import re
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector

# Database config
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "employee"
}

# Regex patterns for validation
email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
phone_pattern = re.compile(r"(0|91)?[7-9][0-9]{9}")

# DB helper functions

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def employee_exists(emp_id):
    con = get_connection()
    try:
        with con.cursor() as c:
            c.execute("SELECT 1 FROM empdata WHERE Id=%s", (emp_id,))
            return c.fetchone() is not None
    finally:
        con.close()

def employee_name_exists(name):
    con = get_connection()
    try:
        with con.cursor() as c:
            c.execute("SELECT 1 FROM empdata WHERE Name=%s", (name,))
            return c.fetchone() is not None
    finally:
        con.close()

# Main Application Class

class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("850x600")
        self.setup_style()
        self.create_widgets()

    def setup_style(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('TLabel', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6)
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'))

    def create_widgets(self):
        # Title label
        title = ttk.Label(self.root, text="Employee Management System", style='Header.TLabel')
        title.pack(pady=10)

        # Notebook widget for tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=True, fill='both')

        # Create tabs
        self.create_add_tab()
        self.create_display_tab()
        self.create_update_tab()
        self.create_promote_tab()
        self.create_remove_tab()
        self.create_search_tab()

    # ------------------ Add Employee Tab ------------------

    def create_add_tab(self):
        self.tab_add = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_add, text="Add Employee")

        frm = self.tab_add

        # Form fields
        labels = ['Employee Id', 'Name', 'Email', 'Phone', 'Address', 'Post', 'Salary']
        self.add_entries = {}

        for i, label in enumerate(labels):
            ttk.Label(frm, text=label + ':').grid(row=i, column=0, sticky='w', padx=10, pady=5)
            entry = ttk.Entry(frm, width=40)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='w')
            self.add_entries[label.lower()] = entry

        # Add Button
        btn_add = ttk.Button(frm, text="Add Employee", command=self.add_employee)
        btn_add.grid(row=len(labels), column=0, columnspan=2, pady=15)

    def add_employee(self):
        emp_id = self.add_entries['employee id'].get().strip()
        name = self.add_entries['name'].get().strip()
        email = self.add_entries['email'].get().strip()
        phone = self.add_entries['phone'].get().strip()
        address = self.add_entries['address'].get().strip()
        post = self.add_entries['post'].get().strip()
        salary_str = self.add_entries['salary'].get().strip()

        # Validation
        if not emp_id or not name or not email or not phone or not address or not post or not salary_str:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        if employee_exists(emp_id):
            messagebox.showerror("Duplicate Error", f"Employee ID '{emp_id}' already exists.")
            return
        if employee_name_exists(name):
            messagebox.showerror("Duplicate Error", f"Employee Name '{name}' already exists.")
            return
        if not email_regex.fullmatch(email):
            messagebox.showerror("Input Error", "Invalid email format.")
            return
        if not phone_pattern.match(phone):
            messagebox.showerror("Input Error", "Invalid phone number.")
            return
        try:
            salary = int(salary_str)
            if salary < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Salary must be a non-negative integer.")
            return

        # Insert into DB
        try:
            con = get_connection()
            with con.cursor() as c:
                sql = """INSERT INTO empdata (Id, Name, Email_Id, Phone_no, Address, Post, Salary) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                c.execute(sql, (emp_id, name, email, phone, address, post, salary))
                con.commit()
            messagebox.showinfo("Success", f"Employee '{name}' added successfully.")
            # Clear form fields after successful add
            for entry in self.add_entries.values():
                entry.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if con.is_connected():
                con.close()

        self.refresh_display_tab()  # update display tab data

    # ------------------ Display Employees Tab ------------------

    def create_display_tab(self):
        self.tab_display = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_display, text="Display Employees")

        self.display_text = scrolledtext.ScrolledText(self.tab_display, wrap=tk.WORD, font=("Consolas", 10))
        self.display_text.pack(expand=True, fill='both', padx=10, pady=10)
        # Load data immediately
        self.refresh_display_tab()

    def refresh_display_tab(self):
        self.display_text.delete(1.0, tk.END)
        con = get_connection()
        try:
            with con.cursor() as c:
                c.execute("SELECT * FROM empdata ORDER BY Id")
                records = c.fetchall()
                if not records:
                    self.display_text.insert(tk.END, "No employee records found.\n")
                else:
                    for rec in records:
                        text_block = (
                            f"ID: {rec[0]}\n"
                            f"Name: {rec[1]}\n"
                            f"Email: {rec[2]}\n"
                            f"Phone: {rec[3]}\n"
                            f"Address: {rec[4]}\n"
                            f"Post: {rec[5]}\n"
                            f"Salary: {rec[6]:,}\n"
                            f"{'-'*40}\n"
                        )
                        self.display_text.insert(tk.END, text_block)
        except mysql.connector.Error as e:
            self.display_text.insert(tk.END, f"Error retrieving records: {str(e)}")
        finally:
            if con.is_connected():
                con.close()

    # ------------------ Update Employee Tab ------------------

    def create_update_tab(self):
        self.tab_update = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_update, text="Update Employee")

        frm = self.tab_update

        # Employee Id search first
        ttk.Label(frm, text="Employee Id:").grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.update_empid_entry = ttk.Entry(frm, width=30)
        self.update_empid_entry.grid(row=0, column=1, sticky='w')

        btn_search = ttk.Button(frm, text="Search", command=self.update_search_employee)
        btn_search.grid(row=0, column=2, padx=10)

        # Update fields below (disabled initially)
        labels = ['Email', 'Phone', 'Address']
        self.update_entries = {}
        for i, label in enumerate(labels, start=1):
            ttk.Label(frm, text=label + ':').grid(row=i, column=0, sticky='w', padx=10, pady=5)
            entry = ttk.Entry(frm, width=40)
            entry.grid(row=i, column=1, columnspan=2, sticky='w', pady=5)
            entry.config(state='disabled')
            self.update_entries[label.lower()] = entry

        btn_update = ttk.Button(frm, text="Update Employee", command=self.update_employee)
        btn_update.grid(row=5, column=0, columnspan=3, pady=15)
        btn_update.config(state='disabled')
        self.update_btn_update = btn_update

    def update_search_employee(self):
        emp_id = self.update_empid_entry.get().strip()
        if not emp_id:
            messagebox.showwarning("Input Error", "Please enter an Employee Id to search.")
            return
        if not employee_exists(emp_id):
            messagebox.showerror("Not Found", f"Employee ID '{emp_id}' not found.")
            return

        # Fetch current details
        con = get_connection()
        try:
            with con.cursor() as c:
                c.execute("SELECT Email_Id, Phone_no, Address FROM empdata WHERE Id=%s", (emp_id,))
                result = c.fetchone()
                if result:
                    # Enable update entries and fill
                    for key, entry in self.update_entries.items():
                        entry.config(state='normal')
                    self.update_entries['email'].delete(0, tk.END)
                    self.update_entries['email'].insert(0, result[0])
                    self.update_entries['phone'].delete(0, tk.END)
                    self.update_entries['phone'].insert(0, result[1])
                    self.update_entries['address'].delete(0, tk.END)
                    self.update_entries['address'].insert(0, result[2])

                    self.update_btn_update.config(state='normal')
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if con.is_connected():
                con.close()

    def update_employee(self):
        emp_id = self.update_empid_entry.get().strip()
        email = self.update_entries['email'].get().strip()
        phone = self.update_entries['phone'].get().strip()
        address = self.update_entries['address'].get().strip()

        if not email or not phone or not address:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        if not email_regex.fullmatch(email):
            messagebox.showerror("Input Error", "Invalid email format.")
            return
        if not phone_pattern.match(phone):
            messagebox.showerror("Input Error", "Invalid phone number.")
            return

        try:
            con = get_connection()
            with con.cursor() as c:
                c.execute("""
                    UPDATE empdata SET Email_Id=%s, Phone_no=%s, Address=%s WHERE Id=%s
                """, (email, phone, address, emp_id))
                con.commit()
            messagebox.showinfo("Success", "Employee record updated successfully.")
            self.refresh_display_tab()
            # Clear update fields and disable
            for entry in self.update_entries.values():
                entry.delete(0, tk.END)
                entry.config(state='disabled')
            self.update_btn_update.config(state='disabled')
            self.update_empid_entry.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if con.is_connected():
                con.close()

    # ------------------ Promote Employee Tab ------------------

    def create_promote_tab(self):
        self.tab_promote = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_promote, text="Promote Employee")

        frm = self.tab_promote

        ttk.Label(frm, text="Employee Id:").grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.promote_empid_entry = ttk.Entry(frm, width=30)
        self.promote_empid_entry.grid(row=0, column=1, sticky='w')

        ttk.Label(frm, text="Increase Salary Amount:").grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.increase_salary_entry = ttk.Entry(frm, width=30)
        self.increase_salary_entry.grid(row=1, column=1, sticky='w')

        btn_promote = ttk.Button(frm, text="Promote", command=self.promote_employee)
        btn_promote.grid(row=2, column=0, columnspan=2, pady=15)

    def promote_employee(self):
        emp_id = self.promote_empid_entry.get().strip()
        increase_salary_str = self.increase_salary_entry.get().strip()
        if not emp_id:
            messagebox.showerror("Input Error", "Employee Id is required.")
            return
        if not employee_exists(emp_id):
            messagebox.showerror("Not Found", f"Employee Id '{emp_id}' does not exist.")
            return
        try:
            increase_salary = int(increase_salary_str)
            if increase_salary <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Salary increase amount must be a positive integer.")
            return

        con = get_connection()
        try:
            with con.cursor() as c:
                c.execute('SELECT Salary FROM empdata WHERE Id = %s', (emp_id,))
                result = c.fetchone()
                if result is None:
                    messagebox.showerror("Not Found", "Employee record not found.")
                    return
                current_salary = result[0]
                new_salary = current_salary + increase_salary

                c.execute('UPDATE empdata SET Salary = %s WHERE Id = %s', (new_salary, emp_id))
                con.commit()
            messagebox.showinfo("Success", f"Employee promoted. New salary: {new_salary}")
            self.refresh_display_tab()
            self.promote_empid_entry.delete(0, tk.END)
            self.increase_salary_entry.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if con.is_connected():
                con.close()

    # ------------------ Remove Employee Tab ------------------

    def create_remove_tab(self):
        self.tab_remove = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_remove, text="Remove Employee")

        frm = self.tab_remove

        ttk.Label(frm, text="Employee Id:").grid(row=0, column=0, sticky='w', padx=10, pady=20)
        self.remove_empid_entry = ttk.Entry(frm, width=30)
        self.remove_empid_entry.grid(row=0, column=1, sticky='w')

        btn_remove = ttk.Button(frm, text="Remove Employee", command=self.remove_employee)
        btn_remove.grid(row=1, column=0, columnspan=2, pady=15)

    def remove_employee(self):
        emp_id = self.remove_empid_entry.get().strip()
        if not emp_id:
            messagebox.showerror("Input Error", "Employee Id is required.")
            return
        if not employee_exists(emp_id):
            messagebox.showerror("Not Found", f"Employee Id '{emp_id}' does not exist.")
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure to remove employee '{emp_id}'?")
        if not confirm:
            return

        con = get_connection()
        try:
            with con.cursor() as c:
                c.execute("DELETE FROM empdata WHERE Id=%s", (emp_id,))
                con.commit()
            messagebox.showinfo("Success", "Employee removed successfully.")
            self.refresh_display_tab()
            self.remove_empid_entry.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if con.is_connected():
                con.close()

    # ------------------ Search Employee Tab ------------------

    def create_search_tab(self):
        self.tab_search = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_search, text="Search Employee")

        frm = self.tab_search

        ttk.Label(frm, text="Employee Id:").grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.search_empid_entry = ttk.Entry(frm, width=30)
        self.search_empid_entry.grid(row=0, column=1, sticky='w')

        btn_search = ttk.Button(frm, text="Search", command=self.search_employee)
        btn_search.grid(row=0, column=2, padx=10)

        # Result area
        self.search_result_text = scrolledtext.ScrolledText(frm, height=15, font=("Consolas", 11))
        self.search_result_text.grid(row=1, column=0, columnspan=3, padx=10, pady=15, sticky='nsew')

        # Make sure the frame expands the text widget
        frm.grid_rowconfigure(1, weight=1)
        frm.grid_columnconfigure(1, weight=1)

    def search_employee(self):
        emp_id = self.search_empid_entry.get().strip()
        self.search_result_text.delete(1.0, tk.END)
        if not emp_id:
            messagebox.showwarning("Input Error", "Please enter an Employee Id to search.")
            return

        con = get_connection()
        try:
            with con.cursor() as c:
                c.execute("SELECT * FROM empdata WHERE Id=%s", (emp_id,))
                record = c.fetchone()
                if record:
                    text_block = (
                        f"ID: {record[0]}\n"
                        f"Name: {record[1]}\n"
                        f"Email: {record[2]}\n"
                        f"Phone: {record[3]}\n"
                        f"Address: {record[4]}\n"
                        f"Post: {record[5]}\n"
                        f"Salary: {record[6]:,}\n"
                    )
                    self.search_result_text.insert(tk.END, text_block)
                else:
                    self.search_result_text.insert(tk.END, "Employee record not found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if con.is_connected():
                con.close()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()
