"""Style analyzer service for analyzing writing samples."""
from typing import List, Dict
import re


class StyleAnalyzer:
    """Analyzes writing samples to extract style profile."""
    
    def analyze_style(self, samples: List[str]) -> Dict:
        """
        Analyze writing samples and extract style profile.
        
        Args:
            samples: List of writing sample texts
            
        Returns:
            Style profile dictionary
        """
        if not samples:
            return self._default_style_profile()
        
        # Combine all samples
        combined_text = " ".join(samples)
        
        # Analyze various style attributes
        tone = self._analyze_tone(combined_text)
        sentence_length = self._analyze_sentence_length(combined_text)
        preferred_phrases = self._extract_common_phrases(combined_text)
        
        return {
            "tone": tone,
            "sentence_length": sentence_length,
            "preferred_phrases": preferred_phrases[:10],  # Top 10
            "avoid_phrases": [],  # Can be manually specified by user
            "audience_modifiers": {
                "investors": "upbeat and confident",
                "employees": "supportive and motivating",
                "partners": "honest and collaborative"
            }
        }
    
    def _analyze_tone(self, text: str) -> str:
        """
        Analyze the tone of the text using simple heuristics.
        
        Args:
            text: Text to analyze
            
        Returns:
            Tone description
        """
        text_lower = text.lower()
        
        # Keywords for different tones
        formal_keywords = ['therefore', 'furthermore', 'consequently', 'moreover', 'nevertheless']
        casual_keywords = ['hey', 'yeah', 'cool', 'awesome', 'basically']
        enthusiastic_keywords = ['exciting', 'thrilled', 'amazing', 'fantastic', 'excellent']
        
        formal_count = sum(1 for word in formal_keywords if word in text_lower)
        casual_count = sum(1 for word in casual_keywords if word in text_lower)
        enthusiastic_count = sum(1 for word in enthusiastic_keywords if word in text_lower)
        
        # Determine tone
        if formal_count > casual_count and enthusiastic_count > 2:
            return "formal but friendly"
        elif formal_count > casual_count:
            return "professional and formal"
        elif casual_count > formal_count:
            return "casual and conversational"
        elif enthusiastic_count > 3:
            return "enthusiastic and positive"
        else:
            return "balanced and professional"
    
    def _analyze_sentence_length(self, text: str) -> str:
        """
        Analyze average sentence length.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentence length category (short/medium/long)
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return "medium"
        
        # Calculate average word count per sentence
        avg_words = sum(len(s.split()) for s in sentences) / len(sentences)
        
        if avg_words < 12:
            return "short"
        elif avg_words < 20:
            return "medium"
        else:
            return "long"
    
    def _extract_common_phrases(self, text: str) -> List[str]:
        """
        Extract common 2-3 word phrases.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of common phrases
        """
        # Simple extraction of 2-word phrases
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Count 2-word phrases
        phrase_counts = {}
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1
        
        # Get most common phrases (appearing at least twice)
        common_phrases = [
            phrase for phrase, count in sorted(
                phrase_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            ) if count >= 2
        ]
        
        return common_phrases[:10]
    
    def _default_style_profile(self) -> Dict:
        """
        Return default style profile when no samples available.
        
        Returns:
            Default style profile
        """
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
