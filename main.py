import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime

# ================== DATA (SESSION ONLY) ==================
students = []
questions = []
results = []

ADMIN_USER = "admin"
ADMIN_PASS = "1234"

EXAM_DURATION_SECONDS = 60
QUESTIONS_PER_EXAM = 5

current_student = None
current_questions = []
current_score = 0
current_total = 0
question_index = 0
exam_running = False
exam_time_left = 0
timer_after_id = None

# ================== HELPERS ==================
def safe(s): return (s or "").strip()
def clean(s): return safe(s).replace("|", "/").replace(",", " ")
def now(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ================== CORE ==================
root = tk.Tk()
root.title("Smart Exam System")
root.state('zoomed')  # Fullscreen / maximized
root.configure(bg="#e6f0ff")  # Light blue background

style = ttk.Style(root)
style.theme_use("clam")

# Global Styles
style.configure("TFrame", background="#e6f0ff")
style.configure("Sidebar.TFrame", background="#0047b3")
style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), background="#e6f0ff")
style.configure("Card.TFrame", background="white", relief="raised", borderwidth=1)
style.configure("CardTitle.TLabel", font=("Segoe UI", 14, "bold"), background="white")
style.configure("Accent.TButton", background="#1e40af", foreground="white", font=("Segoe UI", 11, "bold"), padding=8)
style.map("Accent.TButton", background=[("active", "#1d4ed8")])
style.configure("Horizontal.TProgressbar", thickness=8)

main = ttk.Frame(root)
main.pack(fill="both", expand=True)

# ================== LAYOUT ==================
def clear():
    for w in main.winfo_children():
        w.destroy()

def layout(title, sidebar=None):
    clear()
    wrapper = ttk.Frame(main)
    wrapper.pack(fill="both", expand=True)

    if sidebar:
        sb = ttk.Frame(wrapper, style="Sidebar.TFrame", width=220)
        sb.pack(side="left", fill="y")
        ttk.Label(sb, text="SMART EXAM", font=("Segoe UI", 18, "bold"),
                  foreground="white", background="#0047b3").pack(pady=30)
        for t, c in sidebar:
            btn = ttk.Button(sb, text=t, command=c, style="Accent.TButton")
            btn.pack(fill="x", padx=15, pady=6)

    content = ttk.Frame(wrapper, padding=25)
    content.pack(side="right", fill="both", expand=True)

    # Center wrapper
    center_wrapper = ttk.Frame(content)
    center_wrapper.place(relx=0.5, rely=0.5, anchor='center')
    ttk.Label(center_wrapper, text=title, style="Header.TLabel").pack(anchor="center", pady=(0, 25))

    return center_wrapper

# ================== HOME ==================
def home():
    content = layout("Welcome")
    card = ttk.Frame(content, style="Card.TFrame", padding=40)
    card.pack()
    ttk.Button(card, text="Admin Login", width=25, style="Accent.TButton", command=admin_login).pack(pady=10)
    ttk.Button(card, text="Student Login", width=25, style="Accent.TButton", command=student_login).pack(pady=10)
    ttk.Button(card, text="Exit", width=25, style="Accent.TButton", command=root.destroy).pack(pady=10)

# ================== ADMIN ==================
def admin_login():
    content = layout("Admin Login")
    card = ttk.Frame(content, style="Card.TFrame", padding=30)
    card.pack()

    u, p = tk.StringVar(), tk.StringVar()

    for lbl, var, sec in [("Username", u, False), ("Password", p, True)]:
        row = ttk.Frame(card)
        row.pack(fill="x", pady=8)
        ttk.Label(row, text=lbl, width=12).pack(side="left")
        ttk.Entry(row, textvariable=var, show="*" if sec else "").pack(fill="x", expand=True)

    def check():
        if safe(u.get()) == ADMIN_USER and safe(p.get()) == ADMIN_PASS:
            admin_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    ttk.Button(card, text="Login", style="Accent.TButton", command=check).pack(pady=15)

