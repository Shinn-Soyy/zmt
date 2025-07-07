from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    telegram_id: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    balance: float
    mining_rate: float
    is_mining: bool
    referral_code: str
    total_referrals: int
    daily_login_streak: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class MiningStart(BaseModel):
    pass

class MiningClaim(BaseModel):
    pass

class PurchaseBoost(BaseModel):
    boost_level: int

class ExchangeRequest(BaseModel):
    zmt_amount: float

class ExchangeResponse(BaseModel):
    id: int
    zmt_amount: float
    mmk_amount: float
    fee_amount: float
    exchange_code: str
    status: str
    created_at: datetime

class DailyTaskClaim(BaseModel):
    task_type: str

class ReferralUse(BaseModel):
    referral_code: str
