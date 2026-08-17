import json
import os

DATA_FILE = "students.json"


def calculate_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def calculate_status(marks, attendance):
    if all(mark >= 40 for mark in marks) and attendance >= 75:
        return "PASS"
    return "FAIL"


def get_valid_marks(subjects):
    marks = {}
    for subject in subjects:
        while True:
            try:
                mark = float(input(f"Enter marks in {subject}: "))
                if 0 <= mark <= 100:
                    marks[subject] = mark
                    break
                else:
                    print("Enter marks between 0 and 100.")
            except ValueError:
                print("Invalid input.")
    return marks


def get_valid_attendance():
    while True:
        try:
            attendance = float(input("Enter attendance percentage: "))
            if 0 <= attendance <= 100:
                return attendance
            else:
                print("Attendance must be between 0 and 100.")
        except ValueError:
            print("Invalid input.")


def build_student_record(marks, attendance):
    average = sum(marks.values()) / len(marks)
    highest_subject = max(marks, key=marks.get)
    grade = calculate_grade(average)
    status = calculate_status(list(marks.values()), attendance)

    return {
        "marks": marks,
        "attendance": attendance,
        "average": average,
        "grade": grade,
        "status": status,
        "highest_subject": highest_subject
    }


# ---------------- SAVE / LOAD ----------------

def save_students(students, filename=DATA_FILE):
    try:
        with open(filename, "w") as f:
            json.dump(students, f, indent=2)
        print(f"\nData saved to '{filename}'.")
    except OSError as e:
        print(f"\nCould not save file: {e}")


def load_students(filename=DATA_FILE):
    if not os.path.exists(filename):
        print(f"\nNo saved file found ('{filename}'). Starting fresh.")
        return {}

    try:
        with open(filename, "r") as f:
            data = json.load(f)
        print(f"\nLoaded {len(data)} student(s) from '{filename}'.")
        return data
    except (OSError, json.JSONDecodeError) as e:
        print(f"\nCould not load file: {e}. Starting fresh.")
        return {}


students = {}
subjects = ["Python", "Maths", "Data Science"]


# ---------------- STARTUP: LOAD EXISTING DATA ----------------

if os.path.exists(DATA_FILE):
    choice = input(f"Found existing data in '{DATA_FILE}'. Load it? (y/n): ").strip().lower()
    if choice == "y":
        students = load_students()


# ---------------- STUDENT INPUT ----------------

add_more = input("\nAdd new students now? (y/n): ").strip().lower()

if add_more == "y":
    n = int(input("Enter number of students: "))

    for i in range(n):
        print(f"\n--- Student {i + 1} ---")

        name = input("Enter name: ").strip()
        marks = get_valid_marks(subjects)
        attendance = get_valid_attendance()

        students[name] = build_student_record(marks, attendance)


# ---------------- MENU ----------------