def admin_menu():
    content = layout(
        "Admin Dashboard",
        [("Add Student", add_student),
         ("Add Question", add_question),
         ("View Results", view_results),
         ("Logout", home)]
    )
    ttk.Label(content, text="Manage students, questions, and results.", font=("Segoe UI", 12)).pack(anchor="w")

def add_student():
    content = layout("Add Student", [("Back", admin_menu)])
    card = ttk.Frame(content, style="Card.TFrame", padding=30)
    card.pack()

    sid, name = tk.StringVar(), tk.StringVar()

    for lbl, var in [("Student ID", sid), ("Student Name", name)]:
        row = ttk.Frame(card)
        row.pack(fill="x", pady=10)
        ttk.Label(row, text=lbl, width=15).pack(side="left")
        ttk.Entry(row, textvariable=var).pack(fill="x", expand=True)

    def save():
        if not safe(sid.get()) or not safe(name.get()):
            messagebox.showerror("Error", "All fields required")
            return
        students.append({"Id": safe(sid.get()), "Name": clean(name.get())})
        messagebox.showinfo("Saved", "Student added")
        admin_menu()

    ttk.Button(card, text="Save Student", style="Accent.TButton", command=save).pack(anchor="e", pady=15)

def add_question():
    content = layout("Add Question", [("Back", admin_menu)])
    card = ttk.Frame(content, style="Card.TFrame", padding=25)
    card.pack()

    fields = ["Question", "A", "B", "C", "D", "Correct (A/B/C/D)"]
    vars_ = [tk.StringVar() for _ in fields]

    for lbl, var in zip(fields, vars_):
        row = ttk.Frame(card)
        row.pack(fill="x", pady=6)
        ttk.Label(row, text=lbl, width=20).pack(side="left")
        ttk.Entry(row, textvariable=var).pack(fill="x", expand=True)

    def save():
        if not all(safe(v.get()) for v in vars_):
            messagebox.showerror("Error", "All fields required")
            return
        questions.append({
            "q": clean(vars_[0].get()),
            "A": clean(vars_[1].get()),
            "B": clean(vars_[2].get()),
            "C": clean(vars_[3].get()),
            "D": clean(vars_[4].get()),
            "correct": safe(vars_[5].get()).upper()
        })
        messagebox.showinfo("Saved", "Question added")
        admin_menu()

    ttk.Button(card, text="Save Question", style="Accent.TButton", command=save).pack(anchor="e", pady=15)

def view_results():
    content = layout("Results", [("Back", admin_menu)])
    for r in results:
        card = ttk.Frame(content, style="Card.TFrame", padding=15)
        card.pack(pady=6)
        ttk.Label(card, text=f"{r['Name']} ({r['Id']})", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text=f"Score: {r['Score']}/{r['Total']} | {r['Percent']}% | {r['Status']} | {r['Date']}").pack(anchor="w")

# ================== STUDENT ==================
def student_login():
    content = layout("Student Login")
    card = ttk.Frame(content, style="Card.TFrame", padding=40)
    card.pack()

    sid = tk.StringVar()
    ttk.Entry(card, textvariable=sid, width=35, font=("Segoe UI", 11)).pack(pady=15)

    def login():
        global current_student
        for s in students:
            if s["Id"] == safe(sid.get()):
                current_student = s
                student_menu()
                return
        messagebox.showerror("Error", "Student not found")

    ttk.Button(card, text="Login", style="Accent.TButton", command=login).pack(pady=10)

def student_menu():
    content = layout(
        f"Welcome, {current_student['Name']}",
        [("Take Exam", start_exam),
         ("My Result", my_result),
         ("Logout", home)]
    )

def my_result():
    content = layout("My Result", [("Back", student_menu)])
    found = False
    for r in results:
        if r["Id"] == current_student["Id"]:
            found = True
            card = ttk.Frame(content, style="Card.TFrame", padding=25)
            card.pack(pady=10)
            for k, v in r.items():
                ttk.Label(card, text=f"{k}: {v}", font=("Segoe UI", 11)).pack(anchor="w")
    if not found:
        ttk.Label(content, text="No results found.", font=("Segoe UI", 12)).pack(anchor="w", pady=20)

