import sqlite3
from typing import List, Optional
from models import StudentCreate, StudentUpdate, StudentPatch

def get_student_by_id(conn: sqlite3.Connection, student_id: str) -> Optional[dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    if row:
        return dict(row)
    return None

def get_student_by_email(conn: sqlite3.Connection, email: str) -> Optional[dict]:
    if not email:
        return None
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE LOWER(email) = LOWER(?)", (email.strip(),))
    row = cursor.fetchone()
    if row:
        return dict(row)
    return None

def list_students(
    conn: sqlite3.Connection,
    name: Optional[str] = None,
    email: Optional[str] = None,
    course: Optional[str] = None,
    date_of_birth: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> List[dict]:
    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name.strip()}%")
    if email:
        query += " AND email LIKE ?"
        params.append(f"%{email.strip()}%")
    if course:
        query += " AND course LIKE ?"
        params.append(f"%{course.strip()}%")
    if date_of_birth:
        query += " AND date_of_birth = ?"
        params.append(date_of_birth.strip())

    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor = conn.cursor()
    cursor.execute(query, params)
    return [dict(row) for row in cursor.fetchall()]

def create_student(conn: sqlite3.Connection, student: StudentCreate) -> dict:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO students (
            student_id, name, date_of_birth, email, phone, course, address, enrollment_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student.student_id,
            student.name,
            student.date_of_birth,
            student.email,
            student.phone,
            student.course,
            student.address,
            student.enrollment_date,
        ),
    )
    conn.commit()
    return get_student_by_id(conn, student.student_id)

def update_student(conn: sqlite3.Connection, student_id: str, student: StudentUpdate) -> Optional[dict]:
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE students
        SET name = ?,
            date_of_birth = ?,
            email = ?,
            phone = ?,
            course = ?,
            address = ?,
            enrollment_date = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE student_id = ?
        """,
        (
            student.name,
            student.date_of_birth,
            student.email,
            student.phone,
            student.course,
            student.address,
            student.enrollment_date,
            student_id,
        ),
    )
    conn.commit()
    if cursor.rowcount == 0:
        return None
    return get_student_by_id(conn, student_id)

def patch_student(conn: sqlite3.Connection, student_id: str, student_patch: StudentPatch) -> Optional[dict]:
    update_data = student_patch.model_dump(exclude_unset=True)
    if not update_data:
        return get_student_by_id(conn, student_id)

    clauses = []
    values = []
    for key, value in update_data.items():
        clauses.append(f"{key} = ?")
        values.append(value)

    clauses.append("updated_at = CURRENT_TIMESTAMP")
    values.append(student_id)

    query = f"UPDATE students SET {', '.join(clauses)} WHERE student_id = ?"
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount == 0:
        return None
    return get_student_by_id(conn, student_id)

def delete_student(conn: sqlite3.Connection, student_id: str) -> bool:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    return cursor.rowcount > 0
