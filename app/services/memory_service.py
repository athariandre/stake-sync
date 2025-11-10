"""Memory service for agent-style context management."""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database.models import SummaryMemory, WeeklyUpdateRawInput


class MemoryService:
    """Service for managing agent context/memory."""
    
    def __init__(self, db: Session):
        """Initialize memory service."""
        self.db = db
    
    def get_recent_memories(
        self,
        user_id: int,
        weeks: int = 4
    ) -> List[str]:
        """
        Get recent summary memories for context.
        
        Args:
            user_id: User ID
            weeks: Number of weeks to retrieve (default: 4)
            
        Returns:
            List of summary memory texts
        """
        cutoff_date = datetime.utcnow() - timedelta(weeks=weeks)
        
        memories = self.db.query(SummaryMemory).filter(
            SummaryMemory.user_id == user_id,
            SummaryMemory.week_start >= cutoff_date
        ).order_by(SummaryMemory.week_start.desc()).limit(weeks).all()
        
        return [memory.summary_text for memory in memories]
    
    def create_summary_memory(
        self,
        user_id: int,
        summary_text: str,
        week_start: datetime,
        week_end: datetime
    ) -> SummaryMemory:
        """
        Create a new summary memory.
        
        Args:
            user_id: User ID
            summary_text: Summary text
            week_start: Start of the week
            week_end: End of the week
            
        Returns:
            Created SummaryMemory object
        """
        memory = SummaryMemory(
            user_id=user_id,
            summary_text=summary_text,
            week_start=week_start,
            week_end=week_end
        )
        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)
        return memory
    
    def get_interaction_history(
        self,
        user_id: int,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get recent interaction history (recent updates).
        
        Args:
            user_id: User ID
            limit: Number of recent interactions
            
        Returns:
            List of interaction dictionaries
        """
        updates = self.db.query(WeeklyUpdateRawInput).filter(
            WeeklyUpdateRawInput.user_id == user_id
        ).order_by(WeeklyUpdateRawInput.timestamp.desc()).limit(limit).all()
        
        return [
            {
                "id": update.id,
                "content": update.content[:200] + "..." if len(update.content) > 200 else update.content,
                "timestamp": update.timestamp.isoformat()
            }
            for update in updates
        ]
    
    def build_context(
        self,
        user_id: int,
        style_profile: Optional[Dict] = None
    ) -> Dict:
        """
        Build complete agent context.
        
        Args:
            user_id: User ID
            style_profile: User's style profile
            
        Returns:
            Context dictionary with all layers
        """
        return {
            "long_term_memory": self.get_recent_memories(user_id, weeks=6),
            "short_term_memory": {
                "recent_interactions": self.get_interaction_history(user_id, limit=5)
            },
            "style_profile": style_profile or {}
        }
