"""
Skill Level Adaptation System
Dynamically adjusts questions and follow-ups based on candidate responses
"""
import re
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import streamlit as st

class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class ResponseAnalyzer:
    """Analyzes user responses to determine skill level and adapt questions"""
    
    def __init__(self):
        self.skill_indicators = {
            SkillLevel.BEGINNER: {
                'keywords': ['basic', 'simple', 'learning', 'tutorial', 'beginner', 'new to'],
                'patterns': [r'i\s+(don\'t|haven\'t|never)', r'not\s+familiar', r'just\s+started'],
                'complexity_score': 1
            },
            SkillLevel.INTERMEDIATE: {
                'keywords': ['experience', 'worked with', 'used in projects', 'comfortable', 'familiar'],
                'patterns': [r'i\s+(have|use|work)', r'in\s+my\s+projects', r'usually\s+use'],
                'complexity_score': 2
            },
            SkillLevel.ADVANCED: {
                'keywords': ['optimize', 'performance', 'architecture', 'design patterns', 'best practices'],
                'patterns': [r'performance\s+optimization', r'design\s+patterns', r'scalability'],
                'complexity_score': 3
            },
            SkillLevel.EXPERT: {
                'keywords': ['deep dive', 'internals', 'implementation details', 'contribute', 'mentor'],
                'patterns': [r'under\s+the\s+hood', r'low\s+level', r'contribute\s+to', r'mentor'],
                'complexity_score': 4
            }
        }
        
        self.technical_depth_indicators = [
            'because', 'due to', 'performance', 'memory', 'cpu', 'optimization',
            'algorithm', 'complexity', 'trade-off', 'pros and cons'
        ]
        
        self.experience_indicators = [
            'project', 'production', 'team', 'client', 'deployed', 'maintained',
            'scaled', 'refactored', 'debugged', 'troubleshooting'
        ]
    
    def analyze_response(self, response: str, question_context: str = "") -> Dict[str, Any]:
        """Analyze a response and return skill assessment"""
        response_lower = response.lower()
        
        analysis = {
            'estimated_skill_level': SkillLevel.INTERMEDIATE,
            'confidence': 0.5,
            'technical_depth_score': 0,
            'experience_score': 0,
            'response_quality': 'medium',
            'key_insights': [],
            'suggested_follow_up_type': 'clarification'
        }
        
        # Calculate response metrics
        word_count = len(response.split())
        sentence_count = len(re.split(r'[.!?]+', response))
        
        # Analyze technical depth
        technical_depth = sum(1 for indicator in self.technical_depth_indicators 
                            if indicator in response_lower)
        analysis['technical_depth_score'] = min(technical_depth / 3, 1.0)
        
        # Analyze experience indicators
        experience_score = sum(1 for indicator in self.experience_indicators 
                             if indicator in response_lower)
        analysis['experience_score'] = min(experience_score / 3, 1.0)
        
        # Determine skill level based on indicators
        skill_scores = {}
        for skill_level, indicators in self.skill_indicators.items():
            score = 0
            
            # Keyword matching
            keyword_matches = sum(1 for keyword in indicators['keywords'] 
                                if keyword in response_lower)
            score += keyword_matches * 0.3
            
            # Pattern matching
            pattern_matches = sum(1 for pattern in indicators['patterns'] 
                                if re.search(pattern, response_lower))
            score += pattern_matches * 0.4
            
            # Complexity indicators
            if word_count > 50 and skill_level in [SkillLevel.ADVANCED, SkillLevel.EXPERT]:
                score += 0.2
            if technical_depth > 2 and skill_level in [SkillLevel.ADVANCED, SkillLevel.EXPERT]:
                score += 0.3
            
            skill_scores[skill_level] = score
        
        # Determine most likely skill level
        if skill_scores:
            best_skill = max(skill_scores, key=skill_scores.get)
            analysis['estimated_skill_level'] = best_skill
            analysis['confidence'] = min(skill_scores[best_skill], 1.0)
        
        # Determine response quality
        if word_count < 10:
            analysis['response_quality'] = 'low'
        elif word_count > 100 and technical_depth > 1:
            analysis['response_quality'] = 'high'
        else:
            analysis['response_quality'] = 'medium'
        
        # Generate insights
        insights = []
        if technical_depth > 2:
            insights.append("Shows strong technical understanding")
        if experience_score > 2:
            insights.append("Demonstrates practical experience")
        if word_count > 80:
            insights.append("Provides detailed explanations")
        if any(word in response_lower for word in ['example', 'project', 'used']):
            insights.append("Gives concrete examples")
        
        analysis['key_insights'] = insights
        
        # Suggest follow-up type
        if analysis['response_quality'] == 'low':
            analysis['suggested_follow_up_type'] = 'elaboration'
        elif technical_depth > 2:
            analysis['suggested_follow_up_type'] = 'deeper_technical'
        elif experience_score > 1:
            analysis['suggested_follow_up_type'] = 'practical_application'
        else:
            analysis['suggested_follow_up_type'] = 'clarification'
        
        return analysis

