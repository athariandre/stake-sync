"""Database models for the application."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


Base = declarative_base()


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    style_profile = Column(JSON, nullable=True)  # Store style analysis results
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    writing_samples = relationship("WritingSample", back_populates="user", cascade="all, delete-orphan")
    weekly_updates = relationship("WeeklyUpdateRawInput", back_populates="user", cascade="all, delete-orphan")
    drafts = relationship("Draft", back_populates="user", cascade="all, delete-orphan")
    summary_memories = relationship("SummaryMemory", back_populates="user", cascade="all, delete-orphan")
    audience_groups = relationship("AudienceGroup", back_populates="user", cascade="all, delete-orphan")


class WritingSample(Base):
    """Writing sample uploaded by user for style analysis."""
    __tablename__ = "writing_samples"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="writing_samples")


class WeeklyUpdateRawInput(Base):
    """Raw weekly update submitted by user."""
    __tablename__ = "weekly_updates_raw"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="weekly_updates")
    drafts = relationship("Draft", back_populates="update", cascade="all, delete-orphan")


class AudienceType(str, enum.Enum):
    """Enum for audience types."""
    INVESTORS = "investors"
    EMPLOYEES = "employees"
    PARTNERS = "partners"


class DraftStatus(str, enum.Enum):
    """Enum for draft status."""
    DRAFT = "draft"
    EDITED = "edited"
    APPROVED = "approved"
    REJECTED = "rejected"


class Draft(Base):
    """AI-generated draft for a specific audience."""
    __tablename__ = "drafts"
    
    id = Column(Integer, primary_key=True, index=True)
    update_id = Column(Integer, ForeignKey("weekly_updates_raw.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    audience = Column(Enum(AudienceType), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Enum(DraftStatus), default=DraftStatus.DRAFT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="drafts")
    update = relationship("WeeklyUpdateRawInput", back_populates="drafts")
    email_logs = relationship("EmailLog", back_populates="draft", cascade="all, delete-orphan")


class SummaryMemory(Base):
    """Summarized historical updates for context."""
    __tablename__ = "summary_memories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    summary_text = Column(Text, nullable=False)
    week_start = Column(DateTime, nullable=False)
    week_end = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="summary_memories")


class AudienceGroup(Base):
    """Email list for each audience type."""
    __tablename__ = "audience_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_type = Column(Enum(AudienceType), nullable=False)
    emails = Column(JSON, nullable=False)  # List of email addresses
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="audience_groups")


class EmailLog(Base):
    """Log of sent emails via SendGrid."""
    __tablename__ = "email_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    draft_id = Column(Integer, ForeignKey("drafts.id"), nullable=False)
    recipients = Column(JSON, nullable=False)  # List of email addresses
    sendgrid_status = Column(String(50), nullable=True)
    sent_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    draft = relationship("Draft", back_populates="email_logs")
