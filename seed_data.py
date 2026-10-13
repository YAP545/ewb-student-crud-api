"""
Seed script to populate sample/dummy student records into SQLite.
Usage: python seed_data.py
"""
import os
from database import init_db, get_connection
from models import StudentCreate
import crud

SAMPLE_STUDENTS = [
    {
        "student_id": "STU1001",
        "name": "Aarav Sharma",
        "date_of_birth": "2002-05-14",
        "email": "aarav.sharma@example.com",
        "phone": "+919876543210",
        "course": "Computer Science & Engineering",
        "address": "45 MG Road, Bengaluru, Karnataka",
        "enrollment_date": "2023-08-01"
    },
    {
        "student_id": "STU1002",
        "name": "Diya Patel",
        "date_of_birth": "2003-09-22",
        "email": "diya.patel@example.com",
        "phone": "+919876543211",
        "course": "Data Science & AI",
        "address": "12 SG Highway, Ahmedabad, Gujarat",
        "enrollment_date": "2023-08-01"
    },
    {
        "student_id": "STU1003",
        "name": "Rohan Iyer",
        "date_of_birth": "2001-11-30",
        "email": "rohan.iyer@example.com",
        "phone": "+919876543212",
        "course": "Electrical Engineering",
        "address": "88 Anna Salai, Chennai, Tamil Nadu",
        "enrollment_date": "2022-07-15"
    },
    {
        "student_id": "STU1004",
        "name": "Ananya Sen",
        "date_of_birth": "2002-03-18",
        "email": "ananya.sen@example.com",
        "phone": "+919876543213",
        "course": "Computer Science & Engineering",
        "address": "21 Park Street, Kolkata, West Bengal",
        "enrollment_date": "2023-08-01"
    },
    {
        "student_id": "STU1005",
        "name": "Kabir Khan",
        "date_of_birth": "2001-07-04",
        "email": "kabir.khan@example.com",
        "phone": "+919876543214",
        "course": "Mechanical Engineering",
        "address": "10 Civil Lines, Jaipur, Rajasthan",
        "enrollment_date": "2022-07-15"
    }
]

def seed():
    print("Initializing database...")
    init_db()
    conn = get_connection()
    try:
        inserted_count = 0
        for item in SAMPLE_STUDENTS:
            existing = crud.get_student_by_id(conn, item["student_id"])
            if not existing:
                student = StudentCreate(**item)
                crud.create_student(conn, student)
                inserted_count += 1
                print(f" [+] Inserted: {item['name']} ({item['student_id']})")
            else:
                print(f" [~] Already exists: {item['student_id']}")
        print(f"\nSeeding complete! {inserted_count} new dummy records inserted.")
    finally:
        conn.close()

if __name__ == "__main__":
    seed()
