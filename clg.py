import json

from models import Subject
from utils import get_int, get_float


subjects = []

FILE_NAME = "college_data.json"


def show_menu():
    print("\n====== COLLEGE MANAGER ======")
    print("1. Add subject")
    print("2. View subjects")
    print("3. Update attendance")
    print("4. Add IA marks")
    print("5. Add SEE marks")
    print("6. Calculate SGPA")
    print("7. Save")
    print("8. Exit")
    print("9. Search subject")
    print("10. Edit subject")
    print("11. Delete subject")
    print("12. Attendance report")


def add_subject():
    name = input("Enter subject name: ").strip()

    if not name:
        print("Subject name cannot be empty.")
        return

    credits = get_int("Enter credits: ", 1)

    subject = Subject(
        name=name,
        credits=credits
    )

    subjects.append(subject)

    print(f"\n{name} added successfully!")


def view_subjects():
    if not subjects:
        print("\nNo subjects added yet.")
        return

    print("\n====== YOUR SUBJECTS ======")

    for i, subject in enumerate(subjects, start=1):
        print(f"\n{i}. {subject.name}")
        print(f"   Credits: {subject.credits}")
        print(f"   Attendance: {subject.attendance_percentage()}%")
        print(f"   IA Average: {subject.ia_average()}")
        print(f"   SEE Marks: {subject.see_marks}")
        print(f"   Grade Point: {subject.grade_point}")


def update_attendance():
    if not subjects:
        print("\nNo subjects available.")
        return

    view_subjects()

    number = get_int(
        "\nEnter subject number: ",
        1,
        len(subjects)
    )

    subject = subjects[number - 1]

    while True:
        conducted = get_int(
            "Enter classes conducted: ",
            0
        )

        attended = get_int(
            "Enter classes attended: ",
            0
        )

        if attended > conducted:
            print(
                "Attended classes cannot be greater "
                "than conducted classes."
            )
            continue

        break

    subject.classes_conducted = conducted
    subject.classes_attended = attended

    print(
        f"\nAttendance updated: "
        f"{subject.attendance_percentage()}%"
    )


def add_ia_marks():
    if not subjects:
        print("\nNo subjects available.")
        return

    view_subjects()

    number = get_int(
        "\nEnter subject number: ",
        1,
        len(subjects)
    )

    subject = subjects[number - 1]

    subject.ia1 = get_float(
        "Enter IA 1 marks: ",
        0,
        50
    )

    subject.ia2 = get_float(
        "Enter IA 2 marks: ",
        0,
        50
    )

    subject.ia3 = get_float(
        "Enter IA 3 marks: ",
        0,
        50
    )

    print("\nIA marks added.")
    print(f"IA Average: {subject.ia_average()}")


def add_see_marks():
    if not subjects:
        print("\nNo subjects available.")
        return

    view_subjects()

    number = get_int(
        "\nEnter subject number: ",
        1,
        len(subjects)
    )

    subject = subjects[number - 1]

    subject.see_marks = get_float(
        "Enter SEE marks: ",
        0,
        50
    )

    subject.grade_point = get_float(
        "Enter grade point for this subject: ",
        0,
        10
    )

    print("\nSEE marks added successfully!")


def calculate_sgpa():
    if not subjects:
        print("\nNo subjects available.")
        return

    total_credit_points = 0
    total_credits = 0

    for subject in subjects:
        if subject.grade_point is None:
            print(
                f"\nGrade point missing for {subject.name}."
            )
            print(
                "Add SEE marks and grade point first."
            )
            return

        total_credit_points += (
            subject.credits * subject.grade_point
        )

        total_credits += subject.credits

    if total_credits == 0:
        print("\nNo credits available.")
        return

    sgpa = total_credit_points / total_credits

    print("\n====== SGPA ======")
    print(f"SGPA: {round(sgpa, 2)}")


