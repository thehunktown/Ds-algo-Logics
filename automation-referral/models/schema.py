# rag_referral_agent/models/schema.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime
import enum

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    referral_credits = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    referrals = relationship("Referral", back_populates="user")

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    job_url = Column(String, nullable=False)
    company_name = Column(String)
    role = Column(String)
    job_description = Column(Text)
    skills = Column(Text)
    status = Column(String, default="new")

    job_open_date = Column(DateTime)
    active_till = Column(DateTime)
    posted_by = Column(String)
    received_call = Column(Integer, default=0)  # 0 = No, 1 = Yes
    critical = Column(Integer, default=0)       # 0 to 5
    reminder_date = Column(DateTime)
    reminder_sent = Column(Integer, default=0)  # 0 = No, 1 = Yes

    created_at = Column(DateTime, default=datetime.utcnow)

    # Referrals relationship
    referrals = relationship("Referral", back_populates="job")


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    domain = Column(String)
    email_pattern = Column(String)
    deliverable_format = Column(String)
    last_verified_at = Column(DateTime)
    is_verified = Column(Integer, default=0)  # 0 = Not Verified, 1 = Verified

class EmailStatusEnum(str, enum.Enum):
    sent = "sent"
    failed = "failed"
    verified = "verified"
    blocked = "blocked"

class ResponseStatusEnum(str, enum.Enum):
    waiting = "waiting"
    opened = "opened"
    clicked = "clicked"
    replied = "replied"
    ignored = "ignored"
    unsubscribed = "unsubscribed"
    bounced = "bounced"
    spam_reported = "spam_reported"
    blacklisted = "blacklisted"
    accepted = "accepted"
    rejected = "rejected"

class Referral(Base):
    __tablename__ = "referrals"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    candidate_name = Column(String)
    candidate_email = Column(String)
    email_status = Column(Enum(EmailStatusEnum), default=EmailStatusEnum.sent)
    response_status = Column(Enum(ResponseStatusEnum), default=ResponseStatusEnum.waiting)
    critical = Column(Integer, default=0)  # 0 = not critical, 5 = most critical
    timestamp = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="referrals")
    user = relationship("User", back_populates="referrals")
