"""Update collection routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.database.database import get_db
from app.database.models import WeeklyUpdateRawInput, User

router = APIRouter(prefix="/update", tags=["updates"])


class UpdateSubmit(BaseModel):
    """Request model for submitting update."""
    user_id: int
    content: str


class UpdateResponse(BaseModel):
    """Response model for update."""
    id: int
    user_id: int
    content: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


@router.post("/submit", response_model=UpdateResponse)
def submit_update(update: UpdateSubmit, db: Session = Depends(get_db)):
    """Submit a new weekly update."""
    # Verify user exists
    user = db.query(User).filter(User.id == update.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create update
    new_update = WeeklyUpdateRawInput(
        user_id=update.user_id,
        content=update.content
    )
    db.add(new_update)
    db.commit()
    db.refresh(new_update)
    
    return new_update


@router.get("/list", response_model=List[UpdateResponse])
def list_updates(user_id: int, db: Session = Depends(get_db)):
    """List all updates for a user."""
    updates = db.query(WeeklyUpdateRawInput).filter(
        WeeklyUpdateRawInput.user_id == user_id
    ).order_by(WeeklyUpdateRawInput.timestamp.desc()).all()
    
    return updates


@router.get("/{update_id}", response_model=UpdateResponse)
def get_update(update_id: int, db: Session = Depends(get_db)):
    """Get a specific update."""
    update = db.query(WeeklyUpdateRawInput).filter(
        WeeklyUpdateRawInput.id == update_id
    ).first()
    
    if not update:
        raise HTTPException(status_code=404, detail="Update not found")
    
    return update