def search_subject():
    if not subjects:
        print("\nNo subjects available.")
        return

    name = input("Enter subject name: ").strip().lower()

    for subject in subjects:
        if subject.name.lower() == name:
            print(f"\nSubject: {subject.name}")
            print(f"Credits: {subject.credits}")
            print(
                f"Attendance: "
                f"{subject.attendance_percentage()}%"
            )
            print(
                f"Attendance status: "
                f"{subject.attendance_status()}"
            )
            print(f"IA Average: {subject.ia_average()}")
            print(f"SEE Marks: {subject.see_marks}")
            print(f"Grade Point: {subject.grade_point}")
            return

    print("\nSubject not found.")


def edit_subject():
    if not subjects:
        print("\nNo subjects available.")
        return

    view_subjects()

    number = get_int(
        "\nEnter subject number to edit: ",
        1,
        len(subjects)
    )

    subject = subjects[number - 1]

    print(f"\nEditing: {subject.name}")

    new_name = input(
        f"Enter new name "
        f"(press Enter to keep '{subject.name}'): "
    ).strip()

    new_credits = input(
        f"Enter new credits "
        f"(press Enter to keep {subject.credits}): "
    ).strip()

    if new_name:
        subject.name = new_name

    if new_credits:
        try:
            credits = int(new_credits)

            if credits > 0:
                subject.credits = credits
            else:
                print("Credits must be greater than 0.")

        except ValueError:
            print("Invalid credits. Old credits kept.")

    print("\nSubject updated successfully!")


def delete_subject():
    if not subjects:
        print("\nNo subjects available.")
        return

    view_subjects()

    number = get_int(
        "\nEnter subject number to delete: ",
        1,
        len(subjects)
    )

    subject = subjects[number - 1]

    confirmation = input(
        f"Are you sure you want to delete "
        f"'{subject.name}'? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        subjects.pop(number - 1)
        print(
            f"\n{subject.name} deleted successfully!"
        )
    else:
        print("\nDelete cancelled.")


def attendance_report():
    if not subjects:
        print("\nNo subjects available.")
        return

    print("\n====== ATTENDANCE REPORT ======")

    shortage_count = 0

    for subject in subjects:
        percentage = subject.attendance_percentage()
        status = subject.attendance_status()

        print(f"\n{subject.name}")
        print(f"Attendance: {percentage}%")
        print(f"Status: {status}")

        if status == "Shortage":
            needed = subject.classes_needed_for_75()

            print(
                f"Classes needed to reach 75%: {needed}"
            )

            shortage_count += 1

    print("\n------------------------------")

    if shortage_count == 0:
        print("All subjects are above 75% attendance.")
    else:
        print(
            f"{shortage_count} subject(s) "
            "have attendance shortage."
        )


def save_data():
    data = [
        subject.model_dump()
        for subject in subjects
    ]

    with open(FILE_NAME, "w") as file:
        json.dump(
            data,
            file,
            indent=4
        )

    print("\nData saved successfully!")


def load_data():
    global subjects

    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

        subjects = [
            Subject(**subject_data)
            for subject_data in data
        ]

        print("Previous data loaded.")

    except FileNotFoundError:
        subjects = []

    except json.JSONDecodeError:
        print("Could not read saved data.")
        subjects = []


load_data()


while True:

    show_menu()

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":
        add_subject()

    elif choice == "2":
        view_subjects()

    elif choice == "3":
        update_attendance()

    elif choice == "4":
        add_ia_marks()

    elif choice == "5":
        add_see_marks()

    elif choice == "6":
        calculate_sgpa()

    elif choice == "7":
        save_data()

    elif choice == "8":
        save_data()
        print("Goodbye!")
        break

    elif choice == "9":
        search_subject()

    elif choice == "10":
        edit_subject()

    elif choice == "11":
        delete_subject()

    elif choice == "12":
        attendance_report()

    else:
        print("Invalid choice. Please try again.")