# ================== EXAM ==================
def start_exam():
    global current_questions, current_score, current_total, question_index, exam_running, exam_time_left

    current_questions = random.sample(questions, min(QUESTIONS_PER_EXAM, len(questions)))
    current_score = 0
    current_total = len(current_questions)
    question_index = 0
    exam_time_left = EXAM_DURATION_SECONDS
    exam_running = True

    content = layout("Exam In Progress")
    timer = ttk.Label(content, font=("Segoe UI", 12, "bold"), foreground="red", background="#e6f0ff")
    timer.pack(anchor="e")

    progress = ttk.Progressbar(content, maximum=current_total)
    progress.pack(fill="x", pady=12)

    card = ttk.Frame(content, style="Card.TFrame", padding=25)
    card.pack(pady=20)

    question_lbl = ttk.Label(card, font=("Segoe UI", 14, "bold"), wraplength=700)
    question_lbl.pack(anchor="w", pady=10)

    var = tk.StringVar()
    radios = []

    for _ in range(4):
        rb = ttk.Radiobutton(card, variable=var, style="TRadiobutton")
        rb.pack(anchor="w", pady=6)
        radios.append(rb)

    def update():
        nonlocal question_lbl
        q = current_questions[question_index]
        question_lbl.config(text=q["q"])
        for rb, k in zip(radios, ["A", "B", "C", "D"]):
            rb.config(text=f"{k}) {q[k]}", value=k)
        progress["value"] = question_index + 1
        var.set("")

    def submit():
        global current_score, question_index
        if var.get() == current_questions[question_index]["correct"]:
            current_score += 1
        question_index += 1
        if question_index >= current_total:
            finish_exam()
        else:
            update()

    ttk.Button(card, text="Next", style="Accent.TButton", command=submit).pack(anchor="e", pady=15)
    update()

def finish_exam():
    results.append({
        "Id": current_student["Id"],
        "Name": current_student["Name"],
        "Score": current_score,
        "Total": current_total,
        "Percent": f"{(current_score/current_total)*100:.2f}",
        "Status": "Pass" if current_score/current_total >= 0.5 else "Fail",
        "Date": now()
    })
    messagebox.showinfo("Finished", "Exam completed")
    student_menu()

# ================== START ==================
home()
root.mainloop()


# import tkinter as tk
# from tkinter import ttk, messagebox
# import random
# from datetime import datetime

# # ================== DATA (SESSION ONLY) ==================
# students = []
# questions = []
# results = []

# ADMIN_USER = "admin"
# ADMIN_PASS = "1234"

# EXAM_DURATION_SECONDS = 60
# QUESTIONS_PER_EXAM = 5

# current_student = None
# current_questions = []
# current_score = 0
# current_total = 0
# question_index = 0
# exam_running = False
# exam_time_left = 0
# timer_after_id = None

# # ================== HELPERS ==================
# def safe(s): return (s or "").strip()
# def clean(s): return safe(s).replace("|", "/").replace(",", " ")
# def now(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# # ================== CORE ==================
# root = tk.Tk()
# root.title("Smart Exam System")
# root.geometry("950x600")
# root.configure(bg="#e6f0ff")  # Light blue background

# style = ttk.Style(root)
# style.theme_use("clam")

# # Global Styles
# style.configure("TFrame", background="#e6f0ff")
# style.configure("Sidebar.TFrame", background="#0047b3")  # Dark blue sidebar
# style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), background="#e6f0ff")
# style.configure("Card.TFrame", background="white", relief="raised", borderwidth=1)
# style.configure("CardTitle.TLabel", font=("Segoe UI", 14, "bold"), background="white")
# style.configure("Accent.TButton", background="#1e40af", foreground="white", font=("Segoe UI", 11, "bold"), padding=8)
# style.map("Accent.TButton", background=[("active", "#1d4ed8")])
# style.configure("Horizontal.TProgressbar", thickness=8)

