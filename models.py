from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    balance = Column(Float, default=0.0)
    mining_rate = Column(Float, default=0.000001)
    last_claim_time = Column(DateTime, default=datetime.utcnow)
    is_mining = Column(Boolean, default=False)
    referral_code = Column(String, unique=True, index=True)
    referred_by = Column(Integer, ForeignKey("users.id"))
    total_referrals = Column(Integer, default=0)
    daily_login_streak = Column(Integer, default=0)
    last_login_date = Column(DateTime, default=datetime.utcnow)
    telegram_joined = Column(Boolean, default=False)
    tiktok_shared = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    referrals = relationship("User", backref="referrer", remote_side=[id])
    mining_sessions = relationship("MiningSession", back_populates="user")
    purchases = relationship("Purchase", back_populates="user")
    exchanges = relationship("Exchange", back_populates="user")
    daily_tasks = relationship("DailyTask", back_populates="user")

class MiningSession(Base):
    __tablename__ = "mining_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    amount_mined = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    boost_level = Column(Integer, default=0)
    
    user = relationship("User", back_populates="mining_sessions")

class Purchase(Base):
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_name = Column(String)
    item_price = Column(Float)
    boost_amount = Column(Float)
    purchase_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="purchases")

class Exchange(Base):
    __tablename__ = "exchanges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    zmt_amount = Column(Float)
    mmk_amount = Column(Float)
    fee_amount = Column(Float)
    exchange_code = Column(String, unique=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="exchanges")

class DailyTask(Base):
    __tablename__ = "daily_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_type = Column(String)
    task_name = Column(String)
    reward_amount = Column(Float)
    completed_date = Column(DateTime, default=datetime.utcnow)
    is_claimed = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="daily_tasks")

class ReferralReward(Base):
    __tablename__ = "referral_rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))
    referred_id = Column(Integer, ForeignKey("users.id"))
    reward_amount = Column(Float, default=0.000005)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_claimed = Column(Boolean, default=True)
