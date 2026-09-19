from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StudentBase(BaseModel):
    name: str
    email: str
    major: str
    tuition: float

class StudentCreate(StudentBase):
    id: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    major: Optional[str] = None
    tuition: Optional[float] = None

class StudentResponse(StudentBase):
    id: str
    paid_amount: float
    status: str

    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    student_id: str
    amount: float
    payment_method: str

class PaymentResponse(BaseModel):
    id: int
    student_id: str
    amount: float
    payment_method: str
    created_at: datetime

    class Config:
        from_attributes = True

class StatisticsResponse(BaseModel):
    total_students: int
    paid_students: int
    partial_students: int
    unpaid_students: int
    total_tuition: float
    total_collected: float
    total_remaining: float

    class Config:
        from_attributes = True