# main = ttk.Frame(root)
# main.pack(fill="both", expand=True)

# # ================== LAYOUT ==================
# def clear():
#     for w in main.winfo_children():
#         w.destroy()

# def layout(title, sidebar=None):
#     clear()
#     wrapper = ttk.Frame(main)
#     wrapper.pack(fill="both", expand=True)

#     if sidebar:
#         sb = ttk.Frame(wrapper, style="Sidebar.TFrame", width=220)
#         sb.pack(side="left", fill="y")
#         ttk.Label(sb, text="SMART EXAM", font=("Segoe UI", 18, "bold"),
#                   foreground="white", background="#0047b3").pack(pady=30)
#         for t, c in sidebar:
#             btn = ttk.Button(sb, text=t, command=c, style="Accent.TButton")
#             btn.pack(fill="x", padx=15, pady=6)

#     content = ttk.Frame(wrapper, padding=25)
#     content.pack(side="right", fill="both", expand=True)
#     ttk.Label(content, text=title, style="Header.TLabel").pack(anchor="w", pady=(0, 25))
#     return content

# # ================== HOME ==================
# def home():
#     content = layout("Welcome")
#     card = ttk.Frame(content, style="Card.TFrame", padding=40)
#     card.pack(pady=100)
#     ttk.Button(card, text="Admin Login", width=25, style="Accent.TButton", command=admin_login).pack(pady=10)
#     ttk.Button(card, text="Student Login", width=25, style="Accent.TButton", command=student_login).pack(pady=10)
#     ttk.Button(card, text="Exit", width=25, style="Accent.TButton", command=root.destroy).pack(pady=10)

# # ================== ADMIN ==================
# def admin_login():
#     content = layout("Admin Login")
#     card = ttk.Frame(content, style="Card.TFrame", padding=30)
#     card.pack(pady=60)

#     u, p = tk.StringVar(), tk.StringVar()

#     for lbl, var, sec in [("Username", u, False), ("Password", p, True)]:
#         row = ttk.Frame(card)
#         row.pack(fill="x", pady=8)
#         ttk.Label(row, text=lbl, width=12).pack(side="left")
#         ttk.Entry(row, textvariable=var, show="*" if sec else "").pack(fill="x", expand=True)

#     def check():
#         if safe(u.get()) == ADMIN_USER and safe(p.get()) == ADMIN_PASS:
#             admin_menu()
#         else:
#             messagebox.showerror("Error", "Invalid credentials")

#     ttk.Button(card, text="Login", style="Accent.TButton", command=check).pack(pady=15)

# def admin_menu():
#     content = layout(
#         "Admin Dashboard",
#         [("Add Student", add_student),
#          ("Add Question", add_question),
#          ("View Results", view_results),
#          ("Logout", home)]
#     )
#     ttk.Label(content, text="Manage students, questions, and results.", font=("Segoe UI", 12)).pack(anchor="w")

# def add_student():
#     content = layout("Add Student", [("Back", admin_menu)])
#     card = ttk.Frame(content, style="Card.TFrame", padding=30)
#     card.pack(fill="x")

#     sid, name = tk.StringVar(), tk.StringVar()

#     for lbl, var in [("Student ID", sid), ("Student Name", name)]:
#         row = ttk.Frame(card)
#         row.pack(fill="x", pady=10)
#         ttk.Label(row, text=lbl, width=15).pack(side="left")
#         ttk.Entry(row, textvariable=var).pack(fill="x", expand=True)

#     def save():
#         if not safe(sid.get()) or not safe(name.get()):
#             messagebox.showerror("Error", "All fields required")
#             return
#         students.append({"Id": safe(sid.get()), "Name": clean(name.get())})
#         messagebox.showinfo("Saved", "Student added")
#         admin_menu()

#     ttk.Button(card, text="Save Student", style="Accent.TButton", command=save).pack(anchor="e", pady=15)

# def add_question():
#     content = layout("Add Question", [("Back", admin_menu)])
#     card = ttk.Frame(content, style="Card.TFrame", padding=25)
#     card.pack(fill="x")

