"""
Run: python seed.py
Seeds the database with sample halls, students, and exams.
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_seating.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from seating.models import Hall, Exam, Student
from datetime import date, time

print(" Seeding database...")

# Halls
h1, _ = Hall.objects.get_or_create(name="LEC-15", defaults={"rows": 9, "columns": 3})
h2, _ = Hall.objects.get_or_create(name="LEC-16", defaults={"rows": 4, "columns": 5})
h3, _ = Hall.objects.get_or_create(name="ED-HALL", defaults={"rows": 15, "columns": 5})
print(f"   Created {Hall.objects.count()} halls")

# Students
students_data = [
    ("22301", "Abhishek Jaiswal", "Computer Science", ""),
    ("22302", "Abu Bakar", "Computer Science", ""),
    ("22303", "Aman Rawat", "Computer Science", ""),
    ("22101", " Md Mazish", "Civil", ""),
    ("22102", "Ram Karan", "Civil", ""),
    ("22103", "Yuvraj Singh", "Civil", ""),
    ("22201", "Azim Ahmad", "Mechanical", ""),
    ("22202", "Atique Ahmad", "Mechanical", ""),
    ("22203", "Muzaffar Ehsan", "Mechanical", ""),
    ("22401", "Azmatullah(Epm.)", "OTT", ""),
    ("22402", "Amit Kumar","OTT", ""),
    ("22403", "Ujala parween","OTT", ""),
    ("22701", "Nabeel warsi(Emp.)", "BCA", ""),
    ("22702", "Hamid(Emp.)","BCA",""),
    ("22703", "Ankit Kumar","BCA",""),
    ("22801", "Shahwaj Alam", "RIT", ""),
    ("22802", "Shahid(Romeo)", "RIT", ""),
    ("22803", "Rizwan(Emp.)", "RIT", ""),
    ("22370", "Zishan Ahmad", "Computer Science", ""),
    ("22375","Tauqeer Alam", "Computer Science", "")
]
for roll, name, dept, email in students_data:
    Student.objects.get_or_create(roll_number=roll, defaults={"name": name, "department": dept, "email": email})
print(f" Created {Student.objects.count()} students")

# Exams
e1, _ = Exam.objects.get_or_create(
    name="Data Structures & Algorithms", date=date(2025, 6, 10),
    defaults={"time": time(9, 0), "hall": h1}
)
e2, _ = Exam.objects.get_or_create(
    name="Digital Electronics", date=date(2025, 6, 12),
    defaults={"time": time(14, 0), "hall": h2}
)
e3, _ = Exam.objects.get_or_create(
    name="Engineering Mathematics-1", date=date(2025, 6, 15),
    defaults={"time": time(9, 30), "hall": h1}
)
print(f"   Created {Exam.objects.count()} exams")

print("   Database seeded successfully!")
print("   Run: python manage.py runserver")
print("   Open: http://127.0.0.1:8000")
