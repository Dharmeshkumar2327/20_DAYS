import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import calculate_percentage, calculate_grade, find_student

def test_percentage():
    assert calculate_percentage(90, 80, 70) == 80.0

def test_grades():
    assert calculate_grade(95) == "A+"
    assert calculate_grade(85) == "A"
    assert calculate_grade(75) == "B"
    assert calculate_grade(65) == "C"
    assert calculate_grade(55) == "D"
    assert calculate_grade(45) == "F"

def test_find_student():
    students = [{"roll_no": "101", "name": "Test"}]
    assert find_student(students, "101")["name"] == "Test"
    assert find_student(students, "999") is None