#     fields = ["Question", "A", "B", "C", "D", "Correct (A/B/C/D)"]
#     vars_ = [tk.StringVar() for _ in fields]

#     for lbl, var in zip(fields, vars_):
#         row = ttk.Frame(card)
#         row.pack(fill="x", pady=6)
#         ttk.Label(row, text=lbl, width=20).pack(side="left")
#         ttk.Entry(row, textvariable=var).pack(fill="x", expand=True)

#     def save():
#         if not all(safe(v.get()) for v in vars_):
#             messagebox.showerror("Error", "All fields required")
#             return
#         questions.append({
#             "q": clean(vars_[0].get()),
#             "A": clean(vars_[1].get()),
#             "B": clean(vars_[2].get()),
#             "C": clean(vars_[3].get()),
#             "D": clean(vars_[4].get()),
#             "correct": safe(vars_[5].get()).upper()
#         })
#         messagebox.showinfo("Saved", "Question added")
#         admin_menu()

#     ttk.Button(card, text="Save Question", style="Accent.TButton", command=save).pack(anchor="e", pady=15)

# def view_results():
#     content = layout("Results", [("Back", admin_menu)])
#     for r in results:
#         card = ttk.Frame(content, style="Card.TFrame", padding=15)
#         card.pack(fill="x", pady=6)
#         ttk.Label(card, text=f"{r['Name']} ({r['Id']})", style="CardTitle.TLabel").pack(anchor="w")
#         ttk.Label(card, text=f"Score: {r['Score']}/{r['Total']} | {r['Percent']}% | {r['Status']} | {r['Date']}").pack(anchor="w")

# # ================== STUDENT ==================
# def student_login():
#     content = layout("Student Login")
#     card = ttk.Frame(content, style="Card.TFrame", padding=40)
#     card.pack(pady=80)

#     sid = tk.StringVar()
#     ttk.Entry(card, textvariable=sid, width=35, font=("Segoe UI", 11)).pack(pady=15)

#     def login():
#         global current_student
#         for s in students:
#             if s["Id"] == safe(sid.get()):
#                 current_student = s
#                 student_menu()
#                 return
#         messagebox.showerror("Error", "Student not found")

#     ttk.Button(card, text="Login", style="Accent.TButton", command=login).pack(pady=10)

# def student_menu():
#     content = layout(
#         f"Welcome, {current_student['Name']}",
#         [("Take Exam", start_exam),
#          ("My Result", my_result),
#          ("Logout", home)]
#     )

# def my_result():
#     content = layout("My Result", [("Back", student_menu)])
#     found = False
#     for r in results:
#         if r["Id"] == current_student["Id"]:
#             found = True
#             card = ttk.Frame(content, style="Card.TFrame", padding=25)
#             card.pack(pady=10)
#             for k, v in r.items():
#                 ttk.Label(card, text=f"{k}: {v}", font=("Segoe UI", 11)).pack(anchor="w")
#     if not found:
#         ttk.Label(content, text="No results found.", font=("Segoe UI", 12)).pack(anchor="w", pady=20)

# # ================== EXAM ==================
# def start_exam():
#     global current_questions, current_score, current_total, question_index, exam_running, exam_time_left

#     current_questions = random.sample(questions, min(QUESTIONS_PER_EXAM, len(questions)))
#     current_score = 0
#     current_total = len(current_questions)
#     question_index = 0
#     exam_time_left = EXAM_DURATION_SECONDS
#     exam_running = True

#     content = layout("Exam In Progress")
#     timer = ttk.Label(content, font=("Segoe UI", 12, "bold"), foreground="red", background="#e6f0ff")
#     timer.pack(anchor="e")

#     progress = ttk.Progressbar(content, maximum=current_total)
#     progress.pack(fill="x", pady=12)

#     card = ttk.Frame(content, style="Card.TFrame", padding=25)
#     card.pack(fill="x", pady=20)

#     question_lbl = ttk.Label(card, font=("Segoe UI", 14, "bold"), wraplength=700)
#     question_lbl.pack(anchor="w", pady=10)

