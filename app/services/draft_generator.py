"""Draft generation service."""
from typing import Dict, List
from sqlalchemy.orm import Session
from app.database.models import Draft, WeeklyUpdateRawInput, User, AudienceType, DraftStatus
from app.services.gemini_service import GeminiService
from app.services.memory_service import MemoryService


class DraftGenerator:
    """Service for generating drafts for multiple audiences."""
    
    def __init__(self, db: Session):
        """Initialize draft generator."""
        self.db = db
        self.gemini = GeminiService()
        self.memory_service = MemoryService(db)
    
    def generate_all_drafts(
        self,
        update_id: int,
        user_id: int
    ) -> Dict[str, Draft]:
        """
        Generate drafts for all three audiences.
        
        Args:
            update_id: Weekly update ID
            user_id: User ID
            
        Returns:
            Dictionary with audience type as key and Draft object as value
        """
        # Get the update
        update = self.db.query(WeeklyUpdateRawInput).filter(
            WeeklyUpdateRawInput.id == update_id,
            WeeklyUpdateRawInput.user_id == user_id
        ).first()
        
        if not update:
            raise ValueError("Update not found")
        
        # Get user and style profile
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        style_profile = user.style_profile or self._default_style_profile()
        
        # Get memory context
        memory_blocks = self.memory_service.get_recent_memories(user_id, weeks=4)
        
        # Generate drafts for each audience
        drafts = {}
        for audience in AudienceType:
            draft_content = self.gemini.generate_draft(
                raw_content=update.content,
                style_profile=style_profile,
                audience=audience.value,
                memory_blocks=memory_blocks,
                preferences=None
            )
            
            # Create draft in database
            draft = Draft(
                update_id=update_id,
                user_id=user_id,
                audience=audience,
                content=draft_content,
                status=DraftStatus.DRAFT
            )
            self.db.add(draft)
            drafts[audience.value] = draft
        
        self.db.commit()
        
        # Refresh all drafts
        for draft in drafts.values():
            self.db.refresh(draft)
        
        return drafts
    
    def regenerate_draft(
        self,
        draft_id: int,
        user_id: int
    ) -> Draft:
        """
        Regenerate a specific draft.
        
        Args:
            draft_id: Draft ID
            user_id: User ID
            
        Returns:
            Updated Draft object
        """
        # Get the draft
        draft = self.db.query(Draft).filter(
            Draft.id == draft_id,
            Draft.user_id == user_id
        ).first()
        
        if not draft:
            raise ValueError("Draft not found")
        
        # Get the update
        update = draft.update
        
        # Get user and style profile
        user = self.db.query(User).filter(User.id == user_id).first()
        style_profile = user.style_profile or self._default_style_profile()
        
        # Get memory context
        memory_blocks = self.memory_service.get_recent_memories(user_id, weeks=4)
        
        # Generate new draft content
        new_content = self.gemini.generate_draft(
            raw_content=update.content,
            style_profile=style_profile,
            audience=draft.audience.value,
            memory_blocks=memory_blocks,
            preferences=None
        )
        
        # Update draft
        draft.content = new_content
        draft.status = DraftStatus.DRAFT
        self.db.commit()
        self.db.refresh(draft)
        
        return draft
    
    def apply_edits(
        self,
        draft_id: int,
        user_id: int,
        edit_instructions: str
    ) -> Draft:
        """
        Apply natural language edits to a draft.
        
        Args:
            draft_id: Draft ID
            user_id: User ID
            edit_instructions: Natural language edit instructions
            
        Returns:
            Updated Draft object
        """
        # Get the draft
        draft = self.db.query(Draft).filter(
            Draft.id == draft_id,
            Draft.user_id == user_id
        ).first()
        
        if not draft:
            raise ValueError("Draft not found")
        
        # Get user and style profile
        user = self.db.query(User).filter(User.id == user_id).first()
        style_profile = user.style_profile or self._default_style_profile()
        
        # Apply edits using Gemini
        edited_content = self.gemini.apply_edits(
            original_draft=draft.content,
            edit_instructions=edit_instructions,
            style_profile=style_profile,
            audience=draft.audience.value
        )
        
        # Update draft
        draft.content = edited_content
        draft.status = DraftStatus.EDITED
        self.db.commit()
        self.db.refresh(draft)
        
        return draft
    
    def _default_style_profile(self) -> Dict:
        """Return default style profile."""
        return {
            "tone": "professional and balanced",
            "sentence_length": "medium",
            "preferred_phrases": [],
            "avoid_phrases": [],
            "audience_modifiers": {
                "investors": "upbeat and confident",
                "employees": "supportive and motivating",
                "partners": "honest and collaborative"
            }
        }
