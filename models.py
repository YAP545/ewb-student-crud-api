import re
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Full name of the student")
    date_of_birth: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    email: Optional[str] = Field(None, max_length=100, description="Student email address")
    phone: Optional[str] = Field(None, max_length=20, description="Student phone number")
    course: Optional[str] = Field(None, max_length=100, description="Enrolled course name")
    address: Optional[str] = Field(None, max_length=250, description="Residential address")
    enrollment_date: Optional[str] = Field(None, description="Enrollment date in YYYY-MM-DD format")

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v: str) -> str:
        try:
            parsed_date = date.fromisoformat(v)
            if parsed_date > date.today():
                raise ValueError("Date of birth cannot be in the future")
        except ValueError as err:
            raise ValueError(f"Invalid date format for date_of_birth. Expected YYYY-MM-DD ({err})")
        return v

    @field_validator("enrollment_date")
    @classmethod
    def validate_enrollment(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                date.fromisoformat(v)
            except ValueError:
                raise ValueError("Invalid date format for enrollment_date. Expected YYYY-MM-DD")
        return v

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip().lower()
            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(pattern, v):
                raise ValueError("Invalid email address format")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone_format(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            digits = re.sub(r"[^\d+]", "", v)
            if len(digits) < 7:
                raise ValueError("Phone number must contain at least 7 digits")
        return v

class StudentCreate(StudentBase):
    student_id: str = Field(..., min_length=1, max_length=50, description="Unique identifier for the student")

    @model_validator(mode="after")
    def check_contact_provided(self):
        if not self.email and not self.phone:
            raise ValueError("At least one contact method (email or phone) must be provided.")
        return self

class StudentUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: str = Field(...)
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[str] = None

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v: str) -> str:
        try:
            parsed_date = date.fromisoformat(v)
            if parsed_date > date.today():
                raise ValueError("Date of birth cannot be in the future")
        except ValueError as err:
            raise ValueError(f"Invalid date format for date_of_birth. Expected YYYY-MM-DD ({err})")
        return v

    @field_validator("enrollment_date")
    @classmethod
    def validate_enrollment(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                date.fromisoformat(v)
            except ValueError:
                raise ValueError("Invalid date format for enrollment_date. Expected YYYY-MM-DD")
        return v

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip().lower()
            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(pattern, v):
                raise ValueError("Invalid email address format")
        return v

    @model_validator(mode="after")
    def check_contact_provided(self):
        if not self.email and not self.phone:
            raise ValueError("At least one contact method (email or phone) must be provided.")
        return self

class StudentPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[str] = None

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                parsed_date = date.fromisoformat(v)
                if parsed_date > date.today():
                    raise ValueError("Date of birth cannot be in the future")
            except ValueError as err:
                raise ValueError(f"Invalid date format for date_of_birth. Expected YYYY-MM-DD ({err})")
        return v

    @field_validator("enrollment_date")
    @classmethod
    def validate_enrollment(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            try:
                date.fromisoformat(v)
            except ValueError:
                raise ValueError("Invalid date format for enrollment_date. Expected YYYY-MM-DD")
        return v

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip().lower()
            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(pattern, v):
                raise ValueError("Invalid email address format")
        return v

class StudentResponse(BaseModel):
    student_id: str
    name: str
    date_of_birth: str
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