#     var = tk.StringVar()
#     radios = []

#     for _ in range(4):
#         rb = ttk.Radiobutton(card, variable=var, style="TRadiobutton")
#         rb.pack(anchor="w", pady=6)
#         radios.append(rb)

#     def update():
#         nonlocal question_lbl
#         q = current_questions[question_index]
#         question_lbl.config(text=q["q"])
#         for rb, k in zip(radios, ["A", "B", "C", "D"]):
#             rb.config(text=f"{k}) {q[k]}", value=k)
#         progress["value"] = question_index + 1
#         var.set("")

#     def submit():
#         global current_score, question_index
#         if var.get() == current_questions[question_index]["correct"]:
#             current_score += 1
#         question_index += 1
#         if question_index >= current_total:
#             finish_exam()
#         else:
#             update()

#     ttk.Button(card, text="Next", style="Accent.TButton", command=submit).pack(anchor="e", pady=15)
#     update()

# def finish_exam():
#     results.append({
#         "Id": current_student["Id"],
#         "Name": current_student["Name"],
#         "Score": current_score,
#         "Total": current_total,
#         "Percent": f"{(current_score/current_total)*100:.2f}",
#         "Status": "Pass" if current_score/current_total >= 0.5 else "Fail",
#         "Date": now()
#     })
#     messagebox.showinfo("Finished", "Exam completed")
#     student_menu()

# # ================== START ==================
# home()
# root.mainloop()



# import tkinter as tk
# from tkinter import ttk, messagebox
# import random
# from datetime import datetime

# # ================== DATA (SESSION ONLY) ==================
# students = []
# questions = []
# results = []

# ADMIN_USER = "admin"
# ADMIN_PASS = "1234"

# EXAM_DURATION_SECONDS = 60
# QUESTIONS_PER_EXAM = 5

# current_student = None
# current_questions = []
# current_score = 0
# current_total = 0
# question_index = 0
# exam_running = False
# exam_time_left = 0
# timer_after_id = None

# # ================== HELPERS ==================
# def safe(s): return (s or "").strip()
# def clean(s): return safe(s).replace("|", "/").replace(",", " ")
# def now(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# # ================== CORE ==================
# root = tk.Tk()
# root.title("Smart Exam System")
# root.geometry("900x580")
# root.configure(bg="#f5f7fb")

# style = ttk.Style(root)
# style.theme_use("clam")

# style.configure("TFrame", background="#f5f7fb")
# style.configure("Sidebar.TFrame", background="#111827")
# style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"))
# style.configure("Card.TFrame", background="white", relief="solid", borderwidth=1)
# style.configure("CardTitle.TLabel", font=("Segoe UI", 13, "bold"), background="white")
# style.configure("Accent.TButton", background="#2563eb", foreground="white", font=("Segoe UI", 11, "bold"), padding=10)
# style.map("Accent.TButton", background=[("active", "#1d4ed8")])
# style.configure("Horizontal.TProgressbar", thickness=6)

# main = ttk.Frame(root)
# main.pack(fill="both", expand=True)

# # ================== LAYOUT ==================
# def clear():
#     for w in main.winfo_children():
#         w.destroy()

# def layout(title, sidebar=None):
#     clear()
#     wrapper = ttk.Frame(main)
#     wrapper.pack(fill="both", expand=True)

#     if sidebar:
#         sb = ttk.Frame(wrapper, style="Sidebar.TFrame", width=220)
#         sb.pack(side="left", fill="y")
#         ttk.Label(sb, text="SMART EXAM", font=("Segoe UI", 16, "bold"),
#                   foreground="#e5e7eb", background="#111827").pack(pady=25)
#         for t, c in sidebar:
#             ttk.Button(sb, text=t, command=c).pack(fill="x", padx=15, pady=6)

#     content = ttk.Frame(wrapper, padding=25)
#     content.pack(side="right", fill="both", expand=True)
#     ttk.Label(content, text=title, style="Header.TLabel").pack(anchor="w", pady=(0, 20))
#     return content

