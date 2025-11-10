"""Review workflow routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.database.models import Draft, DraftStatus
from app.services.draft_generator import DraftGenerator
from app.routes.drafts import DraftResponse

router = APIRouter(prefix="/review", tags=["review"])


class ApplyEditsRequest(BaseModel):
    """Request model for applying edits."""
    user_id: int
    edit_instructions: str


class ManualEditRequest(BaseModel):
    """Request model for manual edits."""
    user_id: int
    new_content: str


@router.post("/apply-edits/{draft_id}", response_model=DraftResponse)
def apply_edits(draft_id: int, request: ApplyEditsRequest, db: Session = Depends(get_db)):
    """Apply natural language edits to a draft."""
    try:
        generator = DraftGenerator(db)
        draft = generator.apply_edits(draft_id, request.user_id, request.edit_instructions)
        return draft
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to apply edits: {str(e)}")


@router.post("/manual-edit/{draft_id}", response_model=DraftResponse)
def manual_edit(draft_id: int, request: ManualEditRequest, db: Session = Depends(get_db)):
    """Manually edit a draft."""
    draft = db.query(Draft).filter(
        Draft.id == draft_id,
        Draft.user_id == request.user_id
    ).first()
    
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    
    draft.content = request.new_content
    draft.status = DraftStatus.EDITED
    db.commit()
    db.refresh(draft)
    
    return draft


@router.post("/approve/{draft_id}", response_model=DraftResponse)
def approve_draft(draft_id: int, user_id: int, db: Session = Depends(get_db)):
    """Approve a draft."""
    draft = db.query(Draft).filter(
        Draft.id == draft_id,
        Draft.user_id == user_id
    ).first()
    
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    
    draft.status = DraftStatus.APPROVED
    db.commit()
    db.refresh(draft)
    
    return draft


@router.post("/reject/{draft_id}", response_model=DraftResponse)
def reject_draft(draft_id: int, user_id: int, db: Session = Depends(get_db)):
    """Reject a draft."""
    draft = db.query(Draft).filter(
        Draft.id == draft_id,
        Draft.user_id == user_id
    ).first()
    
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    
    draft.status = DraftStatus.REJECTED
    db.commit()
    db.refresh(draft)
    
    return draft


@router.post("/regenerate/{draft_id}", response_model=DraftResponse)
def regenerate_draft(draft_id: int, user_id: int, db: Session = Depends(get_db)):
    """Regenerate a draft."""
    try:
        generator = DraftGenerator(db)
        draft = generator.regenerate_draft(draft_id, user_id)
        return draft
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to regenerate draft: {str(e)}")
