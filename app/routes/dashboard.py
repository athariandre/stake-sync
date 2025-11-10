"""Dashboard routes."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.database import get_db
from app.database.models import Draft, DraftStatus, EmailLog, User
from app.services.gemini_service import GeminiService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/{user_id}", response_class=HTMLResponse)
def get_dashboard(user_id: int, db: Session = Depends(get_db)):
    """Get user's public dashboard showing sent updates."""
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get all sent drafts
    sent_drafts = db.query(Draft).join(EmailLog).filter(
        Draft.user_id == user_id,
        Draft.status == DraftStatus.APPROVED
    ).order_by(Draft.updated_at.desc()).all()
    
    # Group drafts by update
    updates = {}
    for draft in sent_drafts:
        update_id = draft.update_id
        if update_id not in updates:
            updates[update_id] = {
                "update": draft.update,
                "drafts": [],
                "sent_at": draft.updated_at
            }
        updates[update_id]["drafts"].append(draft)
    
    # Generate HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{user.name}'s Weekly Updates - StakeSync</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background: #f5f5f5;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            header {{
                background: white;
                padding: 30px;
                margin-bottom: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            h1 {{
                color: #2c3e50;
                margin-bottom: 10px;
            }}
            
            .subtitle {{
                color: #7f8c8d;
                font-size: 1.1em;
            }}
            
            .update-card {{
                background: white;
                padding: 30px;
                margin-bottom: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .update-meta {{
                color: #7f8c8d;
                font-size: 0.9em;
                margin-bottom: 15px;
            }}
            
            .audiences {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-bottom: 15px;
            }}
            
            .audience-badge {{
                background: #3498db;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9em;
            }}
            
            .audience-badge.investors {{
                background: #27ae60;
            }}
            
            .audience-badge.employees {{
                background: #e74c3c;
            }}
            
            .audience-badge.partners {{
                background: #f39c12;
            }}
            
            .summary {{
                font-size: 1.1em;
                color: #2c3e50;
                line-height: 1.8;
                margin-top: 15px;
            }}
            
            .no-updates {{
                text-align: center;
                padding: 60px 20px;
                color: #7f8c8d;
            }}
            
            footer {{
                text-align: center;
                padding: 30px;
                color: #7f8c8d;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>{user.name}'s Weekly Updates</h1>
                <p class="subtitle">Stay informed with regular business updates</p>
            </header>
            
            <main>
    """
    
    if not updates:
        html += """
                <div class="update-card no-updates">
                    <p>No updates have been published yet.</p>
                </div>
        """
    else:
        for update_id, update_data in updates.items():
            update = update_data["update"]
            drafts = update_data["drafts"]
            sent_at = update_data["sent_at"]
            
            # Generate summary using Gemini
            try:
                gemini = GeminiService()
                summary = gemini.generate_summary(update.content)
            except:
                summary = update.content[:300] + "..." if len(update.content) > 300 else update.content
            
            audiences_html = "".join([
                f'<span class="audience-badge {draft.audience.value}">{draft.audience.value.title()}</span>'
                for draft in drafts
            ])
            
            html += f"""
                <div class="update-card">
                    <div class="update-meta">
                        {sent_at.strftime('%B %d, %Y at %I:%M %p')}
                    </div>
                    <div class="audiences">
                        {audiences_html}
                    </div>
                    <div class="summary">
                        {summary}
                    </div>
                </div>
            """
    
    html += """
            </main>
            
            <footer>
                <p>Powered by StakeSync - Automated Weekly Business Updates</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    return html