# # ================== HOME ==================
# def home():
#     content = layout("Welcome")
#     card = ttk.Frame(content, style="Card.TFrame", padding=30)
#     card.pack(pady=80)
#     ttk.Button(card, text="Admin Login", width=30, command=admin_login).pack(pady=6)
#     ttk.Button(card, text="Student Login", width=30, command=student_login).pack(pady=6)
#     ttk.Button(card, text="Exit", width=30, command=root.destroy).pack(pady=6)

# # ================== ADMIN ==================
# def admin_login():
#     content = layout("Admin Login")
#     card = ttk.Frame(content, style="Card.TFrame", padding=30)
#     card.pack(pady=80)

#     u, p = tk.StringVar(), tk.StringVar()

#     for lbl, var, sec in [("Username", u, False), ("Password", p, True)]:
#         row = ttk.Frame(card)
#         row.pack(fill="x", pady=8)
#         ttk.Label(row, text=lbl, width=12).pack(side="left")
#         ttk.Entry(row, textvariable=var, show="*" if sec else "").pack(fill="x", expand=True)

#     def check():
#         if safe(u.get()) == ADMIN_USER and safe(p.get()) == ADMIN_PASS:
#             admin_menu()
#         else:
#             messagebox.showerror("Error", "Invalid credentials")

#     ttk.Button(card, text="Login", style="Accent.TButton", command=check).pack(pady=15)

# def admin_menu():
#     content = layout(
#         "Admin Dashboard",
#         [("Add Student", add_student),
#          ("Add Question", add_question),
#          ("View Results", view_results),
#          ("Logout", home)]
#     )
#     ttk.Label(content, text="Manage students, questions, and results.").pack(anchor="w")

# def add_student():
#     content = layout("Add Student", [("Back", admin_menu)])
#     card = ttk.Frame(content, style="Card.TFrame", padding=25)
#     card.pack(fill="x")

#     sid, name = tk.StringVar(), tk.StringVar()

#     for lbl, var in [("Student ID", sid), ("Student Name", name)]:
#         row = ttk.Frame(card)
#         row.pack(fill="x", pady=8)
#         ttk.Label(row, text=lbl, width=15).pack(side="left")
#         ttk.Entry(row, textvariable=var).pack(fill="x", expand=True)

#     def save():
#         if not safe(sid.get()) or not safe(name.get()):
#             messagebox.showerror("Error", "All fields required")
#             return
#         students.append({"Id": safe(sid.get()), "Name": clean(name.get())})
#         messagebox.showinfo("Saved", "Student added")
#         admin_menu()

#     ttk.Button(card, text="Save Student", style="Accent.TButton", command=save).pack(anchor="e", pady=15)

# def add_question():
#     content = layout("Add Question", [("Back", admin_menu)])
#     card = ttk.Frame(content, style="Card.TFrame", padding=25)
#     card.pack(fill="x")

#     fields = ["Question", "A", "B", "C", "D", "Correct (A/B/C/D)"]
#     vars_ = [tk.StringVar() for _ in fields]

#     for lbl, var in zip(fields, vars_):
#         row = ttk.Frame(card)
#         row.pack(fill="x", pady=6)
#         ttk.Label(row, text=lbl, width=20).pack(side="left")
#         ttk.Entry(row, textvariable=var).pack(fill="x", expand=True)

#     def save():
#         if not all(safe(v.get()) for v in vars_):
#             messagebox.showerror("Error", "All fields required")
#             return
#         questions.append({
#             "q": clean(vars_[0].get()),
#             "A": clean(vars_[1].get()),
#             "B": clean(vars_[2].get()),
#             "C": clean(vars_[3].get()),
#             "D": clean(vars_[4].get()),
#             "correct": safe(vars_[5].get()).upper()
#         })
#         messagebox.showinfo("Saved", "Question added")
#         admin_menu()

#     ttk.Button(card, text="Save Question", style="Accent.TButton", command=save).pack(anchor="e", pady=15)

