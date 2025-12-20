import tkinter as tk
from tkinter import ttk, messagebox
from ui.components.widgets import create_button, create_label, create_entry

class LoginPage:
    def __init__(self, parent, on_login, on_back):
        self.parent = parent
        self.on_login = on_login
        self.on_back = on_back
        self.setup_styles()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")  # nicer theme than default
        style.configure("TFrame", background="#f0f0f0")
        style.configure("Header.TLabel", font=("Helvetica", 20, "bold"), foreground="#333", background="#f0f0f0")
        style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
        style.configure("TButton", font=("Helvetica", 12), padding=5)
        style.configure("Accent.TButton", font=("Helvetica", 12, "bold"), background="#4CAF50", foreground="white")
        style.map("Accent.TButton",
                  background=[("active", "#45a049")],
                  foreground=[("active", "white")])

    def render(self):
        self.clear_frame()

        # Center frame
        login_card = ttk.Frame(self.parent, style="TFrame", padding=30, relief="ridge")
        login_card.place(relx=0.5, rely=0.5, anchor="center")

        create_label(login_card, "Login to Testly", style="Header.TLabel").pack(pady=(0, 20))

        username = tk.StringVar()
        password = tk.StringVar()

        create_label(login_card, "Username").pack(anchor="w")
        create_entry(login_card, textvariable=username).pack(fill="x", pady=5)

        create_label(login_card, "Password").pack(anchor="w")
        create_entry(login_card, textvariable=password, show="*").pack(fill="x", pady=5)

        create_button(login_card, "Login", lambda: self.handle_login(username.get(), password.get()), style="Accent.TButton").pack(fill="x", pady=(15, 5))
        create_button(login_card, "Back", self.on_back, style="TButton").pack(fill="x")

    def handle_login(self, username, password):
        if username and password:
            self.on_login(username, password)
        else:
            messagebox.showwarning("Login Failed", "Please enter both username and password.")

    def clear_frame(self):
        for widget in self.parent.winfo_children():
            widget.destroy()



# """
# This module contains the UI for the login page of the Testly application.
# """

# import tkinter as tk
# from tkinter import ttk, messagebox
# from ui.components.widgets import create_button, create_label, create_entry

# class LoginPage:
#     def __init__(self, parent, on_login, on_back):
#         self.parent = parent
#         self.on_login = on_login
#         self.on_back = on_back

#     def render(self):
#         self.clear_frame()
#         login_card = ttk.Frame(self.parent, style="TFrame")
#         login_card.pack(pady=50, padx=20, ipadx=20, ipady=20)

#         create_label(login_card, "Login to Testly", style="Header.TLabel").pack(pady=10)
#         username = tk.StringVar()
#         password = tk.StringVar()
#         create_label(login_card, "Username").pack()
#         create_entry(login_card, textvariable=username).pack(pady=5)
#         create_label(login_card, "Password").pack()
#         create_entry(login_card, textvariable=password, show="*").pack(pady=5)
#         create_button(login_card, "Login", lambda: self.on_login(username.get(), password.get()), style="Accent.TButton").pack(pady=10)
#         create_button(login_card, "Back", self.on_back, style="TButton").pack()

#     def clear_frame(self):
#         for widget in self.parent.winfo_children():
#             widget.destroy()