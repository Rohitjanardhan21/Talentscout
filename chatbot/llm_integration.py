"""
LLM integration for enhanced conversation handling
"""
import openai
from typing import Optional, Dict, Any
from config import Config
import streamlit as st

class LLMIntegration:
    """Handles LLM integration for enhanced responses"""
    
    def __init__(self):
        self.client = None
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize OpenAI client"""
        try:
            if Config.OPENAI_API_KEY:
                openai.api_key = Config.OPENAI_API_KEY
                self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
            else:
                st.warning("⚠️ OpenAI API key not found. Using fallback responses.")
        except Exception as e:
            st.error(f"Error initializing LLM client: {str(e)}")
            self.client = None
    
    def enhance_response(self, base_response: str, context: Dict[str, Any]) -> str:
        """Enhance response using LLM if available - with smart caching"""
        if not self.client:
            return base_response
        
        # Cache key for this response type
        cache_key = f"{context.get('state', 'unknown')}_{len(base_response)}"
        
        # Use cached response if available
        if hasattr(self, '_response_cache') and cache_key in self._response_cache:
            return self._response_cache[cache_key]
        
        try:
            # Only enhance important responses
            important_states = ['tech_stack_collection', 'technical_questions', 'completed']
            if context.get('state') not in important_states:
                return base_response
            
            prompt = self._create_enhancement_prompt(base_response, context)
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                temperature=0.7
            )
            
            enhanced_response = response.choices[0].message.content.strip()
            
            # Cache the response
            if not hasattr(self, '_response_cache'):
                self._response_cache = {}
            self._response_cache[cache_key] = enhanced_response
            
            return enhanced_response if enhanced_response else base_response
            
        except Exception as e:
            return base_response
        
        # Original LLM enhancement code kept but disabled for speed
        # Uncomment below if you want AI enhancement (slower but more personalized)
        """
        if not self.client:
            return base_response
        
        try:
            # Create a prompt for response enhancement
            prompt = self._create_enhancement_prompt(base_response, context)
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,  # Reduced for faster response
                temperature=0.7
            )
            
            enhanced_response = response.choices[0].message.content.strip()
            return enhanced_response if enhanced_response else base_response
            
        except Exception as e:
            return base_response  # Fail silently for speed
        """
    
    def generate_follow_up_question(self, candidate_data: Dict[str, Any]) -> Optional[str]:
        """Generate intelligent follow-up questions"""
        if not self.client:
            return None
        
        try:
            prompt = self._create_follow_up_prompt(candidate_data)
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.error(f"Error generating follow-up: {str(e)}")
            return None
    
    def analyze_technical_response(self, question: str, answer: str) -> Dict[str, Any]:
        """Analyze technical response quality"""
        if not self.client:
            return {"score": "N/A", "feedback": "LLM analysis not available"}
        
        try:
            prompt = f"""
            Analyze this technical interview response:
            
            Question: {question}
            Answer: {answer}
            
            Provide a brief analysis including:
            1. Technical accuracy (if determinable)
            2. Completeness of answer
            3. Communication clarity
            4. Overall assessment
            
            Keep the response concise and professional.
            """
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a technical interviewer analyzing candidate responses."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            analysis = response.choices[0].message.content.strip()
            return {"analysis": analysis}
            
        except Exception as e:
            return {"error": f"Analysis error: {str(e)}"}
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for the LLM"""
        return """You are a friendly, conversational AI recruiter for TalentScout. Think of yourself as a cool, approachable tech recruiter who genuinely enjoys talking to candidates.

Your personality:
- Casual but professional - like chatting with a knowledgeable friend
- Enthusiastic about technology and people's career journeys  
- Encouraging and positive, never intimidating
- Curious about people's experiences and projects
- Uses natural language, contractions, and conversational phrases

Your approach:
- Make candidates feel comfortable and excited about opportunities
- Ask follow-up questions that show genuine interest
- Relate to their experiences when appropriate
- Keep things conversational, not robotic or formal
- Show enthusiasm for their skills and background
- Use emojis sparingly but naturally

Remember: This is a conversation, not an interrogation. You want candidates to leave feeling good about TalentScout and excited about potential opportunities."""
    
    def _create_enhancement_prompt(self, base_response: str, context: Dict[str, Any]) -> str:
        """Create prompt for response enhancement"""
        return f"""
        Make this recruiting conversation response more natural and engaging:
        
        Current response: {base_response}
        
        Context:
        - Conversation stage: {context.get('state', 'unknown')}
        - Candidate's name: {context.get('candidate_name', 'candidate')}
        - What we're discussing: {context.get('current_field', 'general conversation')}
        
        Transform it to be:
        1. More conversational and natural (like talking to a friend)
        2. Enthusiastic but not over-the-top
        3. Personalized using their name when appropriate
        4. Encouraging and positive
        5. Clear and easy to understand
        
        Keep the same information but make it sound like a real person talking, not a bot. Use contractions, natural phrases, and show genuine interest in the candidate.
        """
    
    def _create_follow_up_prompt(self, candidate_data: Dict[str, Any]) -> str:
        """Create prompt for follow-up question generation"""
        tech_stack = candidate_data.get('tech_stack', {})
        experience = candidate_data.get('experience_years', 0)
        position = candidate_data.get('desired_position', 'developer')
        
        return f"""
        Generate a thoughtful follow-up question for a candidate with:
        - Experience: {experience} years
        - Desired position: {position}
        - Tech stack: {tech_stack}
        
        The question should be:
        1. Relevant to their experience level
        2. Related to their tech stack or desired role
        3. Professional and engaging
        4. Not too technical (this is initial screening)
        
        Provide just the question, no additional text.
        """