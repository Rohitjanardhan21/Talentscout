"""
Conversation management and state handling for the hiring assistant
"""
from enum import Enum
from typing import Dict, List, Optional, Any
import streamlit as st
from utils.data_handler import CandidateDataHandler
from utils.question_generator import TechnicalQuestionGenerator
from config import Config

class ConversationState(Enum):
    """Enumeration of conversation states"""
    GREETING = "greeting"
    COLLECTING_INFO = "collecting_info"
    TECH_STACK_COLLECTION = "tech_stack_collection"
    TECHNICAL_QUESTIONS = "technical_questions"
    COMPLETED = "completed"
    ENDED = "ended"

class ConversationManager:
    """Manages the conversation flow and state"""
    
    def __init__(self):
        self.data_handler = CandidateDataHandler()
        self.question_generator = TechnicalQuestionGenerator()
        self.current_state = ConversationState.GREETING
        self.current_field = None
        self.generated_questions = {}
        
        # Cache for faster responses
        self._response_cache = {}
        
        # Field collection order and prompts
        self.field_order = [
            'full_name', 'email', 'phone', 'experience_years', 
            'desired_position', 'location'
        ]
        
        self.field_prompts = {
            'full_name': "What should I call you?",
            'email': "Great! What's the best email to reach you at?",
            'phone': "And your phone number? (Don't worry, we keep everything secure!)",
            'experience_years': "Nice! How long have you been working in tech? Just give me a rough number of years.",
            'desired_position': "What kind of role are you looking for? Feel free to mention a few if you're open to different opportunities!",
            'location': "Where are you based? Just city and country is fine.",
            'tech_stack': "Now for the fun part! Tell me about your tech stack - what languages, frameworks, databases, and tools do you work with? Don't worry about being comprehensive, just mention the main ones you're comfortable with."
        }
        
        self.field_index = 0
    
    def initialize_session_state(self):
        """Initialize Streamlit session state"""
        if 'conversation_state' not in st.session_state:
            st.session_state.conversation_state = ConversationState.GREETING
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'candidate_data' not in st.session_state:
            st.session_state.candidate_data = {}
        if 'field_index' not in st.session_state:
            st.session_state.field_index = 0
        if 'generated_questions' not in st.session_state:
            st.session_state.generated_questions = {}
        if 'questions_answered' not in st.session_state:
            st.session_state.questions_answered = 0
        if 'technical_responses' not in st.session_state:
            st.session_state.technical_responses = []
    
    def is_exit_keyword(self, message: str) -> bool:
        """Check if message contains exit keywords"""
        message_lower = message.lower().strip()
        return any(keyword in message_lower for keyword in Config.EXIT_KEYWORDS)
    
    def get_greeting_message(self) -> str:
        """Get the initial greeting message"""
        return """
        Hey there! 👋 Welcome to TalentScout! 
        
        I'm your AI assistant, and I'm excited to chat with you today. Think of this as a friendly conversation rather than a formal interview - I'm here to get to know you and your technical background.
        
        We'll spend about 5-10 minutes together. I'll ask about your experience, what you're looking for, and dive into some tech topics that match your skills. Feel free to be conversational - no need for formal answers!
        
        If you need to step away at any point, just say 'bye' or 'thanks' and we can wrap up.
        
        So, let's start with the basics - what should I call you?
        """
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input based on current conversation state"""
        # Check for exit keywords first
        if self.is_exit_keyword(user_input):
            return self.handle_conversation_end()
        
        current_state = st.session_state.conversation_state
        
        if current_state == ConversationState.GREETING:
            return self.handle_greeting_response(user_input)
        elif current_state == ConversationState.COLLECTING_INFO:
            return self.handle_info_collection(user_input)
        elif current_state == ConversationState.TECH_STACK_COLLECTION:
            return self.handle_tech_stack_collection(user_input)
        elif current_state == ConversationState.TECHNICAL_QUESTIONS:
            return self.handle_technical_questions(user_input)
        elif current_state == ConversationState.COMPLETED:
            return self.handle_completed_state(user_input)
        else:
            return self.get_fallback_response()
    
    def handle_greeting_response(self, user_input: str) -> str:
        """Handle response after greeting"""
        # Store the name and move to info collection
        name = user_input.strip()
        if self.data_handler.store_candidate_info('full_name', name):
            st.session_state.candidate_data['full_name'] = name
            st.session_state.conversation_state = ConversationState.COLLECTING_INFO
            st.session_state.field_index = 1  # Start with email
            
            # Faster response - no random selection
            return f"Great to meet you, {name}! {self.field_prompts['email']}"
        else:
            return "I didn't quite catch that - could you tell me your name again?"
    
    def handle_info_collection(self, user_input: str) -> str:
        """Handle information collection phase"""
        current_field = self.field_order[st.session_state.field_index]
        user_response = user_input.strip()
        
        # Natural validation responses
        validation_responses = {
            'email': [
                "Hmm, that doesn't look like a valid email format. Could you double-check that for me?",
                "I think there might be a typo in that email. Mind trying again?",
                "That email format seems off - could you give it another shot?"
            ],
            'phone': [
                "That phone number doesn't look quite right. Could you try again?",
                "I'm having trouble with that phone format. Could you give me the number again?",
                "That doesn't seem like a valid phone number. Mind trying once more?"
            ],
            'experience_years': [
                "I need a number for years of experience. How many years would you say?",
                "Could you give me that as a number? Like 3, 5, 10 years?",
                "Just need a rough number of years - how long have you been in tech?"
            ]
        }
        
        # Validate and store the current field
        if self.data_handler.store_candidate_info(current_field, user_response):
            st.session_state.candidate_data[current_field] = user_response
            st.session_state.field_index += 1
            
            # Faster transitions - no random selection
            transition_map = {
                'email': "Got it!",
                'phone': "Great!",
                'experience_years': f"Nice! {user_response} years of experience.",
                'desired_position': "That sounds exciting!",
                'location': f"Cool! {user_response} is a great place for tech."
            }
            
            # Check if we've collected all basic info
            if st.session_state.field_index >= len(self.field_order):
                st.session_state.conversation_state = ConversationState.TECH_STACK_COLLECTION
                return f"Excellent! Now for my favorite part - {self.field_prompts['tech_stack']}"
            else:
                next_field = self.field_order[st.session_state.field_index]
                transition = transition_map.get(current_field, "Great!")
                return f"{transition} {self.field_prompts[next_field]}"
        else:
            # Natural error responses
            import random
            if current_field in validation_responses:
                return random.choice(validation_responses[current_field])
            else:
                return f"Could you help me out with that {current_field.replace('_', ' ')} again? {self.field_prompts[current_field]}"
    
    def handle_tech_stack_collection(self, user_input: str) -> str:
        """Handle tech stack collection and question generation"""
        # Parse and store tech stack
        tech_stack = self.data_handler.parse_tech_stack(user_input)
        
        if tech_stack:
            st.session_state.candidate_data['tech_stack'] = tech_stack
            self.data_handler.store_candidate_info('tech_stack', user_input)
            
            # Generate technical questions
            questions = self.question_generator.generate_questions(
                tech_stack, Config.MAX_QUESTIONS_PER_TECH
            )
            st.session_state.generated_questions = questions
            
            st.session_state.conversation_state = ConversationState.TECHNICAL_QUESTIONS
            
            # Smart response based on tech stack quality
            from utils.candidate_scorer import CandidateScorer
            scorer = CandidateScorer()
            _, depth_score, tech_analysis = scorer.calculate_tech_stack_score(tech_stack)
            
            if tech_analysis['modern_stack']:
                starter = "Impressive! You're working with a really modern tech stack."
            elif tech_analysis['full_stack']:
                starter = "Great! I can see you have full-stack capabilities."
            elif depth_score >= 8:
                starter = "Nice! You've got some solid technical depth there."
            else:
                starter = "Thanks for sharing your tech stack with me."
            
            if questions:
                # More conversational question presentation
                tech_summary = []
                for category, technologies in tech_stack.items():
                    if technologies:
                        tech_summary.append(f"**{category.title()}**: {', '.join(technologies)}")
                
                tech_display = '\n'.join(tech_summary)
                
                return f"""{starter} Here's what I picked up:

