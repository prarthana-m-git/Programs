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


students = {}
subjects = ["Python", "Maths", "Data Science"]


# ---------------- STUDENT INPUT ----------------

n = int(input("Enter number of students: "))

for i in range(n):
    print(f"\n--- Student {i + 1} ---")

    name = input("Enter name: ").strip()

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

    while True:
        try:
            attendance = float(input("Enter attendance percentage: "))

            if 0 <= attendance <= 100:
                break
            else:
                print("Attendance must be between 0 and 100.")

        except ValueError:
            print("Invalid input.")

    average = sum(marks.values()) / len(marks)

    highest_subject = max(marks, key=marks.get)

    grade = calculate_grade(average)

    status = calculate_status(list(marks.values()), attendance)

    students[name] = {
        "marks": marks,
        "attendance": attendance,
        "average": average,
        "grade": grade,
        "status": status,
        "highest_subject": highest_subject
    }


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
    print("6. Exit")

    choice = input("\nEnter your choice: ")

    # -------- DISPLAY ALL --------

    if choice == "1":

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

    # -------- EXIT --------

    elif choice == "6":

        print("\nProgram terminated.")
        break

    else:
        print("Invalid choice. Please try again.")