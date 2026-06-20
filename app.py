from flask import Flask, render_template, request
import csv
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

STUDENTS_FILE = os.path.join(BASE_DIR, "students.csv")
ATTENDANCE_FILE = os.path.join(BASE_DIR, "attendance.csv")


# -------------------------------
# Create CSV files if not exists
# -------------------------------
def create_files():
    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["regno", "name", "branch", "parent_mobile"])

    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "regno", "name", "status"])

create_files()


# -------------------------------
# Read students
# -------------------------------
def get_students():
    students = []
    with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append(row)
    return students


# -------------------------------
# Read attendance
# -------------------------------
def get_attendance():
    records = []
    with open(ATTENDANCE_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records


# -------------------------------
# Home page
# -------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------------------
# Add Student
# -------------------------------
@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    message = ""

    if request.method == "POST":
        regno = request.form["regno"].strip()
        name = request.form["name"].strip()
        branch = request.form["branch"].strip()
        parent_mobile = request.form["parent_mobile"].strip()

        with open(STUDENTS_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([regno, name, branch, parent_mobile])

        message = "Student added successfully!"

    return render_template("add_student.html", message=message)


# -------------------------------
# View Students
# -------------------------------
@app.route("/view_students")
def view_students():
    students = get_students()
    return render_template("view_students.html", students=students)


# -------------------------------
# Mark Attendance
# -------------------------------
@app.route("/mark_attendance", methods=["GET", "POST"])
def mark_attendance():
    students = get_students()
    message = ""

    if request.method == "POST":
        today = str(date.today())

        with open(ATTENDANCE_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            for student in students:
                regno = student["regno"]
                name = student["name"]
                status = request.form.get(regno)

                if status:
                    writer.writerow([today, regno, name, status])

        message = "Attendance saved successfully!"

    return render_template("mark_attendance.html", students=students, message=message)


# -------------------------------
# Attendance List (all present/absent)
# -------------------------------
@app.route("/attendance_list")
def attendance_list():
    records = get_attendance()
    return render_template("attendance_list.html", records=records)


# -------------------------------
# Absent Students only
# -------------------------------
@app.route("/absent_students")
def absent_students():
    records = get_attendance()
    absent_records = [row for row in records if row["status"] == "Absent"]
    return render_template("absent_students.html", absent_records=absent_records)


if __name__ == "__main__":
    app.run(debug=True)