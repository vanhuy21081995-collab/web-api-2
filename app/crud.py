from sqlalchemy.orm import Session
from app import models, schemas
def get_student_by_id(db: Session, student_id: str):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_students(db: Session, search: str = "", skip: int = 0, limit: int = 100):
    query = db.query(models.Student)
    if search:
        query = query.filter(models.Student.name.contains(search))

    total = query.count()
    students = query.order_by(models.Student.id.desc()).offset(skip).limit(limit).all()
    return total, students

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        id=student.id,
        name=student.name,
        email=student.email,
        major=student.major,
        tuition=student.tuition,
        paid_amount=0.0,
        status="Unpaid"
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: str, student_data: schemas.StudentUpdate):
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        return None
    update_data = student_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)
    if db_student.paid_amount >= db_student.tuition:
        db_student.status = "Paid"
    elif db_student.paid_amount > 0:
        db_student.status = "Partial"
    else:
        db_student.status = "Unpaid"

    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: str):
    db_student = get_student_by_id(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False