"""
Intelligent Question Selection System
Selects optimal questions based on candidate profile, experience, and industry
"""
import random
from typing import Dict, List, Tuple, Any
from knowledge_base.advanced_questions import (
    ADVANCED_QUESTION_BANK, 
    INDUSTRY_QUESTIONS, 
    BEHAVIORAL_QUESTIONS,
    get_questions_by_experience_and_tech,
    get_system_design_questions,
    get_industry_questions,
    get_behavioral_questions
)
from knowledge_base.industry_profiles import get_industry_profile, get_role_requirements

class IntelligentQuestionSelector:
    """Advanced question selection based on candidate profile"""
    
    def __init__(self):
        self.experience_levels = {
            (0, 1): 'junior',
            (1, 3): 'mid',
            (3, 7): 'senior',
            (7, 100): 'architect'
        }
    
    def determine_experience_level(self, years: int) -> str:
        """Determine experience level from years"""
        for (min_years, max_years), level in self.experience_levels.items():
            if min_years <= years < max_years:
                return level
        return 'junior'
    
    def detect_industry_from_position(self, position: str) -> str:
        """Detect industry from job position"""
        position_lower = position.lower()
        
        industry_keywords = {
            'fintech': ['fintech', 'financial', 'banking', 'payment', 'trading', 'blockchain'],
            'healthcare': ['healthcare', 'medical', 'health', 'clinical', 'hospital', 'pharma'],
            'ecommerce': ['ecommerce', 'e-commerce', 'retail', 'marketplace', 'shopping'],
            'gaming': ['gaming', 'game', 'unity', 'unreal', 'mobile game'],
            'enterprise_saas': ['enterprise', 'saas', 'b2b', 'crm', 'erp'],
            'media_streaming': ['media', 'streaming', 'video', 'content', 'entertainment']
        }
        
        for industry, keywords in industry_keywords.items():
            if any(keyword in position_lower for keyword in keywords):
                return industry
        
        return 'general'
    
    def select_optimal_questions(self, candidate_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Select optimal questions based on complete candidate profile"""
        
        # Extract candidate information
        experience_years = int(str(candidate_data.get('experience_years', 0)))
        tech_stack = candidate_data.get('tech_stack', {})
        desired_position = candidate_data.get('desired_position', '')
        
        # Determine levels and context
        experience_level = self.determine_experience_level(experience_years)
        industry = self.detect_industry_from_position(desired_position)
        
        selected_questions = {}
        
        # 1. Technical Questions (Primary Technologies)
        primary_techs = self._get_primary_technologies(tech_stack)
        for tech in primary_techs[:3]:  # Focus on top 3 technologies
            tech_questions = get_questions_by_experience_and_tech(tech, experience_level, 2)
            if tech_questions:
                selected_questions[f"{tech}_technical"] = tech_questions
        
        # 2. System Design Questions (Mid+ level)
        if experience_level in ['mid', 'senior', 'architect']:
            system_questions = get_system_design_questions(experience_level, 2)
            if system_questions:
                selected_questions['system_design'] = system_questions
        
        # 3. Industry-Specific Questions
        if industry != 'general':
            industry_questions = get_industry_questions(industry, 2)
            if industry_questions:
                selected_questions['industry_specific'] = industry_questions
        
        # 4. Behavioral Questions (Senior+ level)
        if experience_level in ['senior', 'architect']:
            behavioral_questions = self._select_behavioral_questions(desired_position, 2)
            if behavioral_questions:
                selected_questions['behavioral'] = behavioral_questions
        
        # 5. Role-Specific Questions
        role_questions = self._get_role_specific_questions(desired_position, tech_stack, experience_level)
        if role_questions:
            selected_questions['role_specific'] = role_questions
        
        return selected_questions
    
    def _get_primary_technologies(self, tech_stack: Dict[str, List[str]]) -> List[str]:
        """Identify primary technologies from tech stack"""
        # Priority order for technology categories
        priority_order = ['languages', 'frameworks', 'databases', 'cloud_platforms', 'devops_tools']
        
        primary_techs = []
        
        for category in priority_order:
            if category in tech_stack and tech_stack[category]:
                # Add technologies from this category
                primary_techs.extend(tech_stack[category])
                if len(primary_techs) >= 5:  # Limit to top 5
                    break
        
        # If no priority categories, add from any available category
        if not primary_techs:
            for category, techs in tech_stack.items():
                primary_techs.extend(techs)
                if len(primary_techs) >= 3:
                    break
        
        return primary_techs[:5]  # Return top 5
    
    def _select_behavioral_questions(self, position: str, count: int) -> List[str]:
        """Select behavioral questions based on position"""
        position_lower = position.lower()
        
        # Determine behavioral focus based on position
        if any(keyword in position_lower for keyword in ['senior', 'lead', 'principal', 'architect']):
            # Leadership and problem-solving focus
            questions = []
            questions.extend(get_behavioral_questions('leadership', 1))
            questions.extend(get_behavioral_questions('problem_solving', 1))
            return questions[:count]
        else:
            # Communication and adaptability focus
            questions = []
            questions.extend(get_behavioral_questions('communication', 1))
            questions.extend(get_behavioral_questions('adaptability', 1))
            return questions[:count]
    
    def _get_role_specific_questions(self, position: str, tech_stack: Dict, experience_level: str) -> List[str]:
        """Generate role-specific questions"""
        position_lower = position.lower()
        questions = []
        
        # Frontend Developer Questions
        if any(keyword in position_lower for keyword in ['frontend', 'front-end', 'ui', 'react', 'vue']):
            if experience_level == 'junior':
                questions.append("How do you ensure your web applications work across different browsers?")
                questions.append("What's your approach to making websites responsive for mobile devices?")
            else:
                questions.append("How do you optimize frontend performance for large applications?")
                questions.append("What's your approach to state management in complex frontend applications?")
        
        # Backend Developer Questions
        elif any(keyword in position_lower for keyword in ['backend', 'back-end', 'api', 'server']):
            if experience_level == 'junior':
                questions.append("How do you design a RESTful API for a simple application?")
                questions.append("What's your approach to handling errors in backend applications?")
            else:
                questions.append("How do you design APIs for high-traffic applications?")
                questions.append("What's your strategy for database optimization in production systems?")
        
        # Full Stack Developer Questions
        elif any(keyword in position_lower for keyword in ['full stack', 'fullstack', 'full-stack']):
            if experience_level == 'junior':
                questions.append("How do you handle data flow between frontend and backend in your applications?")
                questions.append("What's your approach to user authentication in full-stack applications?")
            else:
                questions.append("How do you architect a full-stack application for scalability?")
                questions.append("What's your approach to testing across the entire application stack?")
        
        # DevOps Engineer Questions
        elif any(keyword in position_lower for keyword in ['devops', 'infrastructure', 'platform', 'sre']):
            if experience_level == 'junior':
                questions.append("How do you set up a basic CI/CD pipeline for a web application?")
                questions.append("What's your approach to monitoring application health in production?")
            else:
                questions.append("How do you design infrastructure for zero-downtime deployments?")
                questions.append("What's your strategy for handling infrastructure scaling during traffic spikes?")
        
        return questions[:2]  # Return top 2 role-specific questions
    
    def generate_question_explanation(self, question: str, technology: str, experience_level: str) -> str:
        """Generate explanation for why this question was selected"""
        explanations = {
            'junior': f"This {technology} question tests fundamental understanding suitable for your experience level.",
            'mid': f"This {technology} question evaluates practical application skills expected at the mid-level.",
            'senior': f"This {technology} question assesses advanced knowledge and architectural thinking.",
            'architect': f"This {technology} question explores system design and leadership capabilities."
        }
        
        return explanations.get(experience_level, "This question evaluates your technical knowledge.")
    
    def get_question_difficulty_score(self, experience_level: str) -> int:
        """Get difficulty score for questions based on experience level"""
        difficulty_scores = {
            'junior': 3,
            'mid': 5,
            'senior': 7,
            'architect': 9
        }
        return difficulty_scores.get(experience_level, 3)
    
    def format_questions_with_context(self, questions_dict: Dict[str, List[str]], 
                                    candidate_data: Dict[str, Any]) -> str:
        """Format questions with context and explanations"""
        if not questions_dict:
            return "I'll ask you some general questions about your experience."
        
        experience_years = int(str(candidate_data.get('experience_years', 0)))
        experience_level = self.determine_experience_level(experience_years)
        
        formatted_output = f"Based on your {experience_years} years of experience and tech stack, I have some targeted questions:\n\n"
        
        question_count = 1
        for category, questions in questions_dict.items():
            category_name = category.replace('_', ' ').title()
            
            if 'technical' in category:
                tech_name = category.split('_')[0]
                formatted_output += f"**{tech_name.title()} Questions:**\n"
            else:
                formatted_output += f"**{category_name}:**\n"
            
            for question in questions:
                formatted_output += f"{question_count}. {question}\n"
                question_count += 1
            
            formatted_output += "\n"
        
        formatted_output += "Feel free to choose any question that interests you, or I can ask about a specific area!"
        
        return formatted_output