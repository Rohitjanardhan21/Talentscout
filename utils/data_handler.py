"""
Data handling utilities for candidate information
"""
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any

class CandidateDataHandler:
    """Handles candidate data validation and processing"""
    
    def __init__(self):
        self.candidate_data = {}
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format"""
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        # Check if it has 10-15 digits (international format)
        return 10 <= len(digits_only) <= 15
    
    def validate_experience(self, experience: str) -> Optional[int]:
        """Validate and extract years of experience"""
        try:
            years = int(experience)
            return years if 0 <= years <= 50 else None
        except ValueError:
            return None
    
    def parse_tech_stack(self, tech_stack_text: str) -> Dict[str, List[str]]:
        """Parse and categorize tech stack from text - optimized for speed"""
        from config import Config
        
        tech_stack_text = tech_stack_text.lower()
        # Initialize all categories from config
        categorized = {}
        for category in Config.COMMON_TECHNOLOGIES.keys():
            categorized[category] = []
        
        # Faster lookup using sets
        tech_lookup = {}
        for category, technologies in Config.COMMON_TECHNOLOGIES.items():
            for tech in technologies:
                tech_lookup[tech] = category
        
        # Split input and check each word
        words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#.]*\b', tech_stack_text)
        found_techs = set()
        
        for word in words:
            word_lower = word.lower()
            if word_lower in tech_lookup and word_lower not in found_techs:
                category = tech_lookup[word_lower]
                categorized[category].append(word_lower.title())
                found_techs.add(word_lower)
        
        # Return only non-empty categories
        return {k: v for k, v in categorized.items() if v}
    
    def store_candidate_info(self, field: str, value: Any) -> bool:
        """Store candidate information with validation"""
        if field == 'email' and not self.validate_email(value):
            return False
        elif field == 'phone' and not self.validate_phone(value):
            return False
        elif field == 'experience_years':
            validated_exp = self.validate_experience(value)
            if validated_exp is None:
                return False
            value = validated_exp
        elif field == 'tech_stack':
            value = self.parse_tech_stack(value)
        
        self.candidate_data[field] = value
        return True
    
    def get_candidate_data(self) -> Dict[str, Any]:
        """Get current candidate data"""
        return self.candidate_data.copy()
    
    def is_complete(self) -> bool:
        """Check if all required fields are collected"""
        from config import Config
        return all(field in self.candidate_data for field in Config.REQUIRED_FIELDS)
    
    def get_missing_fields(self) -> List[str]:
        """Get list of missing required fields"""
        from config import Config
        return [field for field in Config.REQUIRED_FIELDS 
                if field not in self.candidate_data]
    
    def export_to_json(self) -> str:
        """Export candidate data to JSON string"""
        export_data = self.candidate_data.copy()
        export_data['timestamp'] = datetime.now().isoformat()
        return json.dumps(export_data, indent=2)
    
    def clear_data(self):
        """Clear all candidate data"""
        self.candidate_data = {}