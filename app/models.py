from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(String(20), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    major = Column(String(100), nullable=False)
    tuition = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0.0)
    status = Column(String(20), default="Unpaid")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String(20), ForeignKey("students.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())