from sqlalchemy import Column, Integer, String, Enum, Text, DECIMAL, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base
import enum

class RoleEnum(enum.Enum):
    employee = "employee"
    admin = "admin"

class VerdictEnum(enum.Enum):
    approved = "approved"
    rejected = "rejected"
    manual_review = "manual_review"
    pending = "pending"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.employee, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    receipts = relationship("Receipt", back_populates="user")

class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    rule_type = Column(String(100))
    rule_value = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class Receipt(Base):
    __tablename__ = "receipts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    upload_path = Column(String(500), nullable=False)
    description = Column(Text)
    extracted_text = Column(Text(length=4294967295)) # LONGTEXT roughly maps to that size
    merchant = Column(String(255))
    date = Column(String(50))
    business_purpose = Column(Text)
    total_amount = Column(DECIMAL(10, 2))
    verdict = Column(Enum(VerdictEnum), default=VerdictEnum.pending)
    verdict_reasoning = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="receipts")
