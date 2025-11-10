"""Audience management routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List

from app.database.database import get_db
from app.database.models import AudienceGroup, AudienceType, User

router = APIRouter(prefix="/audience", tags=["audience"])


class AudienceGroupCreate(BaseModel):
    """Request model for creating/updating audience group."""
    user_id: int
    group_type: str  # investors, employees, partners
    emails: List[EmailStr]


class AudienceGroupResponse(BaseModel):
    """Response model for audience group."""
    id: int
    user_id: int
    group_type: str
    emails: List[str]
    
    class Config:
        from_attributes = True


@router.post("/create", response_model=AudienceGroupResponse)
def create_or_update_audience_group(
    group: AudienceGroupCreate,
    db: Session = Depends(get_db)
):
    """Create or update an audience group."""
    # Verify user exists
    user = db.query(User).filter(User.id == group.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate group type
    try:
        audience_type = AudienceType(group.group_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid group type. Must be one of: {', '.join([e.value for e in AudienceType])}"
        )
    
    # Check if group already exists
    existing_group = db.query(AudienceGroup).filter(
        AudienceGroup.user_id == group.user_id,
        AudienceGroup.group_type == audience_type
    ).first()
    
    if existing_group:
        # Update existing group
        existing_group.emails = group.emails
        db.commit()
        db.refresh(existing_group)
        return existing_group
    else:
        # Create new group
        new_group = AudienceGroup(
            user_id=group.user_id,
            group_type=audience_type,
            emails=group.emails
        )
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
        return new_group


@router.get("/list", response_model=List[AudienceGroupResponse])
def list_audience_groups(user_id: int, db: Session = Depends(get_db)):
    """List all audience groups for a user."""
    groups = db.query(AudienceGroup).filter(
        AudienceGroup.user_id == user_id
    ).all()
    
    return groups


@router.get("/{group_id}", response_model=AudienceGroupResponse)
def get_audience_group(group_id: int, db: Session = Depends(get_db)):
    """Get a specific audience group."""
    group = db.query(AudienceGroup).filter(AudienceGroup.id == group_id).first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Audience group not found")
    
    return group
