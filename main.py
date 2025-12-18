import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime

# ================== GLOBAL DATA (IN-MEMORY) ==================
# All data is stored in memory and cleared when the program closes
students = []
questions = []
results = []    

ADMIN_USER = "admin"
ADMIN_PASS = "1234"

# Exam settings
EXAM_DURATION_SECONDS = 60
QUESTIONS_PER_EXAM = 5

# Exam runtime state
exam_time_left = 0
exam_running = False
timer_after_id = None

current_student = None
current_questions = []
current_score = 0
current_total = 0

# Reference to the currently opened question window
open_question_window = None
question_index = 0
progress_bar = None

# ================== HELPER FUNCTIONS ==================
def safe(s):
    """Remove leading/trailing spaces and handle None."""
    return (s or "").strip()

def clean(s):
    """Clean input to avoid format issues."""
    return safe(s).replace("|", "/").replace(",", " ")

def now():
    """Return current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ================== STUDENT FUNCTIONS ==================
def find_student(sid):
    """Find student by ID."""
    sid = safe(sid)
    for s in students:
        if s["Id"] == sid:
            return s
    return None

def student_exists(sid):
    """Check if student already exists."""
    return find_student(sid) is not None

# ================== RESULT FUNCTIONS ==================
def has_taken_exam(sid):
    """Check if student already took the exam."""
    sid = safe(sid)
    for r in results:
        if r["Id"] == sid:
            return True
    return False

def save_result(sid, name, score, total):
    """Save exam result (session only)."""
    pct = (score / total) * 100 if total else 0
    status = "Pass" if pct >= 50 else "Fail"
    results.append({
        "Id": sid,
        "Name": name,
        "Score": score,
        "Total": total,
        "Percent": f"{pct:.2f}",
        "Status": status,
        "Date": now()
    })

def get_result(sid):
    """Get latest result for a student."""
    sid = safe(sid)
    for r in reversed(results):
        if r["Id"] == sid:
            return r
    return None

# ================== GUI CORE ==================
root = tk.Tk()
style = ttk.Style(root)

style.theme_use("clam")

root.configure(bg="#f5f7fb")

style.configure("TFrame", background="#f5f7fb")
style.configure("TLabel", background="#f5f7fb", foreground="#111827")

style.configure(
    "Sidebar.TFrame",
    background="#111827"
)

style.configure(
    "Header.TLabel",
    font=("Segoe UI", 20, "bold"),
    foreground="#111827",
    background="#f5f7fb"
)

style.configure(
    "TButton",
    font=("Segoe UI", 11),
    padding=8
)

style.configure(
    "Accent.TButton",
    background="#2563eb",
    foreground="white",
    font=("Segoe UI", 11, "bold"),
    padding=10,
    borderwidth=0
)

style.map(
    "Accent.TButton",
    background=[("active", "#1d4ed8")]
)

style.configure(
    "Horizontal.TProgressbar",
    troughcolor="#e5e7eb",
    background="#2563eb",
    thickness=8
)



style.configure(
    "TLabel",
    font=("Segoe UI", 11)
)

root.title("Smart Exam System (Session Based)")
root.geometry("750x520")

main = ttk.Frame(root)
main.pack(fill="both", expand=True)

# Timer label (must not be destroyed)
timer_label = ttk.Label(main, text="", font=("Arial", 12, "bold"))
timer_label.pack(pady=5)

def clear():
    """Clear screen except the timer label."""
    for w in main.winfo_children():
        if w != timer_label:
            w.destroy()
    timer_label.config(text="")

def header(title):
    ttk.Label(main, text=title, style="Header.TLabel").pack(pady=15)

def layout_with_sidebar(title, buttons):
    clear()

    wrapper = ttk.Frame(main)
    wrapper.pack(fill="both", expand=True)

    sidebar = ttk.Frame(wrapper, width=210, style="Sidebar.TFrame")
    sidebar.pack(side="left", fill="y", padx=10, pady=10)
    ttk.Label(
    sidebar,
    text="SMART EXAM",
    font=("Segoe UI", 15, "bold"),
    foreground="#e5e7eb",
    background="#111827"
).pack(pady=(15, 25))


    content = ttk.Frame(wrapper)
    content.pack(side="right", fill="both", expand=True, padx=20, pady=10)

    for text, cmd in buttons:
        ttk.Button(sidebar, text=text, command=cmd).pack(fill="x", pady=4)

    ttk.Label(
        content,
        text=title,
        style="Header.TLabel"
    ).pack(anchor="w", pady=10)

    return content


# ================== HOME SCREEN ==================
def home():
    stop_timer()
    clear()
    header("Smart Exam System")

    box = ttk.Frame(main)
    box.pack(pady=30)

    ttk.Button(box, text="Admin Login", width=30, command=admin_login).pack(pady=6)
    ttk.Button(box, text="Student Login", width=30, command=student_login).pack(pady=6)
    ttk.Button(box, text="Exit", width=30, command=root.destroy).pack(pady=6)


# ================== ADMIN SECTION ==================
def admin_login():
    clear()
    header("Admin Login")

    u = tk.StringVar()
    p = tk.StringVar()

    ttk.Label(main, text="Username").pack()
    ttk.Entry(main, textvariable=u).pack()
    ttk.Label(main, text="Password").pack()
    ttk.Entry(main, textvariable=p, show="*").pack()

    def check():
        if safe(u.get()) == ADMIN_USER and safe(p.get()) == ADMIN_PASS:
            admin_menu()
        else:
            messagebox.showerror("Error", "Invalid login")

    ttk.Button(main, text="Login", command=check).pack(pady=10)
    ttk.Button(main, text="Back", command=home).pack()

def admin_menu():
    content = layout_with_sidebar(
        "Admin Dashboard",
        [
            ("Add Student", add_student),
            ("Add Question", add_question),
            ("View Results", view_results),
            ("Logout", home),
        ]
    )

    ttk.Label(
        content,
        text="Manage students, questions and exam results efficiently.",
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=5)


def add_student():
    content = layout_with_sidebar(
        "Add Student",
        [("Back", admin_menu)]
    )

    form = ttk.Frame(content)
    form.pack(pady=20)

    ttk.Label(form, text="Student ID").grid(row=0, column=0, sticky="w", pady=5)
    sid = tk.StringVar()
    ttk.Entry(form, textvariable=sid, width=30).grid(row=0, column=1, pady=5)

    ttk.Label(form, text="Student Name").grid(row=1, column=0, sticky="w", pady=5)
    name = tk.StringVar()
    ttk.Entry(form, textvariable=name, width=30).grid(row=1, column=1, pady=5)

    def save():
        s = safe(sid.get())
        n = clean(name.get())
        if not s or not n:
            messagebox.showerror("Error", "Fill all fields")
            return
        if student_exists(s):
            messagebox.showerror("Error", "Student already exists")
            return
        students.append({"Id": s, "Name": n})
        messagebox.showinfo("Saved", "Student added")
        admin_menu()

    ttk.Button(content, text="Save Student", command=save).pack(pady=10)

def add_question():
    clear()
    header("Add MCQ Question")

    vars_ = [tk.StringVar() for _ in range(6)]
    labels = ["Question", "A", "B", "C", "D", "Correct (A/B/C/D)"]

    for i in range(6):
        ttk.Label(main, text=labels[i]).pack()
        ttk.Entry(main, textvariable=vars_[i]).pack()

    def save():
        if not all(safe(v.get()) for v in vars_):
            messagebox.showerror("Error", "Fill all fields")
            return

        correct = safe(vars_[5].get()).upper()
        if correct not in ["A", "B", "C", "D"]:
            messagebox.showerror("Error", "Correct answer must be A, B, C, or D")
            return

        questions.append({
            "q": clean(vars_[0].get()),
            "A": clean(vars_[1].get()),
            "B": clean(vars_[2].get()),
            "C": clean(vars_[3].get()),
            "D": clean(vars_[4].get()),
            "correct": correct
        })

        messagebox.showinfo("Saved", "Question added (session only)")
        admin_menu()

    ttk.Button(main, text="Save", command=save).pack(pady=10)
    ttk.Button(main, text="Back", command=admin_menu).pack()

def view_results():
    clear()
    header("Results")

    if not results:
        ttk.Label(main, text="No results yet").pack()
    else:
        for r in results:
            ttk.Label(
                main,
                text=f"{r['Id']} | {r['Name']} | {r['Score']}/{r['Total']} | "
                     f"{r['Percent']}% | {r['Status']} | {r['Date']}"
            ).pack(anchor="w", padx=10)

    ttk.Button(main, text="Back", command=admin_menu).pack(pady=10)

# ================== STUDENT SECTION ==================
def student_login():
    global current_student
    clear()
    header("Student Login")

    sid = tk.StringVar()
    ttk.Label(main, text="Student ID").pack()
    ttk.Entry(main, textvariable=sid).pack()

    def login():
        global current_student
        s = find_student(sid.get())
        if not s:
            messagebox.showerror("Error", "Student not found (session)")
            return
        current_student = s
        student_menu()

    ttk.Button(main, text="Login", command=login).pack(pady=10)
    ttk.Button(main, text="Back", command=home).pack()

def student_menu():
    stop_timer()
    content = layout_with_sidebar(
        f"Welcome, {current_student['Name']}",
        [
            ("Take Exam", start_exam),
            ("My Result", view_my_result),
            ("Logout", home),
        ]
    )

    ttk.Label(
        content,
        text="Choose an action from the left panel.",
        font=("Segoe UI", 11)
    ).pack(anchor="w", pady=5)


def view_my_result():
    clear()
    header("My Result")

    r = get_result(current_student["Id"])
    if not r:
        ttk.Label(main, text="No result yet").pack()
    else:
        for k, v in r.items():
            ttk.Label(main, text=f"{k}: {v}").pack(anchor="w", padx=10)

    ttk.Button(main, text="Back", command=student_menu).pack(pady=10)

# ================== TIMER FUNCTIONS ==================
def stop_timer():
    global timer_after_id
    if timer_after_id is not None:
        try:
            root.after_cancel(timer_after_id)
        except Exception:
            pass
        timer_after_id = None

def close_open_question_window():
    global open_question_window
    if open_question_window is not None:
        try:
            if open_question_window.winfo_exists():
                open_question_window.destroy()
        except Exception:
            pass
    open_question_window = None

def update_timer():
    global exam_time_left, exam_running, timer_after_id

    if not exam_running:
        timer_label.config(text="")
        stop_timer()
        return

    timer_label.config(text=f"⏱ Time Left: {exam_time_left} sec")

    if exam_time_left <= 0:
        exam_running = False
        close_open_question_window()
        stop_timer()
        messagebox.showinfo("Time Up", "Exam time is over!")
        finish_exam()
        return

    exam_time_left -= 1
    timer_after_id = root.after(1000, update_timer)

# ================== EXAM FLOW ==================
def start_exam():
    global exam_time_left, exam_running
    global current_questions, current_score, current_total
    global question_index, progress_bar

    if has_taken_exam(current_student["Id"]):
        messagebox.showwarning("Not Allowed", "You already took the exam")
        return

    if not questions:
        messagebox.showerror("Error", "No questions available")
        return

    current_questions = questions[:]
    if QUESTIONS_PER_EXAM > 0:
        current_questions = random.sample(
            current_questions,
            min(QUESTIONS_PER_EXAM, len(current_questions))
        )

    current_score = 0
    current_total = len(current_questions)
    question_index = 0

    exam_time_left = EXAM_DURATION_SECONDS
    exam_running = True

    clear()
    header("Exam In Progress")

    progress_bar = ttk.Progressbar(
    main,
    length=400,
    maximum=current_total,
    mode="determinate",
    style="Horizontal.TProgressbar"
)

    progress_bar.pack(pady=10)

    stop_timer()
    update_timer()
    ask_next_question(0)


def ask_next_question(index):
    global question_index

    if not exam_running:
        return

    question_index = index
    if progress_bar:
        progress_bar["value"] = index

    if index >= len(current_questions):
        finish_exam()
        return

    q = current_questions[index]

    def on_answer(ans):
        global current_score
        if not exam_running:
            return
        if safe(ans).upper() == safe(q["correct"]).upper():
            current_score += 1
        ask_next_question(index + 1)

    ask_question(q, on_answer)


def ask_question(q, callback):
    global open_question_window

    if not exam_running:
        return

    win = tk.Toplevel(root)
    open_question_window = win
    win.title("Exam Question")
    win.geometry("520x380")
    win.resizable(False, False)

    container = ttk.Frame(win, padding=15)
    container.pack(fill="both", expand=True)

    var = tk.StringVar(value="")

    ttk.Label(
        container,
        text=q["q"],
        wraplength=480,
        font=("Segoe UI", 12, "bold")
    ).pack(pady=10)

    for k in ["A", "B", "C", "D"]:
        ttk.Radiobutton(
            container,
            text=f"{k}) {q[k]}",
            variable=var,
            value=k
        ).pack(anchor="w", pady=4)

    submit_btn = ttk.Button(container, text="Submit Answer")
    submit_btn.pack(pady=15)

    def submit():
        if not var.get():
            messagebox.showwarning("Warning", "Please select an answer")
            return
        win.destroy()
        callback(var.get())

    submit_btn.config(command=submit)
    win.protocol("WM_DELETE_WINDOW", submit)
    win.grab_set()



def finish_exam():
    global exam_running
    if exam_running:
        exam_running = False

    stop_timer()
    close_open_question_window()

    save_result(
        current_student["Id"],
        current_student["Name"],
        current_score,
        current_total
    )

    percent = (current_score / current_total) * 100
    status = "PASS ✅" if percent >= 50 else "FAIL ❌"

    messagebox.showinfo(
        "Exam Finished",
        f"Score: {current_score}/{current_total}\n"
        f"Percentage: {percent:.1f}%\n"
        f"Status: {status}"
    )

    student_menu()


# ================== START APPLICATION ==================
home()
root.mainloop()