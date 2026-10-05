import customtkinter as ctk
from tkinter import messagebox
import database


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class CollegeManager(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("College Manager")
        self.geometry("1100x700")

        self.create_dashboard()
        self.refresh_dashboard()

    def create_dashboard(self):

        # Title
        title = ctk.CTkLabel(
            self,
            text="College Manager",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=20)

        # Dashboard cards
        card_frame = ctk.CTkFrame(self)
        card_frame.pack(fill="x", padx=30, pady=10)

        self.subject_card = self.create_card(
            card_frame,
            "Total Subjects",
            "0"
        )

        self.attendance_card = self.create_card(
            card_frame,
            "Average Attendance",
            "0%"
        )

        self.sgpa_card = self.create_card(
            card_frame,
            "SGPA",
            "0"
        )

        self.shortage_card = self.create_card(
            card_frame,
            "Attendance Shortage",
            "0"
        )

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        buttons = [
            ("Add Subject", self.add_subject),
            ("Attendance", self.update_attendance),
            ("Marks", self.update_marks),
            ("Search", self.search_subject),
            ("Edit", self.edit_subject),
            ("Delete", self.delete_subject),
            ("Attendance Report", self.attendance_report),
            ("Calculate SGPA", self.calculate_sgpa),
        ]

        for text, command in buttons:

            ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                width=150
            ).pack(
                side="left",
                padx=5,
                pady=10
            )

        # Subject list
        self.subject_list = ctk.CTkTextbox(
            self,
            width=1000,
            height=400,
            font=("Arial", 15)
        )

        self.subject_list.pack(
            padx=30,
            pady=10,
            fill="both",
            expand=True
        )

    def create_card(self, parent, title, value):

        frame = ctk.CTkFrame(
            parent,
            width=220,
            height=100
        )

        frame.pack(
            side="left",
            padx=10,
            pady=15,
            expand=True,
            fill="both"
        )

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 15)
        )

        label.pack(pady=(15, 5))

        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=("Arial", 25, "bold")
        )

        value_label.pack()

        return value_label

    def refresh_dashboard(self):

        subjects = database.get_subjects()

        self.subject_list.delete("1.0", "end")

        if not subjects:

            self.subject_card.configure(text="0")
            self.attendance_card.configure(text="0%")
            self.sgpa_card.configure(text="0")
            self.shortage_card.configure(text="0")

            self.subject_list.insert(
                "end",
                "No subjects added yet."
            )

            return

        # Total subjects
        self.subject_card.configure(
            text=str(len(subjects))
        )

        # Attendance
        attendance_values = []
        shortage_count = 0

        for subject in subjects:

            (
                subject_id,
                name,
                credits,
                conducted,
                attended,
                ia1,
                ia2,
                ia3,
                see,
                grade_point
            ) = subject

            if conducted > 0:

                attendance = round(
                    attended / conducted * 100,
                    2
                )

                attendance_values.append(attendance)

                if attendance < 75:
                    shortage_count += 1

            else:
                attendance = 0

            self.subject_list.insert(
                "end",
                f"Subject: {name}\n"
                f"Credits: {credits}\n"
                f"Attendance: {attendance}%\n"
                f"IA1: {ia1}\n"
                f"IA2: {ia2}\n"
                f"IA3: {ia3}\n"
                f"SEE: {see}\n"
                f"Grade Point: {grade_point}\n"
                f"\n{'-' * 50}\n\n"
            )

        if attendance_values:

            average_attendance = round(
                sum(attendance_values)
                / len(attendance_values),
                2
            )

        else:
            average_attendance = 0

        self.attendance_card.configure(
            text=f"{average_attendance}%"
        )

        self.shortage_card.configure(
            text=str(shortage_count)
        )

        # SGPA
        total_credits = 0
        total_points = 0
        complete = True

        for subject in subjects:

            credits = subject[2]
            grade_point = subject[9]

            if grade_point is None:
                complete = False
                break

            total_credits += credits
            total_points += credits * grade_point

        if complete and total_credits > 0:

            sgpa = round(
                total_points / total_credits,
                2
            )

            self.sgpa_card.configure(
                text=str(sgpa)
            )

        else:

            self.sgpa_card.configure(
                text="N/A"
            )

    # ---------------- ADD SUBJECT ----------------

    def add_subject(self):

        window = ctk.CTkToplevel(self)

        window.title("Add Subject")
        window.geometry("400x300")

        ctk.CTkLabel(
            window,
            text="Subject Name"
        ).pack(pady=(30, 5))

        name_entry = ctk.CTkEntry(
            window,
            width=250
        )

        name_entry.pack()

        ctk.CTkLabel(
            window,
            text="Credits"
        ).pack(pady=(20, 5))

        credits_entry = ctk.CTkEntry(
            window,
            width=250
        )

        credits_entry.pack()

        def save():

            name = name_entry.get().strip()

            try:
                credits = int(
                    credits_entry.get()
                )

                if not name or credits <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Enter valid subject details."
                )

                return

            database.add_subject(
                name,
                credits
            )

            window.destroy()

            self.refresh_dashboard()

        ctk.CTkButton(
            window,
            text="Add Subject",
            command=save
        ).pack(pady=30)

    # ---------------- ATTENDANCE ----------------

    def update_attendance(self):

        subjects = database.get_subjects()

        if not subjects:

            messagebox.showinfo(
                "Attendance",
                "No subjects available."
            )

            return

        window = ctk.CTkToplevel(self)

        window.title("Update Attendance")
        window.geometry("450x450")

        ctk.CTkLabel(
            window,
            text="Select Subject"
        ).pack(pady=(20, 5))

        subject_names = [
            f"{row[0]} - {row[1]}"
            for row in subjects
        ]

        selected = ctk.CTkComboBox(
            window,
            values=subject_names,
            width=300
        )

        selected.pack()

        ctk.CTkLabel(
            window,
            text="Classes Conducted"
        ).pack(pady=(20, 5))

        conducted_entry = ctk.CTkEntry(
            window,
            width=300
        )

        conducted_entry.pack()

        ctk.CTkLabel(
            window,
            text="Classes Attended"
        ).pack(pady=(20, 5))

        attended_entry = ctk.CTkEntry(
            window,
            width=300
        )

        attended_entry.pack()

        def save():

            try:

                subject_id = int(
                    selected.get().split(" - ")[0]
                )

                conducted = int(
                    conducted_entry.get()
                )

                attended = int(
                    attended_entry.get()
                )

                if conducted < 0 or attended < 0:
                    raise ValueError

                if attended > conducted:

                    messagebox.showerror(
                        "Error",
                        "Attended cannot be greater than conducted."
                    )

                    return

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Enter valid attendance."
                )

                return

            database.update_attendance(
                subject_id,
                conducted,
                attended
            )

            window.destroy()

            self.refresh_dashboard()

        ctk.CTkButton(
            window,
            text="Save Attendance",
            command=save
        ).pack(pady=30)

    # ---------------- MARKS ----------------

    def update_marks(self):

        subjects = database.get_subjects()

        if not subjects:

            messagebox.showinfo(
                "Marks",
                "No subjects available."
            )

            return

        window = ctk.CTkToplevel(self)

        window.title("Update Marks")
        window.geometry("450x650")

        ctk.CTkLabel(
            window,
            text="Select Subject"
        ).pack(pady=(20, 5))

        subject_names = [
            f"{row[0]} - {row[1]}"
            for row in subjects
        ]

        selected = ctk.CTkComboBox(
            window,
            values=subject_names,
            width=300
        )

        selected.pack()

        entries = []

        labels = [
            "IA 1 Marks",
            "IA 2 Marks",
            "IA 3 Marks",
            "SEE Marks",
            "Grade Point"
        ]

        limits = [
            (0, 50),
            (0, 50),
            (0, 50),
            (0, 50),
            (0, 10)
        ]

        for label, limit in zip(labels, limits):

            ctk.CTkLabel(
                window,
                text=label
            ).pack(pady=(15, 5))

            entry = ctk.CTkEntry(
                window,
                width=300
            )

            entry.pack()

            entries.append(entry)

        def save():

            try:

                values = []

                for entry, (minimum, maximum) in zip(
                    entries,
                    limits
                ):

                    value = float(
                        entry.get()
                    )

                    if value < minimum or value > maximum:
                        raise ValueError

                    values.append(value)

                subject_id = int(
                    selected.get().split(" - ")[0]
                )

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Enter valid marks."
                )

                return

            database.update_marks(
                subject_id,
                values[0],
                values[1],
                values[2],
                values[3],
                values[4]
            )

            window.destroy()

            self.refresh_dashboard()

        ctk.CTkButton(
            window,
            text="Save Marks",
            command=save
        ).pack(pady=25)

    # ---------------- SEARCH ----------------

    def search_subject(self):

        subjects = database.get_subjects()

        if not subjects:

            messagebox.showinfo(
                "Search",
                "No subjects available."
            )

            return

        window = ctk.CTkToplevel(self)

        window.title("Search Subject")
        window.geometry("400x300")

        ctk.CTkLabel(
            window,
            text="Subject Name"
        ).pack(pady=(30, 5))

        entry = ctk.CTkEntry(
            window,
            width=300
        )

        entry.pack()

        def search():

            name = entry.get().strip().lower()

            for subject in subjects:

                if subject[1].lower() == name:

                    messagebox.showinfo(
                        "Subject",
                        f"Subject: {subject[1]}\n"
                        f"Credits: {subject[2]}\n"
                        f"IA1: {subject[5]}\n"
                        f"IA2: {subject[6]}\n"
                        f"IA3: {subject[7]}\n"
                        f"SEE: {subject[8]}\n"
                        f"Grade Point: {subject[9]}"
                    )

                    return

            messagebox.showerror(
                "Search",
                "Subject not found."
            )

        ctk.CTkButton(
            window,
            text="Search",
            command=search
        ).pack(pady=30)

    # ---------------- EDIT ----------------

    def edit_subject(self):

        subjects = database.get_subjects()

        if not subjects:

            messagebox.showinfo(
                "Edit",
                "No subjects available."
            )

            return

        window = ctk.CTkToplevel(self)

        window.title("Edit Subject")
        window.geometry("450x400")

        ctk.CTkLabel(
            window,
            text="Select Subject"
        ).pack(pady=(20, 5))

        subject_names = [
            f"{row[0]} - {row[1]}"
            for row in subjects
        ]

        selected = ctk.CTkComboBox(
            window,
            values=subject_names,
            width=300
        )

        selected.pack()

        ctk.CTkLabel(
            window,
            text="New Name"
        ).pack(pady=(20, 5))

        name_entry = ctk.CTkEntry(
            window,
            width=300
        )

        name_entry.pack()

        ctk.CTkLabel(
            window,
            text="New Credits"
        ).pack(pady=(20, 5))

        credits_entry = ctk.CTkEntry(
            window,
            width=300
        )

        credits_entry.pack()

        def save():

            try:

                subject_id = int(
                    selected.get().split(" - ")[0]
                )

                name = name_entry.get().strip()
                credits = int(
                    credits_entry.get()
                )

                if not name or credits <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Enter valid details."
                )

                return

            database.update_subject(
                subject_id,
                name,
                credits
            )

            window.destroy()

            self.refresh_dashboard()

        ctk.CTkButton(
            window,
            text="Save Changes",
            command=save
        ).pack(pady=30)

    # ---------------- DELETE ----------------

    def delete_subject(self):

        subjects = database.get_subjects()

        if not subjects:

            messagebox.showinfo(
                "Delete",
                "No subjects available."
            )

            return

        window = ctk.CTkToplevel(self)

        window.title("Delete Subject")
        window.geometry("400x300")

        ctk.CTkLabel(
            window,
            text="Select Subject"
        ).pack(pady=(30, 5))

        subject_names = [
            f"{row[0]} - {row[1]}"
            for row in subjects
        ]

        selected = ctk.CTkComboBox(
            window,
            values=subject_names,
            width=300
        )

        selected.pack()

        def delete():

            try:

                subject_id = int(
                    selected.get().split(" - ")[0]
                )

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Select a subject."
                )

                return

            if not messagebox.askyesno(
                "Confirm",
                "Delete this subject?"
            ):
                return

            database.delete_subject(
                subject_id
            )

            window.destroy()

            self.refresh_dashboard()

        ctk.CTkButton(
            window,
            text="Delete Subject",
            command=delete
        ).pack(pady=30)

    # ---------------- ATTENDANCE REPORT ----------------

    def attendance_report(self):

        subjects = database.get_subjects()

        if not subjects:

            messagebox.showinfo(
                "Report",
                "No subjects available."
            )

            return

        report = ""

        for subject in subjects:

            name = subject[1]
            conducted = subject[3]
            attended = subject[4]

            if conducted > 0:

                percentage = round(
                    attended / conducted * 100,
                    2
                )

            else:

                percentage = 0

            if percentage >= 75:

                status = "Safe"

            else:

                status = "Shortage"

            report += (
                f"{name}\n"
                f"Attendance: {percentage}%\n"
                f"Status: {status}\n\n"
            )

        messagebox.showinfo(
            "Attendance Report",
            report
        )

    # ---------------- SGPA ----------------

    def calculate_sgpa(self):

        subjects = database.get_subjects()

        if not subjects:

            messagebox.showinfo(
                "SGPA",
                "No subjects available."
            )

            return

        total_points = 0
        total_credits = 0

        for subject in subjects:

            credits = subject[2]
            grade_point = subject[9]

            if grade_point is None:

                messagebox.showerror(
                    "SGPA",
                    f"Grade point missing for {subject[1]}."
                )

                return

            total_points += (
                credits * grade_point
            )

            total_credits += credits

        sgpa = round(
            total_points / total_credits,
            2
        )

        messagebox.showinfo(
            "SGPA",
            f"Your SGPA is {sgpa}"
        )


if __name__ == "__main__":
    app = CollegeManager()
    app.mainloop()

