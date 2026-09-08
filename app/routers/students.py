from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/students", tags=["Students API"])

@router.get("")
def read_students(
    search: str = Query("", description="Tìm kiếm theo Mã SV hoặc Tên"),
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    total, students = crud.get_students(db, search=search, skip=skip, limit=limit)
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "data": students
    }

@router.post("", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_id(db, student.id)
    if db_student:
        raise HTTPException(status_code=400, detail="Mã sinh viên đã tồn tại!")
    return crud.create_student(db, student)

@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: str, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    updated = crud.update_student(db, student_id, student)
    if not updated:
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên!")
    return updated

@router.delete("/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    success = crud.delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên!")
    return {"message": "Xóa sinh viên thành công!"}