import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from data import load_contacts
from config import ISSUE_COLORS

class CallLookupWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Report by Call")

        self.selected_coords = None

        main_frame = tk.Frame(root)
        main_frame.pack(padx=10, pady=10)

        # Left form
        form_frame = tk.Frame(main_frame)
        form_frame.grid(row=0, column=0, sticky="n")

        self.choose_btn = tk.Button(form_frame, text="Select Location on Map", command=self.enable_map_click, width=30)
        self.choose_btn.pack(pady=5)

        tk.Label(form_frame, text="Issue Category").pack()
        self.issue_type_var = tk.StringVar()
        self.issue_type_menu = ttk.Combobox(form_frame, textvariable=self.issue_type_var, state='readonly', width=27)
        self.issue_type_menu['values'] = list(ISSUE_COLORS.keys())
        self.issue_type_menu.pack(pady=5)

        self.lookup_btn = tk.Button(form_frame, text="Find Contact", command=self.find_contact, bg="lightblue", width=30)
        self.lookup_btn.pack(pady=10)

        self.result_label = tk.Label(form_frame, text="", wraplength=200, justify="left", fg="green")
        self.result_label.pack(pady=10)

        # Right map
        self.map_img = Image.open("map_image.png")
        self.map_img = self.map_img.resize((int(self.map_img.width * 0.6), int(self.map_img.height * 0.6)))
        self.tk_map_img = ImageTk.PhotoImage(self.map_img)
        self.canvas = tk.Canvas(main_frame, width=self.map_img.width, height=self.map_img.height)
        self.canvas.grid(row=0, column=1)
        self.canvas.create_image(0, 0, image=self.tk_map_img, anchor='nw')
        self.canvas.bind("<Button-1>", self.on_map_click)

        self.contacts = load_contacts()

    def enable_map_click(self):
        messagebox.showinfo("Select", "Click on the map to choose a location.")
        self.selecting = True

    def on_map_click(self, event):
        if getattr(self, 'selecting', False):
            self.selected_coords = (event.x, event.y)
            messagebox.showinfo("Location Selected", f"You selected X: {event.x}, Y: {event.y}")
            self.selecting = False

    def get_location_from_coords(self, x, y):
        if 5 <= x <= 398 and 5 <= y <= 233:
            return "Zone 1"
        elif 5 <= x <= 398 and 234 <= y <= 460:
            return "Zone 2"
        elif 399 <= x <= 718 and 5 <= y <= 234:
            return "Zone 3"
        elif 399 <= x <= 718 and 235 <= y <= 459:
            return "Zone 4"
        else:
            return "Unknown"

    def find_contact(self):
        category = self.issue_type_var.get()
        if not self.selected_coords or not category:
            messagebox.showerror("Missing Info", "Please select a location and issue category.")
            return

        x, y = self.selected_coords
        location = self.get_location_from_coords(x, y)

        for entry in self.contacts:
            name, loc, contact_type, number = entry
            if loc == location and category.lower() in contact_type.lower():
                self.result_label.config(text=f"📍 Location: {loc}\n☎️ {name}: {number}")
                return

        self.result_label.config(text=f"No contact found for {category} at {location}.")
