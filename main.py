from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Dummy DB substitute (you should use SQLAlchemy in real app)
users_db = {}

app = FastAPI()

# Allow frontend origin
origins = ["http://127.0.0.1:5500", "http://localhost:5500"]  # change as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security settings
SECRET_KEY = "zmtsecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Models
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserData(BaseModel):
    username: str
    email: str
    balance: float
    miningRate: float
    totalMined: float
    referralCode: str
    referrals: int
    referralEarnings: float
    loginStreak: int
    miningStartTime: Optional[int]
    miningEndTime: Optional[int]
    boostLevel: int

# Auth utils
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

# Routes
@app.post("/auth/register")
def register(user: UserRegister):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "data": {
            "username": user.username,
            "email": user.email,
            "balance": 0.0,
            "miningRate": 0.000001,
            "totalMined": 0.0,
            "referralCode": "ZMT" + user.username.upper(),
            "referrals": 0,
            "referralEarnings": 0.0,
            "loginStreak": 1,
            "miningStartTime": None,
            "miningEndTime": None,
            "boostLevel": 0
        }
    }
    return {"message": "Registered successfully"}

@app.post("/auth/login")
def login(user: UserLogin):
    db_user = users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"token": token}

def get_current_user(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid token header")
    token = auth.split(" ")[1]
    decoded = decode_token(token)
    if not decoded:
        raise HTTPException(status_code=403, detail="Invalid token")
    username = decoded.get("sub")
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/user/profile")
def get_profile(user = Depends(get_current_user)):
    return user["data"]

@app.put("/user/update")
def update_user_data(updated_data: UserData, user = Depends(get_current_user)):
    user["data"] = updated_data.dict()
    return {"message": "User data updated"}