{tech_display}

Now, I'd love to dive a bit deeper! I've got some questions that match your experience. Don't worry about giving perfect textbook answers - I'm more interested in hearing about your real-world experience and how you think about these technologies.

Pick any question that interests you, or feel free to tell me about a recent project you've worked on:

{self._format_questions_naturally(questions)}

What would you like to chat about?"""
            else:
                # Fallback to general questions
                experience_years = st.session_state.candidate_data.get('experience_years', 0)
                level = "senior" if int(str(experience_years)) > 5 else "junior" if int(str(experience_years)) < 3 else "general"
                fallback_questions = self.question_generator.get_fallback_questions(level)
                
                return f"""{starter} 

Since I want to learn more about your experience, here are some questions I'd love to hear your thoughts on:

{self._format_fallback_questions_naturally(fallback_questions)}

Feel free to pick whichever one resonates with you, or tell me about something cool you've been working on lately!"""
        else:
            return """I'm having a bit of trouble parsing that tech stack. No worries though! 

Could you help me out by listing them a bit more clearly? Something like:
- Languages: Python, JavaScript
- Frameworks: React, Django  
- Databases: PostgreSQL
- Tools: Docker, Git

Or just throw them at me in a list - whatever's easier for you!"""
    
    def handle_technical_questions(self, user_input: str) -> str:
        """Handle technical question responses with proper context awareness"""
        candidate_name = st.session_state.candidate_data.get('full_name', 'there')
        
        # Initialize question counter if not exists
        if 'questions_answered' not in st.session_state:
            st.session_state.questions_answered = 0
        
        # Increment question counter
        st.session_state.questions_answered += 1
        
        # Store the response for analysis
        if 'technical_responses' not in st.session_state:
            st.session_state.technical_responses = []
        
        st.session_state.technical_responses.append({
            'question_number': st.session_state.questions_answered,
            'response': user_input,
            'timestamp': str(st.session_state.get('current_time', 'unknown'))
        })
        
        # Natural responses to their technical answer
        positive_responses = [
            "That's a great perspective!",
            "I love how you explained that!",
            "Really solid thinking there!",
            "Nice! That shows good understanding.",
            "Excellent way to approach that problem!",
            "That's exactly the kind of insight we're looking for!"
        ]
        
        import random
        feedback = random.choice(positive_responses)
        
        # Check if we should continue with more questions or wrap up
        max_questions = 3  # Allow up to 3 technical questions
        
        if st.session_state.questions_answered >= max_questions:
            # End the technical questioning phase
            st.session_state.conversation_state = ConversationState.COMPLETED
            
            return f"""{feedback} Thanks for sharing your thoughts, {candidate_name}.

I really enjoyed our conversation! You've got a solid background and it's clear you know your stuff. Here's what we covered today:

✅ Got to know you and your background
✅ Learned about your {st.session_state.candidate_data.get('experience_years', 'X')} years of experience  
✅ Explored your tech stack and skills
✅ Had some great technical discussions

**What happens next?**
Our team will review everything we talked about today. You should hear back from us within 2-3 business days. If there's a good fit with any of our current openings, we'll set up a more detailed conversation with the hiring team.

I had a great time chatting with you today! Is there anything you'd like to know about TalentScout, our process, or the types of roles we're working on?"""
        else:
            # Continue with follow-up questions
            return self._generate_follow_up_response(feedback, candidate_name, user_input)
    
    def _generate_follow_up_response(self, feedback: str, candidate_name: str, user_input: str) -> str:
        """Generate contextual follow-up questions"""
        # Get remaining questions from the generated set
        remaining_questions = []
        generated_questions = st.session_state.get('generated_questions', {})
        
        for tech, questions in generated_questions.items():
            for question in questions:
                remaining_questions.append((tech, question))
        
        # If we have more generated questions, use them
        if remaining_questions and st.session_state.questions_answered < len(remaining_questions):
            tech, next_question = remaining_questions[st.session_state.questions_answered]
            
            follow_up_intros = [
                "Great! Let me ask you about something else.",
                "Awesome! I'm curious about another area.",
                "Nice! Here's another one I'd love your thoughts on.",
                "Perfect! Let's dive into something different.",
                "Excellent! I have another question for you."
            ]
            
            import random
            intro = random.choice(follow_up_intros)
            
            return f"""{feedback} {intro}

💭 **{tech}**: {next_question}

Feel free to share your experience or approach to this!"""
        
        # If no more generated questions, create contextual follow-ups
        else:
            return self._create_contextual_follow_up(feedback, candidate_name, user_input)
    
    def _create_contextual_follow_up(self, feedback: str, candidate_name: str, user_input: str) -> str:
        """Create contextual follow-up based on their previous response"""
        tech_stack = st.session_state.candidate_data.get('tech_stack', {})
        experience_years = int(str(st.session_state.candidate_data.get('experience_years', 0)))
        
        # Analyze their response for keywords to create relevant follow-ups
        user_input_lower = user_input.lower()
        
        contextual_questions = []
        
        # Project-based follow-ups
        if any(word in user_input_lower for word in ['project', 'built', 'developed', 'created', 'worked on']):
            contextual_questions.extend([
                "That sounds like an interesting project! What was the most challenging part of building that?",
                "Cool! What technologies did you choose for that project and why?",
                "Nice! How did you handle the deployment and scaling for that project?"
            ])
        
        # Problem-solving follow-ups
        if any(word in user_input_lower for word in ['problem', 'issue', 'challenge', 'bug', 'error']):
            contextual_questions.extend([
                "Great problem-solving approach! How do you typically debug complex issues?",
                "That's a solid way to handle problems! What's your process for troubleshooting?",
                "Nice! Tell me about a time when you had to solve a really tricky technical problem."
            ])
        
        # Architecture/design follow-ups
        if any(word in user_input_lower for word in ['architecture', 'design', 'structure', 'pattern']):
            contextual_questions.extend([
                "Good thinking on architecture! How do you approach designing scalable systems?",
                "That's a great architectural perspective! What design patterns do you find most useful?",
                "Excellent! How do you balance performance and maintainability in your designs?"
            ])
        
        # Experience-based follow-ups
        if experience_years >= 5:
            contextual_questions.extend([
                "With your experience, how do you mentor junior developers?",
                "What's the biggest technical decision you've had to make in a project?",
                "How do you stay current with new technologies and trends?"
            ])
        elif experience_years >= 2:
            contextual_questions.extend([
                "What's been your favorite technology to work with so far?",
                "How do you approach learning new frameworks or tools?",
                "What kind of projects are you most excited to work on?"
            ])
        else:
            contextual_questions.extend([
                "What got you interested in software development?",
                "What's the most exciting thing you've learned recently?",
                "What kind of role are you hoping to grow into?"
            ])
        
        # Default behavioral questions if no context matches
        if not contextual_questions:
            contextual_questions = [
                "How do you explain complex technical concepts to non-technical stakeholders?",
                "Tell me about a time when you had to learn a new technology quickly.",
                "What's your approach to code reviews and collaboration?",
                "How do you handle tight deadlines while maintaining code quality?"
            ]
        
        import random
        selected_question = random.choice(contextual_questions)
        
        return f"""{feedback} 

I'd love to hear more about your experience. Here's something I'm curious about:

💡 **Behavioral**: {selected_question}

Take your time - I'm interested in hearing your real-world perspective on this!"""
    
    def handle_completed_state(self, user_input: str) -> str:
        """Handle conversation after completion - allow for questions about company/process"""
        candidate_name = st.session_state.candidate_data.get('full_name', 'there')
        user_input_lower = user_input.lower()
        
        # Check if they're asking about the company, process, or roles
        if any(word in user_input_lower for word in ['talentscout', 'company', 'process', 'role', 'position', 'job', 'opportunity', 'culture', 'team', 'work', 'office', 'remote', 'salary', 'benefits', 'next steps', 'timeline']):
            
            # Provide relevant information based on their question
            if any(word in user_input_lower for word in ['culture', 'team', 'work environment', 'office']):
                return f"""Great question, {candidate_name}! TalentScout partners with some amazing tech companies that really value their engineering teams.

Most of our client companies offer:
🏢 Flexible work arrangements (remote, hybrid, or in-office)
👥 Collaborative, learning-focused environments  
🚀 Opportunities to work on cutting-edge projects
📈 Clear career growth paths and mentorship
🎯 Focus on work-life balance

The specific culture varies by company, but we only work with organizations that treat their developers well and invest in their growth.

Is there anything specific about work environment you're looking for?"""
            
            elif any(word in user_input_lower for word in ['process', 'next steps', 'timeline', 'hear back']):
                return f"""Sure thing, {candidate_name}! Here's what happens next:

📋 **Next 2-3 days**: Our team reviews your profile and matches you with relevant opportunities
📞 **If there's a match**: We'll reach out to schedule a more detailed conversation with the hiring team
🎯 **Company interviews**: Usually 2-3 rounds depending on the role and company
⚡ **Timeline**: Most of our processes wrap up within 2-3 weeks total

We'll keep you updated throughout the process, and you can always reach out if you have questions!

Any other aspects of the process you'd like to know about?"""
            
            elif any(word in user_input_lower for word in ['role', 'position', 'job', 'opportunity']):
                tech_stack = st.session_state.candidate_data.get('tech_stack', {})
                experience = st.session_state.candidate_data.get('experience_years', 0)
                
                return f"""Absolutely, {candidate_name}! Based on your background, here are the types of roles we're seeing high demand for:

🔥 **Hot right now**:
- Full-stack developers (especially with your tech stack!)
- Backend engineers with {', '.join(tech_stack.get('languages', ['Python', 'JavaScript']))} experience
- Frontend developers with modern frameworks
- DevOps/Cloud engineers

💰 **Salary ranges** (varies by location and company):
- {experience}+ years experience: Usually very competitive packages
- Remote opportunities available across different time zones
- Many include equity, great benefits, and learning budgets

Would you like me to focus on any particular type of role or company size?"""
            
            else:
                return f"""Thanks for asking, {candidate_name}! I'm happy to share more about TalentScout.

We're a tech-focused recruitment agency that partners with innovative companies - from fast-growing startups to established tech leaders. What makes us different:

✨ **We're technical**: Our team understands the technologies you work with
🎯 **Quality over quantity**: We focus on finding the right fit, not just any job
🤝 **Candidate-first**: We're here to help your career, not just fill positions
🚀 **Modern companies**: We work with organizations that value engineering excellence

What would you like to know more about - our process, the types of companies we work with, or something else?"""
        
        # If they're not asking about company/process, politely wrap up
        else:
            return f"""Thanks so much, {candidate_name}! 

The technical part of our conversation is complete, but I'm happy to answer any questions you might have about TalentScout, our process, or the types of opportunities we're working on.

Otherwise, you should hear from us within 2-3 business days if there's a good match with any of our current openings.

Have a great day! 👋"""
    
    def handle_conversation_end(self) -> str:
        """Handle conversation ending"""
        st.session_state.conversation_state = ConversationState.ENDED
        
        candidate_name = st.session_state.candidate_data.get('full_name', 'there')
        
        # Natural goodbye responses
        goodbyes = [
            f"Thanks so much for your time, {candidate_name}! It was great chatting with you.",
            f"Really enjoyed talking with you, {candidate_name}! Thanks for stopping by.",
            f"It was a pleasure meeting you, {candidate_name}! Thanks for the conversation.",
            f"Great talking with you today, {candidate_name}! Thanks for your time."
        ]
        
        import random
        goodbye = random.choice(goodbyes)
        
        if len(st.session_state.candidate_data) > 2:  # If we got some info
            return f"""{goodbye}

Even though we didn't finish everything, I got some good insights about your background. If you want to pick up where we left off sometime, just start a new chat - no problem at all!

Best of luck with your job search, and I hope we get to work together soon! 👋"""
        else:
            return f"""{goodbye}

No worries about not finishing - these things happen! If you're interested in exploring opportunities with TalentScout in the future, feel free to come back anytime.

Take care and best of luck with everything! 👋"""
    
    def get_fallback_response(self) -> str:
        """Get fallback response for unexpected inputs"""
        fallback_responses = [
            "I'm not quite sure I caught that! Could you help me out?",
            "Hmm, I didn't quite understand. Could you try rephrasing that?",
            "I think I missed something there. Mind trying again?",
            "Sorry, that went over my head! Could you say that differently?",
            "I'm a bit confused by that response. Could you clarify?"
        ]
        
        import random
        response = random.choice(fallback_responses)
        
        return f"""{response}

I'm here to chat about your background and experience for TalentScout. You can:
- Answer whatever question I just asked
- Tell me more about yourself or your experience  
- Say 'bye' if you need to wrap up

What would work best for you?"""
    
    def _format_tech_stack(self, tech_stack: Dict[str, List[str]]) -> str:
        """Format tech stack for display"""
        formatted = ""
        for category, technologies in tech_stack.items():
            if technologies:
                formatted += f"- **{category.title()}**: {', '.join(technologies)}\n"
        return formatted
    
    def _format_questions_naturally(self, questions_dict: Dict[str, List[str]]) -> str:
        """Format technical questions in a natural, conversational way"""
        if not questions_dict:
            return "Let me think of some good questions for you..."
        
        formatted_output = ""
        question_intros = [
            "💭 ",
            "🤔 ",
            "💡 ",
            "🔍 ",
            "⚡ "
        ]
        
        import random
        for tech, questions in list(questions_dict.items())[:3]:  # Limit to 3 technologies
            for question in questions[:1]:  # One question per tech
                intro = random.choice(question_intros)
                formatted_output += f"{intro} **{tech}**: {question}\n\n"
        
        return formatted_output.strip()
    
    def _format_fallback_questions_naturally(self, questions: List[str]) -> str:
        """Format fallback questions in a natural way"""
        formatted = ""
        question_intros = ["💭 ", "🤔 ", "💡 "]
        
        import random
        for i, question in enumerate(questions[:3], 1):  # Limit to 3 questions
            intro = random.choice(question_intros)
            formatted += f"{intro} {question}\n\n"
        return formatted.strip()
    
    def _format_fallback_questions(self, questions: List[str]) -> str:
        """Format fallback questions for display"""
        formatted = ""
        for i, question in enumerate(questions[:3], 1):  # Limit to 3 questions
            formatted += f"{i}. {question}\n"
        return formatted
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of the conversation"""
        return {
            'state': st.session_state.conversation_state.value,
            'candidate_data': st.session_state.candidate_data,
            'generated_questions': st.session_state.generated_questions,
            'completion_status': st.session_state.conversation_state in [
                ConversationState.COMPLETED, ConversationState.ENDED
            ]
        }