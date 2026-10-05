import sqlite3
import os

DATABASE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "college_manager.db"
)


def connect():
    return sqlite3.connect(DATABASE)


def create_table():
    connection = connect()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            credits INTEGER NOT NULL,
            classes_conducted INTEGER DEFAULT 0,
            classes_attended INTEGER DEFAULT 0,
            ia1 REAL,
            ia2 REAL,
            ia3 REAL,
            see_marks REAL,
            grade_point REAL
        )
    """)

    connection.commit()
    connection.close()


def add_subject(name, credits):
    connection = connect()

    connection.execute("""
        INSERT INTO subjects (name, credits)
        VALUES (?, ?)
    """, (name, credits))

    connection.commit()
    connection.close()


def get_subjects():
    connection = connect()

    rows = connection.execute("""
        SELECT * FROM subjects
        ORDER BY id
    """).fetchall()

    connection.close()

    return rows


def update_attendance(subject_id, conducted, attended):
    connection = connect()

    connection.execute("""
        UPDATE subjects
        SET classes_conducted = ?,
            classes_attended = ?
        WHERE id = ?
    """, (conducted, attended, subject_id))

    connection.commit()
    connection.close()


def update_marks(
    subject_id,
    ia1,
    ia2,
    ia3,
    see_marks,
    grade_point
):
    connection = connect()

    connection.execute("""
        UPDATE subjects
        SET ia1 = ?,
            ia2 = ?,
            ia3 = ?,
            see_marks = ?,
            grade_point = ?
        WHERE id = ?
    """, (
        ia1,
        ia2,
        ia3,
        see_marks,
        grade_point,
        subject_id
    ))

    connection.commit()
    connection.close()


def update_subject(subject_id, name, credits):
    connection = connect()

    connection.execute("""
        UPDATE subjects
        SET name = ?,
            credits = ?
        WHERE id = ?
    """, (name, credits, subject_id))

    connection.commit()
    connection.close()


def delete_subject(subject_id):
    connection = connect()

    connection.execute(
        "DELETE FROM subjects WHERE id = ?",
        (subject_id,)
    )

    connection.commit()
    connection.close()


create_table()