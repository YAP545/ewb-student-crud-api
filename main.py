import sqlite3
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse

from database import init_db, get_db
from models import StudentCreate, StudentUpdate, StudentPatch, StudentResponse
import crud

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database schema on startup
    init_db()
    yield

app = FastAPI(
    title="Student Record Management API",
    description="EWB Edu Tech Internship Project - Student CRUD Backend built with FastAPI and SQLite.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "service": "Student Record Management API",
        "docs_url": "/docs"
    }

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
    summary="Create a new student record"
)
def create_student_endpoint(
    student: StudentCreate,
    conn: sqlite3.Connection = Depends(get_db)
):
    # Check if student ID already exists
    existing_id = crud.get_student_by_id(conn, student.student_id)
    if existing_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Student with ID '{student.student_id}' already exists."
        )

    # Check if email already exists
    if student.email:
        existing_email = crud.get_student_by_email(conn, student.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Student with email '{student.email}' is already registered."
            )

    created = crud.create_student(conn, student)
    return created

@app.get(
    "/students",
    response_model=List[StudentResponse],
    tags=["Students"],
    summary="List students with optional filters"
)
def list_students_endpoint(
    name: Optional[str] = Query(None, description="Filter by student name (partial match)"),
    email: Optional[str] = Query(None, description="Filter by email (partial match)"),
    course: Optional[str] = Query(None, description="Filter by course name (partial match)"),
    date_of_birth: Optional[str] = Query(None, description="Filter by exact birth date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    conn: sqlite3.Connection = Depends(get_db)
):
    students = crud.list_students(
        conn,
        name=name,
        email=email,
        course=course,
        date_of_birth=date_of_birth,
        limit=limit,
        offset=offset
    )
    return students

@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"],
    summary="Retrieve a specific student by ID"
)
def get_student_endpoint(
    student_id: str,
    conn: sqlite3.Connection = Depends(get_db)
):
    student = crud.get_student_by_id(conn, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID '{student_id}' not found."
        )
    return student

@app.put(
    "/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"],
    summary="Update an existing student (full update)"
)
def update_student_endpoint(
    student_id: str,
    student: StudentUpdate,
    conn: sqlite3.Connection = Depends(get_db)
):
    # Verify student exists
    existing = crud.get_student_by_id(conn, student_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID '{student_id}' not found."
        )

    # Check for email conflict with another student
    if student.email:
        email_owner = crud.get_student_by_email(conn, student.email)
        if email_owner and email_owner["student_id"] != student_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{student.email}' is already taken by another student."
            )

    updated = crud.update_student(conn, student_id, student)
    return updated

@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"],
    summary="Partially update an existing student record"
)
def patch_student_endpoint(
    student_id: str,
    student_patch: StudentPatch,
    conn: sqlite3.Connection = Depends(get_db)
):
    existing = crud.get_student_by_id(conn, student_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID '{student_id}' not found."
        )

    if student_patch.email:
        email_owner = crud.get_student_by_email(conn, student_patch.email)
        if email_owner and email_owner["student_id"] != student_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{student_patch.email}' is already taken by another student."
            )

    updated = crud.patch_student(conn, student_id, student_patch)
    return updated

@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_200_OK,
    tags=["Students"],
    summary="Delete a student record"
)
def delete_student_endpoint(
    student_id: str,
    conn: sqlite3.Connection = Depends(get_db)
):
    existing = crud.get_student_by_id(conn, student_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID '{student_id}' not found."
        )

    deleted = crud.delete_student(conn, student_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete student record."
        )

    return {"message": f"Student '{student_id}' deleted successfully.", "student_id": student_id}