while True:

    print("\n" + "=" * 55)
    print("          STUDENT MANAGEMENT SYSTEM")
    print("=" * 55)

    print("1. Display all students")
    print("2. Display class topper")
    print("3. Search student")
    print("4. Subject-wise average")
    print("5. Display passed students")
    print("6. Add a new student")
    print("7. Edit a student")
    print("8. Delete a student")
    print("9. Save to file")
    print("10. Exit")

    choice = input("\nEnter your choice: ")

    # -------- DISPLAY ALL --------

    if choice == "1":

        if not students:
            print("\nNo students yet.")
            continue

        ranking = sorted(
            students.items(),
            key=lambda x: x[1]["average"],
            reverse=True
        )

        print("\n" + "-" * 75)
        print(f"{'Rank':<6}{'Name':<15}{'Average':<12}"
              f"{'Grade':<10}{'Attendance':<15}{'Status'}")
        print("-" * 75)

        for rank, (name, data) in enumerate(ranking, start=1):

            print(
                f"{rank:<6}"
                f"{name:<15}"
                f"{data['average']:<12.2f}"
                f"{data['grade']:<10}"
                f"{data['attendance']:<15.1f}"
                f"{data['status']}"
            )

    # -------- TOPPER --------

    elif choice == "2":

        if not students:
            print("\nNo students yet.")
            continue

        topper = max(
            students.items(),
            key=lambda x: x[1]["average"]
        )

        name, data = topper

        print("\nCLASS TOPPER")
        print("-" * 30)
        print("Name           :", name)
        print("Average        :", round(data["average"], 2))
        print("Grade          :", data["grade"])
        print("Best Subject   :", data["highest_subject"])
        print("Attendance     :", data["attendance"], "%")

    # -------- SEARCH --------

    elif choice == "3":

        search_name = input("Enter student name: ").strip()

        if search_name in students:

            data = students[search_name]

            print("\nStudent Found!")
            print("-" * 30)
            print("Name       :", search_name)

            for subject, mark in data["marks"].items():
                print(f"{subject:<12}: {mark}")

            print("Average    :", round(data["average"], 2))
            print("Grade      :", data["grade"])
            print("Attendance :", data["attendance"], "%")
            print("Best Subject:", data["highest_subject"])
            print("Status     :", data["status"])

        else:
            print("Student not found.")

    # -------- SUBJECT AVERAGE --------

    elif choice == "4":

        if not students:
            print("\nNo students yet.")
            continue

        print("\nSUBJECT-WISE CLASS AVERAGE")
        print("-" * 35)

        for subject in subjects:

            total = sum(
                data["marks"][subject]
                for data in students.values()
            )

            average = total / len(students)

            print(f"{subject:<15}: {average:.2f}")

    # -------- PASSED STUDENTS --------

    elif choice == "5":

        print("\nPASSED STUDENTS")
        print("-" * 30)

        passed = [
            name
            for name, data in students.items()
            if data["status"] == "PASS"
        ]

        if passed:
            for name in passed:
                print("✓", name)
        else:
            print("No students have passed.")

    # -------- ADD NEW STUDENT --------

    elif choice == "6":

        name = input("Enter name: ").strip()

        if name in students:
            print("A student with this name already exists. Use 'Edit' instead.")
            continue

        marks = get_valid_marks(subjects)
        attendance = get_valid_attendance()

        students[name] = build_student_record(marks, attendance)
        print(f"\n{name} added successfully.")

    # -------- EDIT STUDENT --------

    elif choice == "7":

        name = input("Enter the name of the student to edit: ").strip()

        if name not in students:
            print("Student not found.")
            continue

        print(f"\nEditing {name}. Leave blank to keep current value.")
        current = students[name]
        marks = dict(current["marks"])

        for subject in subjects:
            raw = input(f"{subject} (current: {marks[subject]}): ").strip()
            if raw:
                try:
                    mark = float(raw)
                    if 0 <= mark <= 100:
                        marks[subject] = mark
                    else:
                        print(f"Out of range, keeping {marks[subject]}.")
                except ValueError:
                    print(f"Invalid input, keeping {marks[subject]}.")

        raw = input(f"Attendance (current: {current['attendance']}): ").strip()
        attendance = current["attendance"]
        if raw:
            try:
                val = float(raw)
                if 0 <= val <= 100:
                    attendance = val
                else:
                    print("Out of range, keeping previous attendance.")
            except ValueError:
                print("Invalid input, keeping previous attendance.")

        students[name] = build_student_record(marks, attendance)
        print(f"\n{name} updated successfully.")

    # -------- DELETE STUDENT --------

    elif choice == "8":

        name = input("Enter the name of the student to delete: ").strip()

        if name in students:
            confirm = input(f"Are you sure you want to delete {name}? (y/n): ").strip().lower()
            if confirm == "y":
                del students[name]
                print(f"\n{name} deleted.")
            else:
                print("Cancelled.")
        else:
            print("Student not found.")

    # -------- SAVE --------

    elif choice == "9":

        save_students(students)

    # -------- EXIT --------

    elif choice == "10":

        if students:
            confirm = input("Save before exiting? (y/n): ").strip().lower()
            if confirm == "y":
                save_students(students)

        print("\nProgram terminated.")
        break

    else:
        print("Invalid choice. Please try again.")