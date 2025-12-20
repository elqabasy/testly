import tkinter as tk
from tkinter import ttk
from ui.components.widgets import create_button, create_label

class AdminDashboard:
    def __init__(self, parent, add_student_callback, add_question_callback, view_results_callback, back_callback):
        self.parent = parent
        self.add_student_callback = add_student_callback
        self.add_question_callback = add_question_callback
        self.view_results_callback = view_results_callback
        self.back_callback = back_callback

    def render(self):
        self.clear_frame()

        # Main container frame
        container = ttk.Frame(self.parent)
        container.pack(fill="both", expand=True)

        # Sidebar
        sidebar = ttk.Frame(container, style="Sidebar.TFrame", width=200)
        sidebar.pack(side="left", fill="y")

        # Sidebar buttons
        self.create_sidebar_button(sidebar, "Add Student", self.add_student_callback, 0)
        self.create_sidebar_button(sidebar, "Add Question", self.add_question_callback, 1)
        self.create_sidebar_button(sidebar, "View Results", self.view_results_callback, 2)
        self.create_sidebar_button(sidebar, "Back to Home", self.back_callback, 3, accent=False)

        # Content area
        self.content_area = ttk.Frame(container, style="TFrame")
        self.content_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Welcome message
        create_label(self.content_area, "Admin Dashboard", style="Header.TLabel").pack(pady=(0, 20))
        create_label(self.content_area, "Select an action from the sidebar.", style="TLabel").pack(pady=10)

    def create_sidebar_button(self, parent, text, command, row, accent=True):
        style = "Accent.TButton" if accent else "TButton"
        btn = create_button(parent, text, command, style=style)
        btn.pack(fill="x", pady=10, padx=10)
        # Optional hover effect
        btn.bind("<Enter>", lambda e: btn.configure(cursor="hand2"))
        btn.bind("<Leave>", lambda e: btn.configure(cursor=""))

    def clear_frame(self):
        for widget in self.parent.winfo_children():
            widget.destroy()



# """
# This module contains the UI for the admin dashboard of the Testly application.
# """

# from ui.components.widgets import create_button, create_label

# class AdminDashboard:
#     def __init__(self, parent, on_add_student, on_add_question, on_view_results, on_logout):
#         self.parent = parent
#         self.on_add_student = on_add_student
#         self.on_add_question = on_add_question
#         self.on_view_results = on_view_results
#         self.on_logout = on_logout

#     def render(self):
#         self.clear_frame()
#         create_label(self.parent, "Admin Dashboard", style="Header.TLabel").pack(pady=10)
#         create_button(self.parent, "Add Student", self.on_add_student, style="Accent.TButton").pack(pady=5)
#         create_button(self.parent, "Add Question", self.on_add_question, style="Accent.TButton").pack(pady=5)
#         create_button(self.parent, "View Results", self.on_view_results, style="Accent.TButton").pack(pady=5)
#         create_button(self.parent, "Logout", self.on_logout, style="TButton").pack(pady=5)

#     def clear_frame(self):
#         for widget in self.parent.winfo_children():
#             widget.destroy()