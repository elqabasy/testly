"""
This module contains the UI components for the Testly application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from logic.exam_engine import ExamEngine

class TestlyApp:
    def __init__(self, root):
        self.root = root
        self.engine = ExamEngine()
        self.current_student = None
        self.exam_questions = []
        self.current_score = 0
        self.current_index = 0
        self.timer_id = None
        self.time_left = 0

        self.setup_ui()

    def setup_ui(self):
        self.root.title("Testly - Smart Exam System")
        self.root.geometry("750x520")
        self.root.configure(bg="#F5F7FB")

        style = ttk.Style(self.root)
        style.theme_use("clam")

        # Branding and Colors
        style.configure("TFrame", background="#F5F7FB")
        style.configure("TLabel", background="#F5F7FB", foreground="#111827", font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground="#2563EB", background="#F5F7FB")
        style.configure("TButton", font=("Segoe UI", 11), padding=8)
        style.configure("Accent.TButton", background="#2563EB", foreground="white", font=("Segoe UI", 11, "bold"), padding=10, borderwidth=0)
        style.map("Accent.TButton", background=[("active", "#1D4ED8")])
        style.configure("Sidebar.TFrame", background="#111827")
        style.configure("Sidebar.TLabel", background="#111827", foreground="#E5E7EB", font=("Segoe UI", 15, "bold"))
        style.configure("Horizontal.TProgressbar", troughcolor="#E5E7EB", background="#2563EB", thickness=8)

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        self.show_home()

    def show_home(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="Welcome to Testly", style="Header.TLabel").pack(pady=20)
        ttk.Button(self.main_frame, text="Admin Login", style="Accent.TButton", command=self.show_admin_login).pack(pady=10)
        ttk.Button(self.main_frame, text="Student Login", style="Accent.TButton", command=self.show_student_login).pack(pady=10)
        ttk.Button(self.main_frame, text="Exit", style="TButton", command=self.root.destroy).pack(pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_admin_login(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="Admin Login", font=("Segoe UI", 16)).pack(pady=10)
        username = tk.StringVar()
        password = tk.StringVar()
        ttk.Label(self.main_frame, text="Username").pack()
        ttk.Entry(self.main_frame, textvariable=username).pack()
        ttk.Label(self.main_frame, text="Password").pack()
        ttk.Entry(self.main_frame, textvariable=password, show="*").pack()
        ttk.Button(self.main_frame, text="Login", command=lambda: self.admin_login(username.get(), password.get())).pack(pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.show_home).pack()

    def admin_login(self, username, password):
        if username == "admin" and password == "1234":
            self.show_admin_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def show_admin_dashboard(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="Admin Dashboard", font=("Segoe UI", 16)).pack(pady=10)
        ttk.Button(self.main_frame, text="Add Student", command=self.show_add_student).pack(pady=5)
        ttk.Button(self.main_frame, text="Add Question", command=self.show_add_question).pack(pady=5)
        ttk.Button(self.main_frame, text="View Results", command=self.show_results).pack(pady=5)
        ttk.Button(self.main_frame, text="Logout", command=self.show_home).pack(pady=5)

    def show_add_student(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="Add Student", font=("Segoe UI", 16)).pack(pady=10)
        student_id = tk.StringVar()
        student_name = tk.StringVar()
        ttk.Label(self.main_frame, text="Student ID").pack()
        ttk.Entry(self.main_frame, textvariable=student_id).pack()
        ttk.Label(self.main_frame, text="Student Name").pack()
        ttk.Entry(self.main_frame, textvariable=student_name).pack()
        ttk.Button(self.main_frame, text="Save", command=lambda: self.add_student(student_id.get(), student_name.get())).pack(pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.show_admin_dashboard).pack()

    def add_student(self, student_id, student_name):
        try:
            self.engine.add_student(student_id, student_name)
            messagebox.showinfo("Success", "Student added successfully")
            self.show_admin_dashboard()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_add_question(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="Add Question", font=("Segoe UI", 16)).pack(pady=10)
        question = tk.StringVar()
        options = {opt: tk.StringVar() for opt in "ABCD"}
        correct = tk.StringVar()
        ttk.Label(self.main_frame, text="Question").pack()
        ttk.Entry(self.main_frame, textvariable=question).pack()
        for opt in "ABCD":
            ttk.Label(self.main_frame, text=f"Option {opt}").pack()
            ttk.Entry(self.main_frame, textvariable=options[opt]).pack()
        ttk.Label(self.main_frame, text="Correct Option (A/B/C/D)").pack()
        ttk.Entry(self.main_frame, textvariable=correct).pack()
        ttk.Button(self.main_frame, text="Save", command=lambda: self.add_question(question.get(), {k: v.get() for k, v in options.items()}, correct.get())).pack(pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.show_admin_dashboard).pack()

    def add_question(self, question, options, correct):
        try:
            self.engine.add_question(question, options, correct)
            messagebox.showinfo("Success", "Question added successfully")
            self.show_admin_dashboard()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_results(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="Results", font=("Segoe UI", 16)).pack(pady=10)
        results = self.engine.results
        if not results:
            ttk.Label(self.main_frame, text="No results available").pack()
        else:
            for result in results:
                ttk.Label(self.main_frame, text=f"{result.student_id} | {result.student_name} | {result.score}/{result.total} | {result.percent:.2f}% | {result.status}").pack()
        ttk.Button(self.main_frame, text="Back", command=self.show_admin_dashboard).pack()

    def show_student_login(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="Student Login", font=("Segoe UI", 16)).pack(pady=10)
        student_id = tk.StringVar()
        ttk.Label(self.main_frame, text="Student ID").pack()
        ttk.Entry(self.main_frame, textvariable=student_id).pack()
        ttk.Button(self.main_frame, text="Login", command=lambda: self.student_login(student_id.get())).pack(pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.show_home).pack()

    def student_login(self, student_id):
        """Handle student login by verifying their ID."""
        student = self.engine.find_student(student_id)
        if not student:
            messagebox.showerror("Error", "Student not found")
            return
        self.current_student = student
        self.show_student_dashboard()

    def show_student_dashboard(self):
        """Display the student dashboard after successful login."""
        self.clear_frame()
        ttk.Label(self.main_frame, text=f"Welcome, {self.current_student.name}", style="Header.TLabel").pack(pady=20)
        ttk.Button(self.main_frame, text="Take Exam", style="Accent.TButton", command=self.start_exam).pack(pady=10)
        ttk.Button(self.main_frame, text="View Results", style="Accent.TButton", command=self.show_results).pack(pady=10)
        ttk.Button(self.main_frame, text="Logout", style="TButton", command=self.show_home).pack(pady=10)

    def start_exam(self):
        """Start the exam for the currently logged-in student."""
        if not self.current_student:
            messagebox.showerror("Error", "No student is currently logged in.")
            return

        try:
            self.exam_questions = self.engine.start_exam(self.current_student.id, 5)  # Example: 5 questions per exam
            self.current_score = 0
            self.current_index = 0
            self.show_next_question()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_next_question(self):
        if self.current_index >= len(self.exam_questions):
            self.finish_exam()
            return

        question = self.exam_questions[self.current_index]
        self.current_index += 1

        # Display question in UI
        ttk.Label(self.main_frame, text=question.text, font=("Segoe UI", 14)).pack(pady=10)
        for opt in "ABCD":
            ttk.Radiobutton(self.main_frame, text=question.options[opt], variable=self.answer_var, value=opt).pack(anchor="w")
        ttk.Button(self.main_frame, text="Next", command=self.submit_answer).pack(pady=10)

    def submit_answer(self):
        selected_option = self.answer_var.get()
        correct_option = self.exam_questions[self.current_index - 1].correct
        if selected_option == correct_option:
            self.current_score += 1
        self.show_next_question()

    def finish_exam(self):
        self.engine.save_result(
            self.current_student.id,
            self.current_student.name,
            self.current_score,
            len(self.exam_questions)
        )
        messagebox.showinfo("Exam Finished", "Your results have been saved.")
        self.show_home()

if __name__ == "__main__":
    root = tk.Tk()
    app = TestlyApp(root)
    root.mainloop()