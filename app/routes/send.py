"""Email sending routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.database.database import get_db
from app.database.models import Draft, DraftStatus, AudienceGroup, EmailLog, SummaryMemory
from app.services.sendgrid_service import SendGridService
from app.services.gemini_service import GeminiService

router = APIRouter(prefix="/send", tags=["send"])


class SendResponse(BaseModel):
    """Response model for send operation."""
    draft_id: int
    recipients_count: int
    status: str
    sent_at: datetime


@router.post("/{draft_id}", response_model=SendResponse)
def send_draft(draft_id: int, user_id: int, db: Session = Depends(get_db)):
    """Send an approved draft via email."""
    # Get the draft
    draft = db.query(Draft).filter(
        Draft.id == draft_id,
        Draft.user_id == user_id
    ).first()
    
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    
    # Check if draft is approved
    if draft.status != DraftStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Draft must be approved before sending")
    
    # Get audience group
    audience_group = db.query(AudienceGroup).filter(
        AudienceGroup.user_id == user_id,
        AudienceGroup.group_type == draft.audience
    ).first()
    
    if not audience_group or not audience_group.emails:
        raise HTTPException(status_code=404, detail=f"No recipients found for {draft.audience.value}")
    
    recipients = audience_group.emails
    
    # Generate subject line
    subject = f"Weekly Update – {datetime.utcnow().strftime('%B %d, %Y')}"
    
    # Send email
    try:
        sendgrid = SendGridService()
        response = sendgrid.send_update(
            recipients=recipients,
            subject=subject,
            content=draft.content,
            audience_type=draft.audience.value
        )
        
        # Log the email
        email_log = EmailLog(
            draft_id=draft_id,
            recipients=recipients,
            sendgrid_status=str(response.get("status_code", "unknown")),
            sent_at=datetime.utcnow()
        )
        db.add(email_log)
        
        # Generate and save summary memory if this is the first send for this update
        existing_logs = db.query(EmailLog).join(Draft).filter(
            Draft.update_id == draft.update_id
        ).count()
        
        if existing_logs == 0:  # First audience being sent
            # Generate summary
            gemini = GeminiService()
            summary = gemini.generate_summary(draft.update.content)
            
            # Calculate week boundaries
            now = datetime.utcnow()
            week_start = now - timedelta(days=now.weekday())
            week_end = week_start + timedelta(days=6)
            
            # Save summary memory
            summary_memory = SummaryMemory(
                user_id=user_id,
                summary_text=summary,
                week_start=week_start,
                week_end=week_end
            )
            db.add(summary_memory)
        
        db.commit()
        
        return {
            "draft_id": draft_id,
            "recipients_count": len(recipients),
            "status": "sent",
            "sent_at": email_log.sent_at
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
