from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy.orm import Session
import bcrypt
import os

from database import SessionLocal, engine
from model import User
import model

# Create DB tables
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Schemas ---
class RegisterRequest(BaseModel):
    firstname: str
    middlename: Optional[str] = None
    lastname: str
    email: EmailStr
    password: str

class RegisterResponse(BaseModel):
    message: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str
    user: dict

class PredictRequest(BaseModel):
    bedrooms: int
    bathrooms: int
    area: float
    age: int

class PredictResponse(BaseModel):
    price: float

# --- Routes ---
@app.post("/api/register", response_model=RegisterResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(
        firstname=req.firstname,
        middlename=req.middlename,
        lastname=req.lastname,
        email=req.email,
        password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return RegisterResponse(message="Registration successful")

@app.post("/api/login", response_model=LoginResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not bcrypt.checkpw(req.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user": {
            "firstname": user.firstname,
            "middlename": user.middlename,
            "lastname": user.lastname,
            "email": user.email
        }
    }

@app.post("/api/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    base_price = 50000
    price = base_price + (req.bedrooms * 20000) + (req.bathrooms * 15000) + (req.area * 100) - (req.age * 1000)
    return {"price": round(price, 2)}

# --- Serve frontend ---
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path, html=True), name="static")

# Optional: redirect root to index.html
@app.get("/")
def root():
    return RedirectResponse("/static/index.html")
