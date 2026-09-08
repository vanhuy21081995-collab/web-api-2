from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/statistics", tags=["Statistics API"])

@router.get("", response_model=schemas.StatisticsResponse)
def get_statistics(db: Session = Depends(get_db)):
    total_students = db.query(models.Student).count()
    paid_students = db.query(models.Student).filter(models.Student.status == "Paid").count()
    partial_students = db.query(models.Student).filter(models.Student.status == "Partial").count()
    unpaid_students = db.query(models.Student).filter(models.Student.status == "Unpaid").count()

    total_tuition = db.query(func.sum(models.Student.tuition)).scalar() or 0.0
    total_collected = db.query(func.sum(models.Student.paid_amount)).scalar() or 0.0
    total_remaining = total_tuition - total_collected

    return {
        "total_students": total_students,
        "paid_students": paid_students,
        "partial_students": partial_students,
        "unpaid_students": unpaid_students,
        "total_tuition": total_tuition,
        "total_collected": total_collected,
        "total_remaining": total_remaining,
    }