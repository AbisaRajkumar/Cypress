import tkinter as tk
from tkinter import messagebox
from data import load_users, save_user
from main_menu import MainMenu
import re

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Cypress Login")

        tk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(root, text="Password").grid(row=1, column=0, padx=10, pady=5)

        self.username_entry = tk.Entry(root)
        self.password_entry = tk.Entry(root, show="*")
        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        tk.Button(root, text="Login", command=self.login, bg="lightgreen").grid(row=2, column=0, pady=10)
        tk.Button(root, text="Sign Up", command=self.open_signup, bg="lightblue").grid(row=2, column=1)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        users = load_users()

        for u in users:
            if u[0] == username and u[1] == password:
                role = u[5] if len(u) > 5 else "resident"
                messagebox.showinfo("Login Success", f"Welcome {u[2]} {u[3]}! Logged in as {role.title()}.")
                self.root.destroy()
                MainMenu(role=role)
                return

        messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_signup(self):
        SignUpWindow()

class SignUpWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Create Account")

        row = 0

        # Role selection first
        tk.Label(self.window, text="Register as:").grid(row=row, column=0, sticky="w", pady=5)
        self.role_var = tk.StringVar()
        self.role_var.set("Resident")
        role_menu = tk.OptionMenu(self.window, self.role_var, "Resident", "City Official")
        role_menu.config(width=25)
        role_menu.grid(row=row, column=1, pady=5, padx=5, sticky="ew")

        # Input fields
        fields = ["First Name", "Last Name", "Phone", "Username", "Password"]
        self.entries = {}
        for field in fields:
            row += 1
            tk.Label(self.window, text=field + ":").grid(row=row, column=0, sticky="w", pady=5)
            entry = tk.Entry(self.window, show="*" if field == "Password" else "")
            entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
            entry.config(width=25)
            self.entries[field] = entry

        # Password hint
        row += 1
        self.password_hint = tk.Label(self.window, text="", fg="red")
        self.password_hint.grid(row=row, column=0, columnspan=2, pady=(0, 5))

        # Show password checkbox
        row += 1
        self.show_var = tk.BooleanVar()
        tk.Checkbutton(self.window, text="Show Password", variable=self.show_var,
                       command=self.toggle_password_visibility).grid(row=row, column=0, columnspan=2)

        # Register button
        row += 1
        tk.Button(self.window, text="Register", command=self.register,
                  bg="lightgreen", width=25).grid(row=row, column=0, columnspan=2, pady=10)

        self.window.columnconfigure(1, weight=1)

    def toggle_password_visibility(self):
        show = "" if self.show_var.get() else "*"
        self.entries["Password"].config(show=show)

    def is_strong_password(self, password):
        errors = []
        if len(password) < 8:
            errors.append("at least 8 characters")
        if not re.search(r"[A-Z]", password):
            errors.append("an uppercase letter")
        if not re.search(r"[a-z]", password):
            errors.append("a lowercase letter")
        if not re.search(r"[0-9]", password):
            errors.append("a number")
        if not re.search(r"[!@#$%^&*()_+]", password):
            errors.append("a special character (!@#$...)")
        return errors

    def format_phone_number(self, number):
        number = re.sub(r"[^\d]", "", number)  # Remove non-digit characters
        if len(number) == 10:
            return f"+1-{number[:3]}-{number[3:6]}-{number[6:]}"
        elif len(number) == 11 and number.startswith("1"):
            return f"+1-{number[1:4]}-{number[4:7]}-{number[7:]}"
        else:
            return None

    def register(self):
        fn = self.entries["First Name"].get().strip()
        ln = self.entries["Last Name"].get().strip()
        raw_phone = self.entries["Phone"].get().strip()
        username = self.entries["Username"].get().strip()
        password = self.entries["Password"].get().strip()
        role = self.role_var.get().strip().lower()

        if not all([fn, ln, raw_phone, username, password, role]):
            messagebox.showerror("Missing Info", "Please fill in all fields.")
            return

        formatted_phone = self.format_phone_number(raw_phone)
        if not formatted_phone:
            messagebox.showerror("Invalid Phone", "Phone number must be 10 digits (Canada), e.g. 4165551234")
            return

        password_errors = self.is_strong_password(password)
        if password_errors:
            self.password_hint.config(
                text="Password must include: " + ", ".join(password_errors),
                fg="red"
            )
            return
        else:
            self.password_hint.config(text="")

        users = load_users()
        for u in users:
            if u[2].lower() == fn.lower() and u[3].lower() == ln.lower():
                messagebox.showerror("Duplicate Name", "A user with the same name already exists.")
                return
            if u[0] == username:
                messagebox.showerror("Username Taken", "This username is already in use.")
                return

        save_user(username, password, fn, ln, formatted_phone, role)
        messagebox.showinfo("Success", "Account created. You can now log in.")
        self.window.destroy()
