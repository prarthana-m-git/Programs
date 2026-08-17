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
            attendance = float(input("Enter