# def view_results():
#     content = layout("Results", [("Back", admin_menu)])
#     for r in results:
#         card = ttk.Frame(content, style="Card.TFrame", padding=15)
#         card.pack(fill="x", pady=6)
#         ttk.Label(card, text=f"{r['Name']} ({r['Id']})", style="CardTitle.TLabel").pack(anchor="w")
#         ttk.Label(card, text=f"Score: {r['Score']}/{r['Total']} | {r['Percent']}% | {r['Status']}").pack(anchor="w")

# # ================== STUDENT ==================
# def student_login():
#     content = layout("Student Login")
#     card = ttk.Frame(content, style="Card.TFrame", padding=30)
#     card.pack(pady=80)

#     sid = tk.StringVar()
#     ttk.Entry(card, textvariable=sid, width=30).pack(pady=10)

#     def login():
#         global current_student
#         for s in students:
#             if s["Id"] == safe(sid.get()):
#                 current_student = s
#                 student_menu()
#                 return
#         messagebox.showerror("Error", "Student not found")

#     ttk.Button(card, text="Login", style="Accent.TButton", command=login).pack(pady=10)

# def student_menu():
#     content = layout(
#         f"Welcome, {current_student['Name']}",
#         [("Take Exam", start_exam),
#          ("My Result", my_result),
#          ("Logout", home)]
#     )

# def my_result():
#     content = layout("My Result", [("Back", student_menu)])
#     for r in results:
#         if r["Id"] == current_student["Id"]:
#             card = ttk.Frame(content, style="Card.TFrame", padding=20)
#             card.pack()
#             for k, v in r.items():
#                 ttk.Label(card, text=f"{k}: {v}").pack(anchor="w")

# # ================== EXAM ==================
# def start_exam():
#     global current_questions, current_score, current_total, question_index, exam_running, exam_time_left

#     current_questions = random.sample(questions, min(QUESTIONS_PER_EXAM, len(questions)))
#     current_score = 0
#     current_total = len(current_questions)
#     question_index = 0
#     exam_time_left = EXAM_DURATION_SECONDS
#     exam_running = True

#     content = layout("Exam In Progress")
#     timer = ttk.Label(content, font=("Segoe UI", 11, "bold"), foreground="red")
#     timer.pack(anchor="e")

#     progress = ttk.Progressbar(content, maximum=current_total)
#     progress.pack(fill="x", pady=10)

#     card = ttk.Frame(content, style="Card.TFrame", padding=25)
#     card.pack(fill="x")

#     question_lbl = ttk.Label(card, font=("Segoe UI", 14, "bold"), wraplength=650)
#     question_lbl.pack(anchor="w", pady=10)

#     var = tk.StringVar()
#     radios = []

#     for _ in range(4):
#         rb = ttk.Radiobutton(card, variable=var)
#         rb.pack(anchor="w", pady=4)
#         radios.append(rb)

#     def update():
#         nonlocal question_lbl
#         q = current_questions[question_index]
#         question_lbl.config(text=q["q"])
#         for rb, k in zip(radios, ["A", "B", "C", "D"]):
#             rb.config(text=f"{k}) {q[k]}", value=k)
#         progress["value"] = question_index + 1
#         var.set("")

#     def submit():
#         global current_score, question_index
#         if var.get() == current_questions[question_index]["correct"]:
#             current_score += 1
#         question_index += 1
#         if question_index >= current_total:
#             finish_exam()
#         else:
#             update()

#     ttk.Button(card, text="Next", style="Accent.TButton", command=submit).pack(anchor="e", pady=15)
#     update()

# def finish_exam():
#     results.append({
#         "Id": current_student["Id"],
#         "Name": current_student["Name"],
#         "Score": current_score,
#         "Total": current_total,
#         "Percent": f"{(current_score/current_total)*100:.2f}",
#         "Status": "Pass" if current_score/current_total >= 0.5 else "Fail",
#         "Date": now()
#     })
#     messagebox.showinfo("Finished", "Exam completed")
#     student_menu()

# # ================== START ==================
# home()
# root.mainloop()
