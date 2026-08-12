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


students = {}

n = int(input("Enter number of students: "))

for i in range(n):
    name = input(f"\nEnter student {i + 1} name: ")

    marks = []
    for subject in ["Python", "Maths", "Data Science"]:
        while True:
            try:
                mark = float(input(f"Enter marks in {subject}: "))

                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                else:
                    print("Marks must be between 0 and 100.")

            except ValueError:
                print("Please enter a valid number.")

    average = sum(marks) / len(marks)

    students[name] = {
        "marks": marks,
        "average": average,
        "grade": calculate_grade(average)
    }


# Rank students based on average marks
ranking = sorted(
    students.items(),
    key=lambda x: x[1]["average"],
    reverse=True
)

print("\n" + "=" * 50)
print("           STUDENT PERFORMANCE REPORT")
print("=" * 50)

for rank, (name, data) in enumerate(ranking, start=1):
    print(
        f"{rank}. {name:<15} "
        f"Average: {data['average']:.2f}   "
        f"Grade: {data['grade']}"
    )

# Class statistics
averages = [data["average"] for data in students.values()]

print("\n" + "-" * 50)
print(f"Class Average : {sum(averages) / len(averages):.2f}")
print(f"Top Student   : {ranking[0][0]}")
print(f"Highest Score : {ranking[0][1]['average']:.2f}")
print("-" * 50)