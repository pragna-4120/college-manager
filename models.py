from pydantic import BaseModel


class Subject(BaseModel):
    name: str
    credits: int

    classes_conducted: int = 0
    classes_attended: int = 0

    ia1: float | None = None
    ia2: float | None = None
    ia3: float | None = None

    see_marks: float | None = None
    grade_point: float | None = None

    def attendance_percentage(self):
        if self.classes_conducted == 0:
            return 0

        return round(
            (self.classes_attended / self.classes_conducted) * 100,
            2
        )

    def attendance_status(self):
        if self.classes_conducted == 0:
            return "No attendance data"

        if self.attendance_percentage() >= 75:
            return "Safe"

        return "Shortage"

    def classes_needed_for_75(self):
        if self.classes_conducted == 0:
            return 0

        if self.attendance_percentage() >= 75:
            return 0

        additional_classes = 0

        while (
            (self.classes_attended + additional_classes)
            / (self.classes_conducted + additional_classes)
        ) * 100 < 75:
            additional_classes += 1

        return additional_classes

    def ia_average(self):
        marks = [self.ia1, self.ia2, self.ia3]
        marks = [mark for mark in marks if mark is not None]

        if not marks:
            return 0

        if len(marks) >= 2:
            marks = sorted(marks, reverse=True)[:2]

        return round(sum(marks) / len(marks), 2)

    def calculate_grade_point(self):
        total = self.ia_average() + (self.see_marks or 0)

        if total >= 90:
            return 10
        elif total >= 80:
            return 9
        elif total >= 70:
            return 8
        elif total >= 60:
            return 7
        elif total >= 50:
            return 6
        elif total >= 40:
            return 5
        else:
            return 0