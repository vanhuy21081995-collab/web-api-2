from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import statistics, students

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hệ thống Quản lý Sinh viên", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router, prefix="/api")
app.include_router(statistics.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Hệ thống Quản lý Sinh viên API đang hoạt động!"}


@app.post("/")
def create_root():
    return {"message": "Dữ liệu đã được tạo (POST)"}


@app.put("/")
def update_root():
    return {"message": "Dữ liệu đã được cập nhật (PUT)"}


@app.delete("/")
def delete_root():
    return {"message": "Dữ liệu đã bị xóa (DELETE)"}