class AdaptiveQuestionGenerator:
    """Generates questions adapted to detected skill level"""
    
    def __init__(self):
        self.question_templates = {
            SkillLevel.BEGINNER: {
                'technical': [
                    "Can you explain what {concept} is and when you might use it?",
                    "What's your understanding of {concept}?",
                    "Have you worked with {concept} before? What was your experience?",
                    "How would you describe {concept} to someone new to programming?"
                ],
                'practical': [
                    "Tell me about a time you used {technology} in a project.",
                    "What resources do you use to learn about {technology}?",
                    "What challenges have you faced when working with {technology}?"
                ]
            },
            SkillLevel.INTERMEDIATE: {
                'technical': [
                    "How do you approach {concept} in your projects?",
                    "What are the trade-offs you consider when using {concept}?",
                    "Can you walk me through your process for implementing {concept}?",
                    "What best practices do you follow when working with {concept}?"
                ],
                'practical': [
                    "Tell me about a challenging problem you solved using {technology}.",
                    "How do you handle debugging issues with {technology}?",
                    "What's your experience with scaling applications using {technology}?"
                ]
            },
            SkillLevel.ADVANCED: {
                'technical': [
                    "How would you optimize {concept} for performance in a large-scale application?",
                    "What are the internal mechanisms behind {concept} and how do they affect your design decisions?",
                    "How do you evaluate different approaches to implementing {concept}?",
                    "What architectural patterns do you use when working with {concept}?"
                ],
                'practical': [
                    "Describe a complex system you've designed using {technology}.",
                    "How do you mentor junior developers on {technology} best practices?",
                    "What's your approach to performance tuning with {technology}?"
                ]
            },
            SkillLevel.EXPERT: {
                'technical': [
                    "How would you contribute to the {technology} ecosystem or community?",
                    "What are the fundamental limitations of {concept} and how do you work around them?",
                    "How do you stay current with the evolution of {concept} and its ecosystem?",
                    "What innovations or improvements would you like to see in {concept}?"
                ],
                'practical': [
                    "Tell me about a time you had to make critical architectural decisions involving {technology}.",
                    "How do you evaluate and adopt new tools or versions in the {technology} ecosystem?",
                    "What's your philosophy on balancing innovation with stability when using {technology}?"
                ]
            }
        }
        
        self.follow_up_templates = {
            'elaboration': [
                "That's interesting! Could you elaborate on that a bit more?",
                "Can you give me a specific example of what you mean?",
                "Tell me more about your experience with that."
            ],
            'deeper_technical': [
                "Great technical insight! How does that affect performance in practice?",
                "That's a solid approach. What trade-offs did you consider?",
                "Excellent! How would you explain this to a team member?"
            ],
            'practical_application': [
                "That sounds like valuable experience. What was the outcome?",
                "How did you measure the success of that approach?",
                "What would you do differently if you faced a similar situation again?"
            ],
            'clarification': [
                "Can you help me understand your reasoning behind that choice?",
                "What factors influenced your decision to use that approach?",
                "How did you learn about that technique or tool?"
            ]
        }
    
    def generate_adaptive_question(self, 
                                 technology: str, 
                                 concept: str,
                                 skill_level: SkillLevel,
                                 question_type: str = 'technical') -> str:
        """Generate a question adapted to the detected skill level"""
        
        templates = self.question_templates.get(skill_level, {})
        question_templates = templates.get(question_type, templates.get('technical', []))
        
        if not question_templates:
            return f"Tell me about your experience with {technology}."
        
        import random
        template = random.choice(question_templates)
        
        # Replace placeholders
        question = template.replace('{technology}', technology)
        question = question.replace('{concept}', concept)
        
        return question
    
    def generate_follow_up(self, 
                          analysis: Dict[str, Any], 
                          original_question: str,
                          technology: str) -> Optional[str]:
        """Generate an appropriate follow-up question"""
        
        follow_up_type = analysis.get('suggested_follow_up_type', 'clarification')
        templates = self.follow_up_templates.get(follow_up_type, [])
        
        if not templates:
            return None
        
        import random
        return random.choice(templates)

