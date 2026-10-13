# Student Record Management API (EWB Edu Tech Internship)

A clean, robust, and production-grade RESTful backend for managing student records, built using **Python**, **FastAPI**, and **SQLite**.

---

## 📌 Features

- **CRUD Operations**:
  - `POST /students`: Create a new student with validation.
  - `GET /students`: List students with optional query filters (name, email, course, date of birth) and pagination (`limit`, `offset`).
  - `GET /students/{student_id}`: Retrieve a specific student record by ID.
  - `PUT /students/{student_id}`: Update an entire student record.
  - `PATCH /students/{student_id}`: Partially update student fields.
  - `DELETE /students/{student_id}`: Delete a student record.
- **Data Validation & Integrity**:
  - Pydantic models with strict field validation (ISO date checking, email regex, phone formatting, birth dates in the past).
  - Enforces duplicate prevention for primary ID (`student_id`) and unique `email`.
  - At least one contact method (email or phone) is mandatory.
- **SQLite Persistence**:
  - Pure SQLite persistent database (`students.db`) using safe parameterized queries to prevent SQL injection.
- **Interactive Documentation**:
  - Automatic OpenAPI / Swagger UI at `/docs` and ReDoc at `/redoc`.
- **Sample Data**:
  - Seed script provided with safe mock/dummy records.

---

## 🛠️ Prerequisites

- **Python 3.10+** (Tested on Python 3.10 through 3.14)
- **pip** (Python package manager)

---

## 🚀 Getting Started

### 1. Clone or Open the Repository
```bash
git clone <repository_url>
cd internship
```

### 2. Create and Activate a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🏃 Running the Application

### Start the Server
Run the FastAPI development server with Uvicorn:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Once running:
- **API Root / Health Check**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Seeding Sample Data

To populate the database with safe, realistic sample student records:
```bash
python seed_data.py
```

---

## 📖 API Endpoints & Example Requests

### 1. Create a Student
**Request:**
- **POST** `/students`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "student_id": "STU1001",
  "name": "Aarav Sharma",
  "date_of_birth": "2002-05-14",
  "email": "aarav.sharma@example.com",
  "phone": "+919876543210",
  "course": "Computer Science & Engineering",
  "address": "45 MG Road, Bengaluru, Karnataka",
  "enrollment_date": "2023-08-01"
}
```
**Response (201 Created):**
```json
{
  "student_id": "STU1001",
  "name": "Aarav Sharma",
  "date_of_birth": "2002-05-14",
  "email": "aarav.sharma@example.com",
  "phone": "+919876543210",
  "course": "Computer Science & Engineering",
  "address": "45 MG Road, Bengaluru, Karnataka",
  "enrollment_date": "2023-08-01",
  "created_at": "2026-10-13 15:30:00",
  "updated_at": "2026-10-13 15:30:00"
}
```

### 2. List Students (with Filtering)
- **GET** `/students`
- **GET** `/students?name=Aarav`
- **GET** `/students?course=Computer&limit=10&offset=0`

### 3. Retrieve Single Student
- **GET** `/students/STU1001`
- Returns `200 OK` or `404 Not Found` if missing.

### 4. Full Update
- **PUT** `/students/STU1001`
- Replaces all mutable fields for that student.

### 5. Partial Update (Patch)
- **PATCH** `/students/STU1001`
- **Body:**
```json
{
  "course": "Artificial Intelligence & Data Science"
}
```

### 6. Delete a Student
- **DELETE** `/students/STU1001`
- **Response (200 OK):**
```json
{
  "message": "Student 'STU1001' deleted successfully.",
  "student_id": "STU1001"
}
```

---

## 🧪 Running Automated Tests

A comprehensive test suite is provided in `test_main.py` using `pytest`. The tests run against an isolated temporary SQLite database so that local application data is never touched.

Execute tests using:
```bash
python -m pytest test_main.py -v
```

---

## 🗂️ Project Structure

```text
├── main.py           # FastAPI application entrypoint and route handlers
├── models.py         # Pydantic schemas, validation rules, and response models
├── crud.py           # SQLite database queries and parameterized CRUD helpers
├── database.py       # SQLite connection manager and table initialization
├── seed_data.py      # Dummy data seeding script
├── test_main.py      # Automated test suite (CRUD, validations, persistence)
├── requirements.txt  # Project dependencies
├── .gitignore        # Git ignore rules for virtual environments, DBs, and caches
└── README.md         # Documentation and setup instructions
```

---

## 🤖 Optional AI Extension (Note)
In accordance with system specifications, AI extensions (such as local Ollama / LLM integrations for automated student feedback or query synthesis) remain an optional, modular extension. The current core architecture is decoupled such that an AI service module can be attached directly into `main.py` without requiring database changes.
