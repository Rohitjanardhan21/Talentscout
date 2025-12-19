"""
Interactive Question Selection System
Allows users to choose specific questions from generated sets
"""
import streamlit as st
from typing import Dict, List, Any, Optional
import random

class InteractiveQuestionSelector:
    """Manages interactive question selection and user preferences"""
    
    def __init__(self):
        self.question_categories = {
            'technical_depth': 'Deep Technical Knowledge',
            'problem_solving': 'Problem Solving & Debugging',
            'best_practices': 'Best Practices & Standards',
            'real_world': 'Real-World Experience',
            'architecture': 'System Design & Architecture',
            'performance': 'Performance & Optimization'
        }
        
        self.difficulty_levels = {
            'junior': 'Entry Level (0-2 years)',
            'mid': 'Mid Level (2-5 years)', 
            'senior': 'Senior Level (5+ years)',
            'expert': 'Expert Level (8+ years)'
        }
    
    def render_question_selection_interface(self, available_questions: Dict[str, List[str]]) -> Dict[str, Any]:
        """Render interactive question selection UI"""
        st.markdown("### 🎯 Customize Your Interview Experience")
        
        selection_preferences = {}
        
        # Question category preferences
        st.markdown("**📋 What areas would you like to focus on?**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            focus_areas = st.multiselect(
                "Select focus areas:",
                options=list(self.question_categories.keys()),
                format_func=lambda x: self.question_categories[x],
                default=['technical_depth', 'real_world'],
                help="Choose the types of questions you'd like to be asked"
            )
        
        with col2:
            difficulty_preference = st.selectbox(
                "Preferred difficulty level:",
                options=list(self.difficulty_levels.keys()),
                format_func=lambda x: self.difficulty_levels[x],
                index=1,  # Default to mid-level
                help="Questions will be adapted to your experience level"
            )
        
        # Technology-specific preferences
        st.markdown("**🔧 Technology Focus**")
        
        tech_priorities = {}
        if available_questions:
            st.write("Rate your interest in discussing each technology (1-5 stars):")
            
            cols = st.columns(min(3, len(available_questions)))
            for i, (tech, questions) in enumerate(available_questions.items()):
                with cols[i % 3]:
                    priority = st.slider(
                        f"{tech}",
                        min_value=1,
                        max_value=5,
                        value=3,
                        help=f"{len(questions)} questions available"
                    )
                    tech_priorities[tech] = priority
        
        # Question quantity preferences
        st.markdown("**📊 Interview Length**")
        
        col1, col2 = st.columns(2)
        with col1:
            total_questions = st.slider(
                "Total questions to ask:",
                min_value=3,
                max_value=15,
                value=8,
                help="Total number of questions for the interview"
            )
        
        with col2:
            questions_per_tech = st.slider(
                "Questions per technology:",
                min_value=1,
                max_value=5,
                value=2,
                help="Maximum questions per technology"
            )
        
        # Interview style preferences
        st.markdown("**🎭 Interview Style**")
        
        interview_style = st.radio(
            "Choose your interview style:",
            options=['conversational', 'structured', 'mixed'],
            format_func=lambda x: {
                'conversational': '💬 Conversational - Natural, flowing discussion',
                'structured': '📋 Structured - Formal, systematic questions',
                'mixed': '🔄 Mixed - Combination of both styles'
            }[x],
            index=0,
            help="This affects how questions are presented and follow-ups are handled"
        )
        
        selection_preferences = {
            'focus_areas': focus_areas,
            'difficulty_level': difficulty_preference,
            'tech_priorities': tech_priorities,
            'total_questions': total_questions,
            'questions_per_tech': questions_per_tech,
            'interview_style': interview_style
        }
        
        return selection_preferences
    
    def generate_personalized_questions(self, 
                                      available_questions: Dict[str, List[str]], 
                                      preferences: Dict[str, Any],
                                      candidate_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate personalized question set based on preferences"""
        
        personalized_questions = {}
        tech_priorities = preferences.get('tech_priorities', {})
        total_questions = preferences.get('total_questions', 8)
        questions_per_tech = preferences.get('questions_per_tech', 2)
        difficulty_level = preferences.get('difficulty_level', 'mid')
        focus_areas = preferences.get('focus_areas', ['technical_depth'])
        
        # Sort technologies by priority
        sorted_techs = sorted(
            available_questions.items(),
            key=lambda x: tech_priorities.get(x[0], 3),
            reverse=True
        )
        
        questions_allocated = 0
        
        for tech, questions in sorted_techs:
            if questions_allocated >= total_questions:
                break
            
            # Filter questions based on difficulty and focus areas
            filtered_questions = self._filter_questions_by_preferences(
                questions, difficulty_level, focus_areas, candidate_data
            )
            
            # Select questions for this technology
            num_questions = min(
                questions_per_tech,
                len(filtered_questions),
                total_questions - questions_allocated
            )
            
            if num_questions > 0:
                selected_questions = random.sample(filtered_questions, num_questions)
                personalized_questions[tech] = selected_questions
                questions_allocated += num_questions
        
        return personalized_questions
    
    def _filter_questions_by_preferences(self, 
                                       questions: List[str], 
                                       difficulty_level: str,
                                       focus_areas: List[str],
                                       candidate_data: Dict[str, Any]) -> List[str]:
        """Filter questions based on difficulty and focus areas"""
        
        # For now, return all questions - in a real implementation,
        # questions would be tagged with difficulty and category metadata
        filtered = questions.copy()
        
        # Adjust based on difficulty level
        experience_years = candidate_data.get('experience_years', 3)
        
        if difficulty_level == 'junior' and experience_years > 5:
            # Mix in some easier questions for senior candidates who want junior-level questions
            pass
        elif difficulty_level == 'expert' and experience_years < 5:
            # Filter out very advanced questions for less experienced candidates
            pass
        
        # Filter based on focus areas
        if 'real_world' in focus_areas:
            # Prioritize questions that ask about experience
            real_world_indicators = ['experience', 'project', 'worked', 'used', 'approach']
            filtered = [q for q in filtered if any(indicator in q.lower() for indicator in real_world_indicators)] + filtered
        
        if 'problem_solving' in focus_areas:
            # Prioritize debugging and problem-solving questions
            problem_indicators = ['debug', 'problem', 'issue', 'challenge', 'solve', 'optimize']
            filtered = [q for q in filtered if any(indicator in q.lower() for indicator in problem_indicators)] + filtered
        
        # Remove duplicates while preserving order
        seen = set()
        unique_filtered = []
        for q in filtered:
            if q not in seen:
                seen.add(q)
                unique_filtered.append(q)
        
        return unique_filtered
    
    def render_question_picker(self, available_questions: Dict[str, List[str]]) -> List[str]:
        """Render a question picker interface for manual selection"""
        st.markdown("### 🎯 Pick Your Questions")
        st.write("Select the specific questions you'd like to answer:")
        
        selected_questions = []
        
        for tech, questions in available_questions.items():
            with st.expander(f"🔧 {tech} Questions ({len(questions)} available)"):
                for i, question in enumerate(questions):
                    if st.checkbox(f"Q{i+1}: {question[:80]}{'...' if len(question) > 80 else ''}", 
                                 key=f"{tech}_{i}"):
                        selected_questions.append(f"**{tech}**: {question}")
        
        if selected_questions:
            st.success(f"✅ {len(selected_questions)} questions selected")
        else:
            st.info("💡 Select questions above to customize your interview")
        
        return selected_questions
    
    def get_adaptive_follow_up(self, 
                             user_response: str, 
                             original_question: str,
                             tech: str,
                             difficulty_level: str) -> Optional[str]:
        """Generate adaptive follow-up questions based on user response"""
        
        response_lower = user_response.lower()
        
        # Analyze response quality and depth
        response_length = len(user_response.split())
        has_examples = any(indicator in response_lower for indicator in ['example', 'project', 'used', 'worked'])
        has_technical_depth = any(indicator in response_lower for indicator in ['because', 'performance', 'optimize', 'design'])
        
        follow_ups = []
        
        # Generate follow-ups based on response analysis
        if response_length < 20:
            follow_ups.append(f"That's interesting! Could you elaborate a bit more on your experience with {tech}?")
        
        if has_examples:
            follow_ups.append("That sounds like a great project! What was the most challenging part of implementing that?")
        
        if has_technical_depth:
            follow_ups.append("Great technical insight! How did you measure the impact of that approach?")
        
        if 'don\'t know' in response_lower or 'not sure' in response_lower:
            follow_ups.append("No worries! How would you approach learning about this if you encountered it in a project?")
        
        # Difficulty-based follow-ups
        if difficulty_level == 'senior' and response_length > 50:
            follow_ups.append("Excellent! How would you explain this concept to a junior developer on your team?")
        
        return random.choice(follow_ups) if follow_ups else None

# Global instance
interactive_selector = InteractiveQuestionSelector()