class SkillLevelAdapter:
    """Main class that coordinates skill level adaptation"""
    
    def __init__(self):
        self.analyzer = ResponseAnalyzer()
        self.question_generator = AdaptiveQuestionGenerator()
        self.session_analysis = {}
    
    def process_response_and_adapt(self, 
                                 user_response: str,
                                 question_context: str,
                                 technology: str,
                                 session_id: str) -> Dict[str, Any]:
        """Process response and return adaptation recommendations"""
        
        # Analyze the response
        analysis = self.analyzer.analyze_response(user_response, question_context)
        
        # Store in session analysis
        if session_id not in self.session_analysis:
            self.session_analysis[session_id] = {
                'responses': [],
                'skill_progression': [],
                'overall_skill_level': SkillLevel.INTERMEDIATE
            }
        
        self.session_analysis[session_id]['responses'].append({
            'response': user_response,
            'analysis': analysis,
            'technology': technology,
            'timestamp': st.session_state.get('current_time', 'unknown')
        })
        
        # Update overall skill assessment
        self._update_overall_skill_level(session_id, analysis)
        
        # Generate follow-up if appropriate
        follow_up = self.question_generator.generate_follow_up(
            analysis, question_context, technology
        )
        
        # Generate next adaptive question
        overall_skill = self.session_analysis[session_id]['overall_skill_level']
        next_question = self.question_generator.generate_adaptive_question(
            technology, technology, overall_skill
        )
        
        return {
            'analysis': analysis,
            'follow_up_question': follow_up,
            'next_adaptive_question': next_question,
            'overall_skill_level': overall_skill.value,
            'session_insights': self._generate_session_insights(session_id)
        }
    
    def _update_overall_skill_level(self, session_id: str, analysis: Dict[str, Any]):
        """Update the overall skill level assessment for the session"""
        
        session_data = self.session_analysis[session_id]
        responses = session_data['responses']
        
        if len(responses) < 2:
            return
        
        # Calculate weighted average of skill levels
        skill_values = {
            SkillLevel.BEGINNER: 1,
            SkillLevel.INTERMEDIATE: 2,
            SkillLevel.ADVANCED: 3,
            SkillLevel.EXPERT: 4
        }
        
        total_score = 0
        total_weight = 0
        
        for response_data in responses[-5:]:  # Consider last 5 responses
            resp_analysis = response_data['analysis']
            skill_level = resp_analysis['estimated_skill_level']
            confidence = resp_analysis['confidence']
            
            total_score += skill_values[skill_level] * confidence
            total_weight += confidence
        
        if total_weight > 0:
            avg_score = total_score / total_weight
            
            # Map back to skill level
            if avg_score < 1.5:
                overall_skill = SkillLevel.BEGINNER
            elif avg_score < 2.5:
                overall_skill = SkillLevel.INTERMEDIATE
            elif avg_score < 3.5:
                overall_skill = SkillLevel.ADVANCED
            else:
                overall_skill = SkillLevel.EXPERT
            
            session_data['overall_skill_level'] = overall_skill
    
    def _generate_session_insights(self, session_id: str) -> List[str]:
        """Generate insights about the candidate's performance"""
        
        if session_id not in self.session_analysis:
            return []
        
        session_data = self.session_analysis[session_id]
        responses = session_data['responses']
        
        if not responses:
            return []
        
        insights = []
        
        # Analyze response quality trend
        recent_responses = responses[-3:]
        avg_quality = sum(1 for r in recent_responses 
                         if r['analysis']['response_quality'] == 'high') / len(recent_responses)
        
        if avg_quality > 0.6:
            insights.append("Consistently provides detailed, high-quality responses")
        elif avg_quality < 0.3:
            insights.append("Responses could benefit from more detail and examples")
        
        # Analyze technical depth
        avg_tech_depth = sum(r['analysis']['technical_depth_score'] 
                           for r in recent_responses) / len(recent_responses)
        
        if avg_tech_depth > 0.7:
            insights.append("Demonstrates strong technical understanding")
        elif avg_tech_depth < 0.3:
            insights.append("Could elaborate more on technical concepts")
        
        # Analyze experience indicators
        avg_experience = sum(r['analysis']['experience_score'] 
                           for r in recent_responses) / len(recent_responses)
        
        if avg_experience > 0.7:
            insights.append("Shows substantial practical experience")
        elif avg_experience < 0.3:
            insights.append("Would benefit from sharing more practical examples")
        
        return insights
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive session analysis summary"""
        
        if session_id not in self.session_analysis:
            return {}
        
        session_data = self.session_analysis[session_id]
        
        return {
            'overall_skill_level': session_data['overall_skill_level'].value,
            'total_responses': len(session_data['responses']),
            'session_insights': self._generate_session_insights(session_id),
            'skill_progression': [r['analysis']['estimated_skill_level'].value 
                                for r in session_data['responses']],
            'average_response_quality': sum(1 for r in session_data['responses'] 
                                          if r['analysis']['response_quality'] == 'high') / len(session_data['responses']) if session_data['responses'] else 0
        }

# Global instance
skill_adapter = SkillLevelAdapter()