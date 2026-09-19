from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=dict)
def read_students(
    search: Optional[str] = "",
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    db: Session = Depends(get_db)
):
    total, students = crud.get_students(db, search=search, skip=skip, limit=limit)
    return {"total": total, "students": students}

@router.post("/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    if crud.get_student_by_id(db, student.id):
        raise HTTPException(status_code=400, detail="Mã sinh viên đã tồn tại")
    return crud.create_student(db=db, student=student)

@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: str, student_data: schemas.StudentUpdate, db: Session = Depends(get_db)):
    updated = crud.update_student(db=db, student_id=student_id, student_data=student_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
    return updated

@router.delete("/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    if not crud.delete_student(db=db, student_id=student_id):
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
    return {"message": "Đã xóa sinh viên"}