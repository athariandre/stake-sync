"""Draft generation routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict
from datetime import datetime

from app.database.database import get_db
from app.database.models import Draft
from app.services.draft_generator import DraftGenerator

router = APIRouter(prefix="/drafts", tags=["drafts"])


class DraftResponse(BaseModel):
    """Response model for draft."""
    id: int
    update_id: int
    user_id: int
    audience: str
    content: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/generate/{update_id}")
def generate_drafts(update_id: int, user_id: int, db: Session = Depends(get_db)):
    """Generate drafts for all audiences."""
    try:
        generator = DraftGenerator(db)
        drafts = generator.generate_all_drafts(update_id, user_id)
        
        return {
            "investors": DraftResponse.model_validate(drafts["investors"]),
            "employees": DraftResponse.model_validate(drafts["employees"]),
            "partners": DraftResponse.model_validate(drafts["partners"])
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate drafts: {str(e)}")


@router.get("/{draft_id}", response_model=DraftResponse)
def get_draft(draft_id: int, db: Session = Depends(get_db)):
    """Get a specific draft."""
    draft = db.query(Draft).filter(Draft.id == draft_id).first()
    
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    
    return draft
