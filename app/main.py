from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import students
app = FastAPI(
    tile="API HETHONGQLSINHVIEN",
    desription="RESTful API cho ứng dụng ETHONGQLSINHVIEN dùng FastAPI và SQL Server",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)
app.include_router(students.router)