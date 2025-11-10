"""Gemini API integration service."""
import os
from typing import Dict, List, Optional
from google import genai
from app.config import get_settings

settings = get_settings()


class GeminiService:
    """Service for interacting with Google Gemini API."""
    
    def __init__(self):
        """Initialize Gemini client."""
        api_key = settings.gemini_key
        if not api_key:
            raise ValueError("GEMINI_KEY not found in environment variables")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash-exp"
    
    def generate_draft(
        self,
        raw_content: str,
        style_profile: Dict,
        audience: str,
        memory_blocks: List[str],
        preferences: Optional[str] = None
    ) -> str:
        """
        Generate a draft for a specific audience.
        
        Args:
            raw_content: Raw weekly update content
            style_profile: User's writing style profile
            audience: Target audience (investors/employees/partners)
            memory_blocks: Recent summary memory blocks
            preferences: Additional user preferences
            
        Returns:
            Generated draft text
        """
        # Build the prompt
        system_prompt = """You are an assistant that writes weekly business updates in a consistent style.
You must follow the user's writing style, tone profile, audience rules, and historical memory."""
        
        # Format memory blocks
        memory_text = "\n".join(memory_blocks) if memory_blocks else "No previous context available."
        
        # Get audience-specific modifiers
        audience_modifier = style_profile.get("audience_modifiers", {}).get(
            audience, 
            f"appropriate for {audience}"
        )
        
        user_prompt = f"""Raw update:
{raw_content}

Style Profile:
- Tone: {style_profile.get('tone', 'professional')}
- Sentence Length: {style_profile.get('sentence_length', 'medium')}
- Audience Modifier: {audience_modifier}
- Preferred Phrases: {', '.join(style_profile.get('preferred_phrases', []))}
- Avoid Phrases: {', '.join(style_profile.get('avoid_phrases', []))}

Audience:
{audience}

Recent Summary Memory:
{memory_text}

User Preferences:
{preferences or 'None specified'}

TASK:
Generate a clear, concise weekly update tailored for the {audience} audience.
The update should be professional, informative, and match the user's writing style.
Keep it between 200-400 words."""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=f"{system_prompt}\n\n{user_prompt}"
            )
            return response.text
        except Exception as e:
            raise Exception(f"Failed to generate draft: {str(e)}")
    
    def generate_summary(self, content: str) -> str:
        """
        Generate a 2-3 sentence summary of content.
        
        Args:
            content: Content to summarize
            
        Returns:
            Summary text
        """
        prompt = f"""Generate a concise 2-3 sentence summary of the following weekly business update:

{content}

Summary:"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            raise Exception(f"Failed to generate summary: {str(e)}")
    
    def apply_edits(
        self,
        original_draft: str,
        edit_instructions: str,
        style_profile: Dict,
        audience: str
    ) -> str:
        """
        Apply natural language edits to a draft.
        
        Args:
            original_draft: The current draft
            edit_instructions: Natural language edit instructions
            style_profile: User's writing style profile
            audience: Target audience
            
        Returns:
            Updated draft
        """
        audience_modifier = style_profile.get("audience_modifiers", {}).get(
            audience,
            f"appropriate for {audience}"
        )
        
        prompt = f"""You are editing a weekly business update for {audience}.

Current Draft:
{original_draft}

Style Guidelines:
- Tone: {style_profile.get('tone', 'professional')}
- Audience Modifier: {audience_modifier}

Edit Instructions:
{edit_instructions}

Generate the updated draft following the edit instructions while maintaining the style guidelines.
Provide only the updated draft text, no additional commentary."""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            raise Exception(f"Failed to apply edits: {str(e)}")
