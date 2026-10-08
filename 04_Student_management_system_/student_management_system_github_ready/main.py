from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "students.csv"
FIELDS = ["roll_no", "name", "python", "sql", "maths", "percentage", "grade"]

def calculate_percentage(python, sql, maths):
    return round((python + sql + maths) / 3, 2)

def calculate_grade(percentage):
    if percentage >= 90: return "A+"
    if percentage >= 80: return "A"
    if percentage >= 70: return "B"
    if percentage >= 60: return "C"
    if percentage >= 50: return "D"
    return "F"

def load_students():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def save_students(students):
    with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(students)

def get_mark(subject):
    while True:
        try:
            mark = float(input(f"Enter {subject} marks (0-100): "))
            if 0 <= mark <= 100:
                return mark
            print("Marks must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")

def find_student(students, roll_no):
    return next((s for s in students if s["roll_no"] == roll_no), None)

def add_student(students):
    print("\n--- ADD STUDENT ---")
    roll_no = input("Enter roll number: ").strip()
    if find_student(students, roll_no):
        print("A student with this roll number already exists.")
        return
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    python = get_mark("Python")
    sql = get_mark("SQL")
    maths = get_mark("Maths")
    percentage = calculate_percentage(python, sql, maths)
    students.append({
        "roll_no": roll_no, "name": name, "python": python,
        "sql": sql, "maths": maths, "percentage": percentage,
        "grade": calculate_grade(percentage)
    })
    save_students(students)
    print("Student added successfully.")

def view_students(students):
    print("\n--- ALL STUDENTS ---")
    if not students:
        print("No student records found.")
        return
    print("-" * 85)
    print(f"{'Roll':<10}{'Name':<22}{'Python':<10}{'SQL':<10}{'Maths':<10}{'%':<10}{'Grade':<8}")
    print("-" * 85)
    for s in students:
        print(f"{s['roll_no']:<10}{s['name']:<22}{float(s['python']):<10.2f}"
              f"{float(s['sql']):<10.2f}{float(s['maths']):<10.2f}"
              f"{float(s['percentage']):<10.2f}{s['grade']:<8}")
    print("-" * 85)

def search_student(students):
    print("\n--- SEARCH STUDENT ---")
    roll_no = input("Enter roll number: ").strip()
    student = find_student(students, roll_no)
    if not student:
        print("Student not found.")
        return
    print(f"\nRoll Number : {student['roll_no']}")
    print(f"Name        : {student['name']}")
    print(f"Python      : {student['python']}")
    print(f"SQL         : {student['sql']}")
    print(f"Maths       : {student['maths']}")
    print(f"Percentage  : {student['percentage']}%")
    print(f"Grade       : {student['grade']}")

def update_student(students):
    print("\n--- UPDATE STUDENT ---")
    roll_no = input("Enter roll number: ").strip()
    student = find_student(students, roll_no)
    if not student:
        print("Student not found.")
        return
    name = input(f"Enter new name [{student['name']}]: ").strip()
    if name:
        student["name"] = name
    student["python"] = get_mark("Python")
    student["sql"] = get_mark("SQL")
    student["maths"] = get_mark("Maths")
    pct = calculate_percentage(float(student["python"]), float(student["sql"]), float(student["maths"]))
    student["percentage"] = pct
    student["grade"] = calculate_grade(pct)
    save_students(students)
    print("Student updated successfully.")

def delete_student(students):
    print("\n--- DELETE STUDENT ---")
    roll_no = input("Enter roll number: ").strip()
    student = find_student(students, roll_no)
    if not student:
        print("Student not found.")
        return
    students.remove(student)
    save_students(students)
    print("Student deleted successfully.")

def show_topper(students):
    print("\n--- TOPPER ---")
    if not students:
        print("No student records found.")
        return
    topper = max(students, key=lambda s: float(s["percentage"]))
    print(f"Roll Number : {topper['roll_no']}")
    print(f"Name        : {topper['name']}")
    print(f"Percentage  : {topper['percentage']}%")
    print(f"Grade       : {topper['grade']}")

def main():
    students = load_students()
    while True:
        print("\n" + "=" * 50)
        print("       STUDENT MANAGEMENT SYSTEM")
        print("=" * 50)
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Show Topper")
        print("7. Exit")
        print("=" * 50)
        choice = input("Enter your choice (1-7): ").strip()
        if choice == "1": add_student(students)
        elif choice == "2": view_students(students)
        elif choice == "3": search_student(students)
        elif choice == "4": update_student(students)
        elif choice == "5": delete_student(students)
        elif choice == "6": show_topper(students)
        elif choice == "7":
            print("Thank you for using Student Management System.")
            break
        else: print("Invalid choice. Please select 1-7.")

if __name__ == "__main__":
    main()
