import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import os
from data import save_issue, load_issues
from config import ISSUE_COLORS, DB_FILE

class MapReportingWindow:
    def __init__(self, root, role="resident"):
        self.root = root
        self.role = role
        self.click_mode = False
        self.markers = []
        self.issues = []
        self.selected_coords = None

        main_frame = tk.Frame(root)
        main_frame.pack(padx=10, pady=10)

        # Left side form
        if self.role == "resident":
            form_frame = tk.Frame(main_frame)
            form_frame.grid(row=0, column=0, sticky="n")

            self.choose_btn = tk.Button(form_frame, text="Choose Location on Map", command=self.enable_click_mode, width=30)
            self.choose_btn.pack(pady=5)

            tk.Label(form_frame, text="Category").pack()
            self.issue_type_var = tk.StringVar()
            self.issue_type_menu = ttk.Combobox(form_frame, textvariable=self.issue_type_var, state='readonly', width=27)
            self.issue_type_menu['values'] = list(ISSUE_COLORS.keys())
            self.issue_type_menu.pack(pady=5)

            tk.Label(form_frame, text="Description").pack()
            self.description_entry = tk.Text(form_frame, height=4, width=30)
            self.description_entry.pack(pady=5)

            self.submit_btn = tk.Button(form_frame, text="Submit", command=self.submit_issue, bg="lightgreen", width=30)
            self.submit_btn.pack(pady=10)

        # Right side map (scaled down)
        self.map_img = Image.open("map_image.png")
        self.map_img = self.map_img.resize((int(self.map_img.width * 0.7), int(self.map_img.height * 0.7)))
        self.tk_map_img = ImageTk.PhotoImage(self.map_img)
        self.canvas = tk.Canvas(main_frame, width=self.map_img.width, height=self.map_img.height)
        self.canvas.grid(row=0, column=1)
        self.canvas.create_image(0, 0, image=self.tk_map_img, anchor='nw')
        self.canvas.bind("<Button-1>", self.on_map_click if self.role == "resident" else self.handle_official_click)

        self.load_existing_issues()

    def enable_click_mode(self):
        messagebox.showinfo("Ready", "Click a location on the map to select it.")
        self.click_mode = True

    def on_map_click(self, event):
        if not self.click_mode:
            return
        self.selected_coords = (event.x, event.y)
        messagebox.showinfo("Location Selected", f"Location chosen at X: {event.x}, Y: {event.y}")
        self.click_mode = False

    def submit_issue(self):
        if not self.selected_coords:
            messagebox.showerror("Missing Info", "Please choose a location on the map.")
            return
        issue_type = self.issue_type_var.get()
        description = self.description_entry.get("1.0", tk.END).strip()

        if not issue_type or not description:
            messagebox.showerror("Missing Info", "Please select a category and enter a description.")
            return

        x, y = self.selected_coords
        status = "Unsolved"
        save_issue(x, y, issue_type, description)
        self.add_marker(x, y, issue_type, description, status)
        self.selected_coords = None
        self.issue_type_var.set("")
        self.description_entry.delete("1.0", tk.END)

    def add_marker(self, x, y, issue_type, description, status):
        if status.lower() == "solved":
            return

        color = ISSUE_COLORS.get(issue_type, "black")
        marker = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=color, outline="black")

        def show_tooltip(event):
            tooltip_text = f"Status: {status}\n{description}"
            tooltip = tk.Toplevel(self.root)
            tooltip.wm_overrideredirect(True)
            tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=tooltip_text, background="grey", relief='solid', borderwidth=1)
            label.pack()
            self.canvas.tooltip = tooltip
            self.canvas.itemconfig(marker, fill="white")

        def hide_tooltip(event):
            if hasattr(self.canvas, 'tooltip'):
                self.canvas.tooltip.destroy()
                del self.canvas.tooltip
            self.canvas.itemconfig(marker, fill=color)

        def handle_click(event, index=len(self.issues)):
            if self.role == "city official":
                self.update_status_dialog(index)

        self.canvas.tag_bind(marker, "<Enter>", show_tooltip)
        self.canvas.tag_bind(marker, "<Leave>", hide_tooltip)
        self.canvas.tag_bind(marker, "<Button-1>", handle_click)

        self.issues.append({
            "marker": marker,
            "x": x,
            "y": y,
            "type": issue_type,
            "desc": description,
            "status": status
        })

    def load_existing_issues(self):
        if not os.path.exists(DB_FILE):
            return
        for line in load_issues():
            parts = line.strip().split('|')
            if len(parts) >= 5:
                _, coord, issue_type, description, status = map(str.strip, parts)
                x_str, y_str = coord.split(',')
                self.add_marker(int(float(x_str)), int(float(y_str)), issue_type, description, status.replace("Status:", "").strip())

    def update_status_dialog(self, index):
        issue = self.issues[index]
        options = ["Solved", "Under Review", "No Action Taken"]

        new_status = simpledialog.askstring("Update Status",
                                            f"Current: {issue['status']}\nNew status ({'/'.join(options)}):")
        if new_status and new_status in options:
            comment = simpledialog.askstring("Add Note", "What was done to solve or review this?")
            if comment:
                issue['status'] = new_status
                issue['desc'] = comment
                if new_status == "Solved":
                    self.canvas.delete(issue['marker'])
                    self.issues.pop(index)
                self.save_all_issues()
                messagebox.showinfo("Updated", "Issue status updated.")

    def save_all_issues(self):
        with open(DB_FILE, 'w') as f:
            for issue in self.issues:
                f.write(f"2025-04-02 | {issue['x']},{issue['y']} | {issue['type']} | {issue['desc']} | Status: {issue['status']}\n")

    def handle_official_click(self, event):
        pass
