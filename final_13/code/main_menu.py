import tkinter as tk
from map_window import MapReportingWindow
from call_window import CallLookupWindow

class MainMenu:
    def __init__(self, role="resident"):
        self.role = role
        self.window = tk.Tk()
        self.window.title("Cypress Main Menu")

        tk.Label(self.window, text=f"Logged in as: {self.role.title()}", font=("Arial", 12, "italic"), fg="gray").pack(pady=5)

        if self.role == "resident":
            tk.Label(self.window, text="How would you like to report an issue?", font=("Arial", 16, "bold")).pack(pady=20)

            tk.Button(self.window, text="🗺️ Report via Map", width=30, height=2, bg="lightblue",
                      command=self.open_map_window).pack(pady=10)

            tk.Button(self.window, text="📞 Report via Call", width=30, height=2, bg="lightgreen",
                      command=self.open_call_window).pack(pady=10)
        else:
            tk.Label(self.window, text="Manage Reported Issues", font=("Arial", 16, "bold")).pack(pady=20)

            tk.Button(self.window, text="🛠️ View Issues on Map", width=30, height=2, bg="lightblue",
                      command=self.open_map_window).pack(pady=10)

        tk.Button(self.window, text="Exit", command=self.window.destroy, bg="lightgray", width=30, height=2).pack(pady=20)

        self.window.mainloop()

    def open_map_window(self):
        MapReportingWindow(tk.Toplevel(self.window), role=self.role)

    def open_call_window(self):
        CallLookupWindow(tk.Toplevel(self.window))
