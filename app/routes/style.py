"""Style sample routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Optional

from app.database.database import get_db
from app.database.models import WritingSample, User
from app.services.style_analyzer import StyleAnalyzer

router = APIRouter(prefix="/style", tags=["style"])


class StyleSampleUpload(BaseModel):
    """Request model for uploading style sample."""
    user_id: int
    content: str


class StyleProfileResponse(BaseModel):
    """Response model for style profile."""
    user_id: int
    style_profile: Optional[Dict]


@router.post("/upload")
def upload_style_sample(sample: StyleSampleUpload, db: Session = Depends(get_db)):
    """Upload a writing sample for style analysis."""
    # Verify user exists
    user = db.query(User).filter(User.id == sample.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create writing sample
    new_sample = WritingSample(
        user_id=sample.user_id,
        content=sample.content
    )
    db.add(new_sample)
    db.commit()
    
    # Analyze all samples for this user
    all_samples = db.query(WritingSample).filter(
        WritingSample.user_id == sample.user_id
    ).all()
    
    sample_texts = [s.content for s in all_samples]
    
    # Analyze style
    analyzer = StyleAnalyzer()
    style_profile = analyzer.analyze_style(sample_texts)
    
    # Update user's style profile
    user.style_profile = style_profile
    db.commit()
    
    return {
        "message": "Style sample uploaded successfully",
        "style_profile": style_profile
    }


@router.get("/profile", response_model=StyleProfileResponse)
def get_style_profile(user_id: int, db: Session = Depends(get_db)):
    """Get user's style profile."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.id,
        "style_profile": user.style_profile
    }
