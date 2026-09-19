from pydantic import BaseModel, EmailStr
from typing import Optional
class StudentBase(BaseModel):
    id: str
    name: str
    email: EmailStr
    major: str
    tuition: float

class StudentCreate(StudentBase)
    pass

class StudentUpdate(BaseModel)
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    tuition: Optional[float] = None
    paid_amount: Optional[float] = None
    
class StudentResponse(StudentBase)
    paid_amount: float
    status: str
    class Config:
        from_attributes = True