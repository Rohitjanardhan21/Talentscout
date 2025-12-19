"""
Advanced AIML Engine for Intelligent Conversation Handling
"""
import aiml
import os
import re
import json
from typing import Dict, List, Optional, Any
import streamlit as st
from datetime import datetime

class AIMLEngine:
    """Advanced AIML engine with context awareness and learning capabilities"""
    
    def __init__(self):
        self.kernel = aiml.Kernel()
        self.conversation_context = {}
        self.learning_data = {}
        self.pattern_cache = {}
        self.initialize_aiml()
    
    def initialize_aiml(self):
        """Initialize AIML kernel with patterns"""
        try:
            # Load AIML patterns
            aiml_dir = os.path.join(os.path.dirname(__file__))
            pattern_files = [
                os.path.join(aiml_dir, "hiring_patterns.aiml"),
                os.path.join(aiml_dir, "advanced_patterns.aiml")
            ]
            
            for pattern_file in pattern_files:
                if os.path.exists(pattern_file):
                    self.kernel.learn(pattern_file)
                    print(f"✅ Loaded AIML patterns from {pattern_file}")
                else:
                    print(f"⚠️ AIML pattern file not found: {pattern_file}")
            
            # Set initial bot predicates
            self.kernel.setBotPredicate("name", "TalentScout Assistant")
            self.kernel.setBotPredicate("age", "1")
            self.kernel.setBotPredicate("location", "Cloud")
            self.kernel.setBotPredicate("master", "TalentScout Team")
            
        except Exception as e:
            print(f"❌ Error initializing AIML: {e}")
    
    def process_input(self, user_input: str, session_id: str = "default") -> Dict[str, Any]:
        """Process user input through AIML with context awareness"""
        try:
            # Normalize input
            normalized_input = self.normalize_input(user_input)
            
            # Get AIML response
            aiml_response = self.kernel.respond(normalized_input)
            
            # Extract context from response
            context = self.extract_context(aiml_response, user_input)
            
            # Store conversation context
            self.update_context(session_id, user_input, aiml_response, context)
            
            # Enhance response with dynamic content
            enhanced_response = self.enhance_response(aiml_response, context, session_id)
            
            return {
                "response": enhanced_response,
                "context": context,
                "confidence": self.calculate_confidence(normalized_input, aiml_response),
                "intent": self.detect_intent(user_input),
                "entities": self.extract_entities(user_input)
            }
            
        except Exception as e:
            print(f"❌ Error processing AIML input: {e}")
            return {
                "response": "I'm having a bit of trouble understanding that. Could you try rephrasing?",
                "context": {},
                "confidence": 0.1,
                "intent": "unknown",
                "entities": {}
            }
    
    def normalize_input(self, user_input: str) -> str:
        """Normalize user input for better pattern matching"""
        # Convert to uppercase for AIML processing
        normalized = user_input.upper()
        
        # Handle common contractions
        contractions = {
            "I'M": "I AM",
            "I'VE": "I HAVE",
            "I'D": "I WOULD",
            "I'LL": "I WILL",
            "DON'T": "DO NOT",
            "CAN'T": "CAN NOT",
            "WON'T": "WILL NOT",
            "SHOULDN'T": "SHOULD NOT",
            "WOULDN'T": "WOULD NOT",
            "COULDN'T": "COULD NOT"
        }
        
        for contraction, expansion in contractions.items():
            normalized = normalized.replace(contraction, expansion)
        
        # Clean up extra spaces and punctuation
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
    
    def extract_context(self, aiml_response: str, user_input: str) -> Dict[str, Any]:
        """Extract context information from the conversation"""
        context = {}
        
        # Extract technical skills mentioned - dynamically build patterns from config
        from config import Config
        tech_patterns = {}
        
        # Build regex patterns for each category from config
        for category, technologies in Config.COMMON_TECHNOLOGIES.items():
            # Escape special regex characters and create pattern
            escaped_techs = [re.escape(tech) for tech in technologies]
            pattern = r'\b(' + '|'.join(escaped_techs) + r')\b'
            tech_patterns[category] = pattern
        
        user_lower = user_input.lower()
        for category, pattern in tech_patterns.items():
            matches = re.findall(pattern, user_lower, re.IGNORECASE)
            if matches:
                context[category] = list(set(matches))
        
        # Extract experience level
        exp_match = re.search(r'(\d+)\s*years?\s*(of\s*)?(experience|exp)', user_lower)
        if exp_match:
            context['experience_years'] = int(exp_match.group(1))
        
        # Extract name
        name_match = re.search(r'(my name is|i am|call me)\s+([a-zA-Z]+)', user_lower)
        if name_match:
            context['name'] = name_match.group(2).title()
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', user_input)
        if email_match:
            context['email'] = email_match.group(0)
        
        # Extract phone
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', user_input)
        if phone_match:
            context['phone'] = phone_match.group(0)
        
        return context
    
    def detect_intent(self, user_input: str) -> str:
        """Detect user intent from input"""
        user_lower = user_input.lower()
        
        intent_patterns = {
            'greeting': r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b',
            'introduction': r'\b(my name is|i am|call me|i\'m)\b',
            'experience': r'\b(years|experience|worked|developer|engineer)\b',
            'tech_stack': r'\b(use|work with|know|familiar|experience with|tech stack)\b',
            'project': r'\b(built|developed|created|project|application|system)\b',
            'question_company': r'\b(talentscout|company|process|what happens|salary|benefits)\b',
            'goodbye': r'\b(bye|goodbye|thanks|thank you|see you|later)\b',
            'clarification': r'\b(what|how|why|when|where|explain|tell me)\b'
        }
        
        for intent, pattern in intent_patterns.items():
            if re.search(pattern, user_lower):
                return intent
        
        return 'general'
    
    def extract_entities(self, user_input: str) -> Dict[str, List[str]]:
        """Extract named entities from user input"""
        entities = {}
        
        # Technology entities - use config for comprehensive coverage
        from config import Config
        tech_entities = Config.COMMON_TECHNOLOGIES
        
        user_lower = user_input.lower()
        for category, items in tech_entities.items():
            found_items = [item for item in items if item in user_lower]
            if found_items:
                entities[category] = found_items
        
        return entities
    
    def calculate_confidence(self, normalized_input: str, aiml_response: str) -> float:
        """Calculate confidence score for the response"""
        # Check if AIML found a specific pattern match
        if aiml_response and not aiml_response.startswith("I'm not quite sure"):
            # Higher confidence for specific responses
            if len(aiml_response) > 50:
                return 0.9
            elif len(aiml_response) > 20:
                return 0.7
            else:
                return 0.5
        else:
            # Lower confidence for fallback responses
            return 0.2
    
    def update_context(self, session_id: str, user_input: str, aiml_response: str, context: Dict[str, Any]):
        """Update conversation context for the session"""
        if session_id not in self.conversation_context:
            self.conversation_context[session_id] = {
                'messages': [],
                'extracted_data': {},
                'conversation_state': 'greeting',
                'start_time': datetime.now().isoformat()
            }
        
        # Add message to history
        self.conversation_context[session_id]['messages'].append({
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'bot_response': aiml_response,
            'context': context
        })
        
        # Update extracted data
        self.conversation_context[session_id]['extracted_data'].update(context)
        
        # Update conversation state based on context
        if context.get('name'):
            self.conversation_context[session_id]['conversation_state'] = 'collecting_info'
        elif context.get('experience_years'):
            self.conversation_context[session_id]['conversation_state'] = 'tech_stack_collection'
        else:
            from config import Config
            if any(key in context for key in Config.COMMON_TECHNOLOGIES.keys()):
                self.conversation_context[session_id]['conversation_state'] = 'technical_questions'
    
    def enhance_response(self, aiml_response: str, context: Dict[str, Any], session_id: str) -> str:
        """Enhance AIML response with dynamic content"""
        enhanced = aiml_response
        
        # Get session context
        session_context = self.conversation_context.get(session_id, {})
        extracted_data = session_context.get('extracted_data', {})
        
        # Replace placeholders with actual data
        if '{name}' in enhanced and extracted_data.get('name'):
            enhanced = enhanced.replace('{name}', extracted_data['name'])
        
        if '{experience}' in enhanced and extracted_data.get('experience_years'):
            enhanced = enhanced.replace('{experience}', str(extracted_data['experience_years']))
        
        # Add personalized tech stack information
        from config import Config
        if any(context.get(category) for category in Config.COMMON_TECHNOLOGIES.keys()):
            tech_summary = []
            for category in Config.COMMON_TECHNOLOGIES.keys():
                if context.get(category):
                    tech_summary.append(f"**{category.replace('_', ' ').title()}**: {', '.join(context[category])}")
            
            if tech_summary and 'tech stack' in enhanced.lower():
                tech_display = '\n'.join(tech_summary)
                enhanced += f"\n\nHere's what I picked up:\n{tech_display}"
        
        return enhanced
    
    def get_session_context(self, session_id: str) -> Dict[str, Any]:
        """Get conversation context for a session"""
        return self.conversation_context.get(session_id, {})
    
    def reset_session(self, session_id: str):
        """Reset conversation context for a session"""
        if session_id in self.conversation_context:
            del self.conversation_context[session_id]
    
    def learn_from_feedback(self, session_id: str, feedback: Dict[str, Any]):
        """Learn from user feedback to improve responses"""
        if session_id not in self.learning_data:
            self.learning_data[session_id] = []
        
        self.learning_data[session_id].append({
            'timestamp': datetime.now().isoformat(),
            'feedback': feedback
        })
    
    def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """Generate a summary of the conversation"""
        session_context = self.conversation_context.get(session_id, {})
        
        if not session_context:
            return {}
        
        extracted_data = session_context.get('extracted_data', {})
        messages = session_context.get('messages', [])
        
        # Check for tech stack mentions using all categories from config
        from config import Config
        tech_stack_mentioned = any(key in extracted_data for key in Config.COMMON_TECHNOLOGIES.keys())
        
        return {
            'session_id': session_id,
            'start_time': session_context.get('start_time'),
            'message_count': len(messages),
            'conversation_state': session_context.get('conversation_state'),
            'candidate_data': extracted_data,
            'tech_stack_mentioned': tech_stack_mentioned,
            'completion_status': session_context.get('conversation_state') in ['completed', 'ended']
        }