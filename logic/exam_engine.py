"""
This module contains the core logic for managing students, questions, and exam flow.
"""

from datetime import datetime
from random import sample
from models.models import Student, Question, Result

class ExamEngine:
    def __init__(self):
        self.students = []
        self.questions = []
        self.results = []

    def safe(self, s):
        return (s or "").strip()

    def clean(self, s):
        return self.safe(s).replace("|", "/").replace(",", " ")

    def now(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Student Management
    def add_student(self, student_id, name):
        if self.find_student(student_id):
            raise ValueError("Student already exists")
        self.students.append(Student(id=student_id, name=name))

    def find_student(self, student_id):
        """Retrieve a student by their ID."""
        student_id = self.safe(student_id)
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    # Question Management
    def add_question(self, question, options, correct):
        if correct not in options:
            raise ValueError("Correct answer must be one of the options")
        self.questions.append(Question(question=question, options=options, correct=correct))

    # Exam Flow
    def start_exam(self, student_id, question_count):
        student = self.find_student(student_id)
        if not student:
            raise ValueError("Student not found")
        if self.has_taken_exam(student_id):
            raise ValueError("Student has already taken the exam")
        if len(self.questions) < question_count:
            raise ValueError("Not enough questions available")
        return sample(self.questions, question_count)

    def has_taken_exam(self, student_id):
        return any(result.student_id == student_id for result in self.results)

    def save_result(self, student_id, student_name, score, total):
        percent = (score / total) * 100 if total else 0
        status = "Pass" if percent >= 50 else "Fail"
        self.results.append(Result(
            student_id=student_id,
            student_name=student_name,
            score=score,
            total=total,
            percent=percent,
            status=status,
            date=self.now()
        ))

    def get_results(self, student_id):
        return [result for result in self.results if result.student_id == student_id]