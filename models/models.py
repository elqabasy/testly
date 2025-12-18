"""
This module contains the data models for the Testly application.
"""

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Student:
    id: str
    name: str

@dataclass
class Question:
    question: str
    options: dict
    correct: str

@dataclass
class Result:
    student_id: str
    student_name: str
    score: int
    total: int
    percent: float
    status: str
    date: str