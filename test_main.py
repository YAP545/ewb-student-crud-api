import os
import unittest
from fastapi.testclient import TestClient

TEST_DB = "test_students_runner.db"
os.environ["STUDENT_DB_PATH"] = TEST_DB

from database import init_db, get_connection, get_db
from models import StudentCreate
import crud
from main import app

class StudentAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Override FastAPI get_db dependency
        def override_get_db():
            conn = get_connection(TEST_DB)
            try:
                yield conn
            finally:
                conn.close()
        app.dependency_overrides[get_db] = override_get_db

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except PermissionError:
                pass

    def setUp(self):
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except PermissionError:
                pass
        init_db(TEST_DB)
        self.client = TestClient(app)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except PermissionError:
                pass

    def test_01_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")

    def test_02_create_student_success(self):
        payload = {
            "student_id": "STU101",
            "name": "Aarav Sharma",
            "date_of_birth": "2002-05-15",
            "email": "aarav.sharma@example.com",
            "phone": "+919876543210",
            "course": "Computer Science",
            "address": "123 MG Road, Bengaluru",
            "enrollment_date": "2024-08-01"
        }
        response = self.client.post("/students", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["student_id"], "STU101")
        self.assertEqual(data["name"], "Aarav Sharma")
        self.assertEqual(data["email"], "aarav.sharma@example.com")

    def test_03_create_duplicate_student_id(self):
        payload = {
            "student_id": "STU102",
            "name": "Priya Patel",
            "date_of_birth": "2003-01-20",
            "email": "priya.patel@example.com",
            "phone": "+919876543211"
        }
        res1 = self.client.post("/students", json=payload)
        self.assertEqual(res1.status_code, 201)

        payload2 = {
            "student_id": "STU102",
            "name": "Another Priya",
            "date_of_birth": "2003-01-20",
            "email": "different@example.com",
            "phone": "+919876543212"
        }
        res2 = self.client.post("/students", json=payload2)
        self.assertEqual(res2.status_code, 409)
        self.assertIn("already exists", res2.json()["detail"])

    def test_04_create_duplicate_email(self):
        payload1 = {
            "student_id": "STU103",
            "name": "Rohan Verma",
            "date_of_birth": "2001-11-10",
            "email": "common@example.com",
            "phone": "+919876543213"
        }
        self.client.post("/students", json=payload1)

        payload2 = {
            "student_id": "STU104",
            "name": "Rohit Verma",
            "date_of_birth": "2001-11-10",
            "email": "common@example.com",
            "phone": "+919876543214"
        }
        res = self.client.post("/students", json=payload2)
        self.assertEqual(res.status_code, 409)
        self.assertIn("already registered", res.json()["detail"])

    def test_05_validation_missing_contact_method(self):
        payload = {
            "student_id": "STU105",
            "name": "Neha Gupta",
            "date_of_birth": "2002-07-25"
        }
        response = self.client.post("/students", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_06_validation_future_date_of_birth(self):
        payload = {
            "student_id": "STU106",
            "name": "Future Student",
            "date_of_birth": "2099-01-01",
            "email": "future@example.com"
        }
        response = self.client.post("/students", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_07_get_students_list_and_filters(self):
        s1 = {
            "student_id": "STU201",
            "name": "Ananya Roy",
            "date_of_birth": "2002-03-12",
            "email": "ananya@example.com",
            "course": "Mechanical Engineering"
        }
        s2 = {
            "student_id": "STU202",
            "name": "Kavita Rao",
            "date_of_birth": "2003-08-22",
            "email": "kavita@example.com",
            "course": "Computer Science"
        }
        self.client.post("/students", json=s1)
        self.client.post("/students", json=s2)

        # List all
        all_res = self.client.get("/students")
        self.assertEqual(all_res.status_code, 200)
        self.assertGreaterEqual(len(all_res.json()), 2)

        # Filter by name
        name_res = self.client.get("/students?name=Ananya")
        self.assertEqual(len(name_res.json()), 1)
        self.assertEqual(name_res.json()[0]["student_id"], "STU201")

        # Filter by course
        course_res = self.client.get("/students?course=Computer")
        self.assertEqual(len(course_res.json()), 1)
        self.assertEqual(course_res.json()[0]["student_id"], "STU202")

        # Filter by date_of_birth
        dob_res = self.client.get("/students?date_of_birth=2002-03-12")
        self.assertEqual(len(dob_res.json()), 1)
        self.assertEqual(dob_res.json()[0]["student_id"], "STU201")

    def test_08_get_student_by_id_and_not_found(self):
        s = {
            "student_id": "STU301",
            "name": "Dev Mishra",
            "date_of_birth": "2001-09-09",
            "email": "dev@example.com"
        }
        self.client.post("/students", json=s)

        res = self.client.get("/students/STU301")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["name"], "Dev Mishra")

        not_found = self.client.get("/students/NON_EXISTENT")
        self.assertEqual(not_found.status_code, 404)
        self.assertIn("not found", not_found.json()["detail"])

    def test_09_update_student_put(self):
        s = {
            "student_id": "STU401",
            "name": "Original Name",
            "date_of_birth": "2000-01-01",
            "email": "orig@example.com"
        }
        self.client.post("/students", json=s)

        update_payload = {
            "name": "Updated Name",
            "date_of_birth": "2000-01-01",
            "email": "updated@example.com",
            "phone": "+919999988888",
            "course": "AI & ML",
            "address": "456 Tech Park",
            "enrollment_date": "2024-01-15"
        }
        res = self.client.put("/students/STU401", json=update_payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["name"], "Updated Name")
        self.assertEqual(res.json()["course"], "AI & ML")

        res_404 = self.client.put("/students/NON_EXISTENT", json=update_payload)
        self.assertEqual(res_404.status_code, 404)

    def test_10_patch_student(self):
        s = {
            "student_id": "STU501",
            "name": "Vikram Seth",
            "date_of_birth": "2002-04-04",
            "email": "vikram@example.com",
            "course": "History"
        }
        self.client.post("/students", json=s)

        patch_res = self.client.patch("/students/STU501", json={"course": "Literature"})
        self.assertEqual(patch_res.status_code, 200)
        self.assertEqual(patch_res.json()["course"], "Literature")
        self.assertEqual(patch_res.json()["name"], "Vikram Seth")

    def test_11_delete_student(self):
        s = {
            "student_id": "STU601",
            "name": "To Delete",
            "date_of_birth": "2000-12-12",
            "email": "delete_me@example.com"
        }
        self.client.post("/students", json=s)

        del_res = self.client.delete("/students/STU601")
        self.assertEqual(del_res.status_code, 200)

        get_res = self.client.get("/students/STU601")
        self.assertEqual(get_res.status_code, 404)

        del_404 = self.client.delete("/students/STU601")
        self.assertEqual(del_404.status_code, 404)

    def test_12_sqlite_persistence_verification(self):
        test_db_file = "test_persistence_manual.db"
        if os.path.exists(test_db_file):
            try:
                os.remove(test_db_file)
            except PermissionError:
                pass

        init_db(test_db_file)
        conn = get_connection(test_db_file)

        student_data = StudentCreate(
            student_id="PERSIST_1",
            name="Persistence Tester",
            date_of_birth="2001-02-03",
            email="persist@example.com",
            course="Data Science"
        )
        crud.create_student(conn, student_data)
        conn.close()

        # Reopen connection from disk
        conn2 = get_connection(test_db_file)
        persisted = crud.get_student_by_id(conn2, "PERSIST_1")
        conn2.close()

        self.assertIsNotNone(persisted)
        self.assertEqual(persisted["name"], "Persistence Tester")

        if os.path.exists(test_db_file):
            try:
                os.remove(test_db_file)
            except PermissionError:
                pass

if __name__ == "__main__":
    unittest.main()
