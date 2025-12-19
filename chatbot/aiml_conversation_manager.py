"""
AIML-Enhanced Conversation Manager for Intelligent Hiring Assistant
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enum import Enum
from typing import Dict, List, Optional, Any
import streamlit as st
from utils.data_handler import CandidateDataHandler
from utils.question_generator import TechnicalQuestionGenerator
from config import Config
from aiml_patterns.aiml_engine import AIMLEngine

class ConversationState(Enum):
    """Enumeration of conversation states"""
    GREETING = "greeting"
    COLLECTING_INFO = "collecting_info"
    TECH_STACK_COLLECTION = "tech_stack_collection"
    TECHNICAL_QUESTIONS = "technical_questions"
    COMPLETED = "completed"
    ENDED = "ended"

class AIMLConversationManager:
    """AIML-Enhanced Conversation Manager with intelligent pattern matching"""
    
    def __init__(self):
        self.data_handler = CandidateDataHandler()
        self.question_generator = TechnicalQuestionGenerator()
        self.aiml_engine = AIMLEngine()
        self.current_state = ConversationState.GREETING
        self.session_id = "default"
        
        # Hybrid approach: AIML + Rule-based logic
        self.use_aiml_for_states = [
            ConversationState.GREETING,
            ConversationState.COMPLETED,
            ConversationState.ENDED
        ]
        
        # Cache for performance
        self._response_cache = {}
        
        # Field collection order for structured data
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
            'tech_stack': "Now for the fun part! Tell me about your tech stack - what languages, frameworks, databases, and tools do you work with?"
        }
        
        self.field_index = 0
    
    def initialize_session_state(self):
        """Initialize Streamlit session state with AIML integration"""
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
        if 'aiml_session_id' not in st.session_state:
            st.session_state.aiml_session_id = f"session_{len(st.session_state.messages)}"
        
        self.session_id = st.session_state.aiml_session_id
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input using hybrid AIML + rule-based approach"""
        current_state = st.session_state.conversation_state
        
        # Check for exit keywords first
        if self.is_exit_keyword(user_input):
            return self.handle_conversation_end()
        
        # Use AIML for certain states or as fallback
        if current_state in self.use_aiml_for_states or self.should_use_aiml(user_input):
            return self.process_with_aiml(user_input)
        
        # Use rule-based logic for structured data collection
        if current_state == ConversationState.COLLECTING_INFO:
            return self.handle_info_collection(user_input)
        elif current_state == ConversationState.TECH_STACK_COLLECTION:
            return self.handle_tech_stack_collection(user_input)
        elif current_state == ConversationState.TECHNICAL_QUESTIONS:
            return self.handle_technical_questions(user_input)
        else:
            return self.process_with_aiml(user_input)
    
    def should_use_aiml(self, user_input: str) -> bool:
        """Determine if AIML should handle this input"""
        # Use AIML for conversational, open-ended responses
        aiml_triggers = [
            'what', 'how', 'why', 'tell me', 'explain', 'describe',
            'talentscout', 'company', 'process', 'salary', 'benefits',
            'culture', 'team', 'work', 'remote', 'office'
        ]
        
        user_lower = user_input.lower()
        
        # Don't use AIML for tech stack collection - let rule-based handle it
        if st.session_state.conversation_state == ConversationState.TECH_STACK_COLLECTION:
            # Check if this looks like a tech stack list
            tech_indicators = ['python', 'javascript', 'java', 'react', 'django', 'flask', 'sql', 'mysql', 'postgresql', 'mongodb', 'docker', 'kubernetes', 'aws', 'azure']
            if any(tech in user_lower for tech in tech_indicators):
                return False  # Use rule-based handling
        
        return any(trigger in user_lower for trigger in aiml_triggers)
    
    def process_with_aiml(self, user_input: str) -> str:
        """Process input using AIML engine"""
        try:
            # Special handling for greeting state - be more permissive with names
            if st.session_state.conversation_state == ConversationState.GREETING:
                # Check if it's likely a name (single word, 2-20 characters, alphabetic)
                cleaned_input = user_input.strip()
                if (len(cleaned_input.split()) == 1 and 
                    2 <= len(cleaned_input) <= 20 and 
                    cleaned_input.isalpha()):
                    # Treat as a name
                    name = cleaned_input.title()
                    st.session_state.candidate_data['full_name'] = name
                    st.session_state.conversation_state = ConversationState.COLLECTING_INFO
                    st.session_state.field_index = 1  # Move to email collection
                    return f"Great to meet you, {name}! What's the best email to reach you at?"
            
            # Get AIML response
            aiml_result = self.aiml_engine.process_input(user_input, self.session_id)
            
            # Update session state with extracted context
            self.update_session_from_aiml_context(aiml_result['context'])
            
            # Enhance response based on current conversation state
            enhanced_response = self.enhance_aiml_response(
                aiml_result['response'], 
                aiml_result['context'],
                aiml_result['intent']
            )
            
            return enhanced_response
            
        except Exception as e:
            print(f"❌ AIML processing error: {e}")
            return self.get_fallback_response()
    
    def update_session_from_aiml_context(self, context: Dict[str, Any]):
        """Update Streamlit session state from AIML extracted context"""
        if context.get('name'):
            st.session_state.candidate_data['full_name'] = context['name']
            if st.session_state.conversation_state == ConversationState.GREETING:
                st.session_state.conversation_state = ConversationState.COLLECTING_INFO
                st.session_state.field_index = 1  # Move to email collection
        
        if context.get('email'):
            st.session_state.candidate_data['email'] = context['email']
        
        if context.get('phone'):
            st.session_state.candidate_data['phone'] = context['phone']
        
        if context.get('experience_years'):
            st.session_state.candidate_data['experience_years'] = str(context['experience_years'])
        
        # Update tech stack from AIML context
        from config import Config
        tech_stack = {}
        for category in Config.COMMON_TECHNOLOGIES.keys():
            if context.get(category):
                tech_stack[category] = context[category]
        
        if tech_stack:
            st.session_state.candidate_data['tech_stack'] = tech_stack
            if st.session_state.conversation_state in [ConversationState.COLLECTING_INFO, ConversationState.TECH_STACK_COLLECTION]:
                st.session_state.conversation_state = ConversationState.TECHNICAL_QUESTIONS
    
    def enhance_aiml_response(self, aiml_response: str, context: Dict[str, Any], intent: str) -> str:
        """Enhance AIML response based on conversation context"""
        # If AIML detected tech stack, generate technical questions
        from config import Config
        if context and any(key in context for key in Config.COMMON_TECHNOLOGIES.keys()):
            tech_stack = {k: v for k, v in context.items() if k in Config.COMMON_TECHNOLOGIES.keys()}
            
            # Generate technical questions
            questions = self.question_generator.generate_questions(tech_stack, Config.MAX_QUESTIONS_PER_TECH)
            if questions:
                st.session_state.generated_questions = questions
                
                # Add technical questions to the response
                tech_summary = []
                for category, technologies in tech_stack.items():
                    if technologies:
                        tech_summary.append(f"**{category.title()}**: {', '.join(technologies)}")
                
                if tech_summary:
                    tech_display = '\n'.join(tech_summary)
                    aiml_response += f"\n\nHere's what I picked up:\n{tech_display}"
                
                # Add first technical question
                first_tech, first_questions = next(iter(questions.items()))
                if first_questions:
                    aiml_response += f"\n\n💭 **{first_tech}**: {first_questions[0]}\n\nWhat would you like to chat about?"
        
        return aiml_response
    
    def handle_info_collection(self, user_input: str) -> str:
        """Handle structured information collection"""
        current_field = self.field_order[st.session_state.field_index]
        user_response = user_input.strip()
        
        # Try AIML first for natural extraction
        aiml_result = self.aiml_engine.process_input(user_input, self.session_id)
        context = aiml_result['context']
        
        # Check if AIML extracted the needed field
        field_mapping = {
            'email': 'email',
            'phone': 'phone',
            'experience_years': 'experience_years',
            'desired_position': 'desired_position',
            'location': 'location'
        }
        
        if current_field in field_mapping and context.get(field_mapping[current_field]):
            # AIML successfully extracted the field
            extracted_value = context[field_mapping[current_field]]
            st.session_state.candidate_data[current_field] = str(extracted_value)
            st.session_state.field_index += 1
            
            # Natural transition
            if st.session_state.field_index >= len(self.field_order):
                st.session_state.conversation_state = ConversationState.TECH_STACK_COLLECTION
                return f"Great! Now for my favorite part - {self.field_prompts['tech_stack']}"
            else:
                next_field = self.field_order[st.session_state.field_index]
                return f"Perfect! {self.field_prompts[next_field]}"
        
        # Fallback to rule-based validation
        if self.data_handler.store_candidate_info(current_field, user_response):
            st.session_state.candidate_data[current_field] = user_response
            st.session_state.field_index += 1
            
            if st.session_state.field_index >= len(self.field_order):
                st.session_state.conversation_state = ConversationState.TECH_STACK_COLLECTION
                return f"Excellent! Now for my favorite part - {self.field_prompts['tech_stack']}"
            else:
                next_field = self.field_order[st.session_state.field_index]
                return f"Great! {self.field_prompts[next_field]}"
        else:
            # Use AIML for natural error handling
            return aiml_result['response'] if aiml_result['confidence'] > 0.5 else f"Could you help me out with that {current_field.replace('_', ' ')} again? {self.field_prompts[current_field]}"
    
    def handle_tech_stack_collection(self, user_input: str) -> str:
        """Handle tech stack collection with AIML enhancement"""
        # Use AIML to extract tech stack
        aiml_result = self.aiml_engine.process_input(user_input, self.session_id)
        context = aiml_result['context']
        
        # Build tech stack from AIML context
        from config import Config
        tech_stack = {}
        for category in Config.COMMON_TECHNOLOGIES.keys():
            if context.get(category):
                tech_stack[category] = context[category]
        
        # Fallback to rule-based parsing if AIML didn't extract enough
        if not tech_stack:
            tech_stack = self.data_handler.parse_tech_stack(user_input)
        
        if tech_stack:
            st.session_state.candidate_data['tech_stack'] = tech_stack
            self.data_handler.store_candidate_info('tech_stack', user_input)
            
            # Generate technical questions with industry awareness
            questions = self.question_generator.generate_questions(tech_stack, Config.MAX_QUESTIONS_PER_TECH)
            
            # Add industry-specific questions if applicable
            try:
                from utils.industry_question_sets import industry_questions, Industry
                
                # Detect industry from candidate data and conversation
                conversation_context = [msg['content'] for msg in st.session_state.messages if msg['role'] == 'user']
                detected_industry = industry_questions.detect_industry_from_context(
                    st.session_state.candidate_data, conversation_context
                )
                
                if detected_industry != Industry.GENERAL:
                    industry_questions_dict = industry_questions.get_industry_specific_questions(
                        detected_industry, tech_stack, 2
                    )
                    
                    # Merge industry questions with general questions
                    questions.update(industry_questions_dict)
                    
                    # Store industry info for later use
                    st.session_state.detected_industry = detected_industry.value
                
            except Exception as e:
                print(f"Industry detection error: {e}")
            
            st.session_state.generated_questions = questions
            st.session_state.conversation_state = ConversationState.TECHNICAL_QUESTIONS
            
            # Create a natural response for tech stack
            from utils.candidate_scorer import CandidateScorer
            scorer = CandidateScorer()
            _, depth_score, tech_analysis = scorer.calculate_tech_stack_score(tech_stack)
            
            # Smart response based on tech stack quality
            if tech_analysis['modern_stack']:
                starter = "Impressive! You're working with a really modern tech stack."
            elif tech_analysis['full_stack']:
                starter = "Great! I can see you have full-stack capabilities."
            elif depth_score >= 8:
                starter = "Nice! You've got some solid technical depth there."
            else:
                starter = "Thanks for sharing your tech stack with me."
            
            # Format tech stack display
            tech_summary = []
            for category, technologies in tech_stack.items():
                if technologies:
                    tech_summary.append(f"**{category.title()}**: {', '.join(technologies)}")
            
            tech_display = '\n'.join(tech_summary)
            
            # Display multiple questions from different technologies
            if questions:
                questions_display = []
                question_count = 0
                max_display_questions = 5  # Show up to 5 questions initially
                
                for tech, tech_questions in questions.items():
                    for i, question in enumerate(tech_questions):
                        if question_count >= max_display_questions:
                            break
                        question_count += 1
                        questions_display.append(f"💭 **{tech}**: {question}")
                    if question_count >= max_display_questions:
                        break
                
                questions_text = "\n\n".join(questions_display)
                total_questions = sum(len(q) for q in questions.values())
                
                return f"""{starter} Here's what I picked up:

{tech_display}

Now, I'd love to dive a bit deeper! I've got {total_questions} questions that match your experience. Don't worry about giving perfect textbook answers - I'm more interested in hearing about your real-world experience and how you think about these technologies.

Pick any question that interests you, or feel free to tell me about a recent project you've worked on:

{questions_text}

What would you like to chat about?"""
            else:
                return f"""{starter} Here's what I picked up:

{tech_display}

Tell me about a challenging project you've worked on with these technologies!"""
        else:
            return """I'm having a bit of trouble parsing that tech stack. No worries though! 

Could you help me out by listing them a bit more clearly? Something like:
- Languages: Python, JavaScript
- Frameworks: React, Django  
- Databases: PostgreSQL
- Tools: Docker, Git

Or just throw them at me in a list - whatever's easier for you!"""
    
    def handle_technical_questions(self, user_input: str) -> str:
        """Handle technical questions with AIML intelligence and advanced question generation"""
        # Use AIML for natural response analysis
        aiml_result = self.aiml_engine.process_input(user_input, self.session_id)
        
        # Track questions answered
        if 'questions_answered' not in st.session_state:
            st.session_state.questions_answered = 0
        
        st.session_state.questions_answered += 1
        
        # Store response
        if 'technical_responses' not in st.session_state:
            st.session_state.technical_responses = []
        
        st.session_state.technical_responses.append({
            'question_number': st.session_state.questions_answered,
            'response': user_input,
            'aiml_analysis': aiml_result,
            'timestamp': str(st.session_state.get('current_time', 'unknown'))
        })
        
        # Analyze response quality and adapt difficulty
        response_analysis = self.analyze_response_quality(user_input, aiml_result)
        
        # Check if we should continue or complete
        max_questions = 8  # Increased for more comprehensive assessment
        
        if st.session_state.questions_answered >= max_questions:
            st.session_state.conversation_state = ConversationState.COMPLETED
            return self.generate_completion_response(aiml_result)
        else:
            return self.generate_advanced_follow_up_response(aiml_result, response_analysis)
    
    def generate_completion_response(self, aiml_result: Dict[str, Any]) -> str:
        """Generate completion response using AIML"""
        candidate_name = st.session_state.candidate_data.get('full_name', 'there')
        
        # Use AIML for natural feedback
        feedback = aiml_result['response'] if aiml_result['confidence'] > 0.7 else "That's a great perspective!"
        
        return f"""{feedback} Thanks for sharing your thoughts, {candidate_name}.

I really enjoyed our conversation! You've got a solid background and it's clear you know your stuff. Here's what we covered today:

✅ Got to know you and your background
✅ Learned about your {st.session_state.candidate_data.get('experience_years', 'X')} years of experience  
✅ Explored your tech stack and skills
✅ Had some great technical discussions

**What happens next?**
Our team will review everything we talked about today. You should hear back from us within 2-3 business days. If there's a good fit with any of our current openings, we'll set up a more detailed conversation with the hiring team.

I had a great time chatting with you today! Is there anything you'd like to know about TalentScout, our process, or the types of roles we're working on?"""
    
    def analyze_response_quality(self, user_input: str, aiml_result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze response quality to determine skill level and next question difficulty"""
        response_length = len(user_input.split())
        
        # Technical depth indicators
        technical_keywords = [
            'architecture', 'performance', 'optimization', 'scalability', 'design pattern',
            'algorithm', 'complexity', 'memory', 'concurrency', 'async', 'threading',
            'microservices', 'monolith', 'database', 'indexing', 'caching', 'security',
            'authentication', 'authorization', 'encryption', 'testing', 'deployment',
            'ci/cd', 'docker', 'kubernetes', 'cloud', 'monitoring', 'logging'
        ]
        
        technical_score = sum(1 for keyword in technical_keywords if keyword in user_input.lower())
        
        # Experience indicators
        experience_keywords = [
            'production', 'project', 'team', 'built', 'implemented', 'designed',
            'optimized', 'scaled', 'deployed', 'maintained', 'refactored',
            'migrated', 'integrated', 'collaborated', 'led', 'mentored'
        ]
        
        experience_score = sum(1 for keyword in experience_keywords if keyword in user_input.lower())
        
        # Determine skill level
        if response_length > 50 and (technical_score >= 3 or experience_score >= 2):
            skill_level = 'advanced'
        elif response_length > 25 and (technical_score >= 1 or experience_score >= 1):
            skill_level = 'intermediate'
        else:
            skill_level = 'beginner'
        
        return {
            'skill_level': skill_level,
            'technical_score': technical_score,
            'experience_score': experience_score,
            'response_length': response_length,
            'confidence': aiml_result.get('confidence', 0.5)
        }
    
    def generate_advanced_follow_up_response(self, aiml_result: Dict[str, Any], response_analysis: Dict[str, Any]) -> str:
        """Generate advanced follow-up response based on skill level analysis"""
        # Use AIML response as base feedback
        feedback = aiml_result['response'] if aiml_result['confidence'] > 0.7 else "Excellent insight!"
        
        skill_level = response_analysis['skill_level']
        tech_stack = st.session_state.candidate_data.get('tech_stack', {})
        
        # Generate advanced questions based on detected skill level and tech stack
        advanced_question = self.get_advanced_question(skill_level, tech_stack, st.session_state.questions_answered)
        
        if advanced_question:
            return f"""{feedback} I can see you have solid experience with this.

Let me dive deeper into your expertise:

💭 **{advanced_question['category']}**: {advanced_question['question']}

I'm particularly interested in your real-world experience and problem-solving approach."""
        else:
            # Fallback to contextual follow-up
            return self.create_contextual_follow_up_aiml(feedback, aiml_result)
    
    def get_advanced_question(self, skill_level: str, tech_stack: Dict[str, List[str]], question_number: int) -> Optional[Dict[str, str]]:
        """Get advanced questions based on skill level and tech stack"""
        
        # Advanced question bank organized by technology and difficulty
        advanced_questions = {
            'python': {
                'intermediate': [
                    "How do you handle exception handling in Python? Any best practices you follow?",
                    "Explain Python's memory management and garbage collection. Any performance issues you've encountered?",
                    "What's your experience with Python's asyncio? When would you choose it over threading?",
                    "How do you structure large Python applications? What design patterns do you use?"
                ],
                'advanced': [
                    "Explain Python's GIL and its implications for multi-threaded applications. How do you work around it?",
                    "How do you implement custom metaclasses in Python? Can you give a real-world example?",
                    "Describe your approach to Python performance profiling and optimization in production systems.",
                    "How do you handle memory leaks in long-running Python applications? What tools do you use?"
                ]
            },
            'javascript': {
                'intermediate': [
                    "How do you handle asynchronous operations in JavaScript? Promises vs async/await?",
                    "Explain JavaScript's event loop and how it affects performance.",
                    "What's your approach to error handling in JavaScript applications?",
                    "How do you manage state in complex JavaScript applications?"
                ],
                'advanced': [
                    "Explain JavaScript's prototype chain and how you'd implement inheritance without classes.",
                    "How do you optimize JavaScript performance for large-scale applications?",
                    "Describe your approach to memory management and preventing memory leaks in JavaScript.",
                    "How do you implement custom iterators and generators in JavaScript?"
                ]
            },
            'react': {
                'intermediate': [
                    "How do you optimize React component performance? What techniques do you use?",
                    "Explain React's reconciliation algorithm and how it affects rendering.",
                    "What's your approach to state management in large React applications?",
                    "How do you handle side effects in React? useEffect best practices?"
                ],
                'advanced': [
                    "How do you implement custom React hooks for complex business logic?",
                    "Explain React's Fiber architecture and how it improves performance.",
                    "How do you handle React application performance at scale? Code splitting, lazy loading?",
                    "Describe your approach to React testing strategies for complex components."
                ]
            },
            'system_design': {
                'intermediate': [
                    "How would you design a scalable REST API that handles 10,000 requests per minute?",
                    "Explain your approach to database design for a social media application.",
                    "How do you implement caching strategies in web applications?",
                    "What's your approach to handling authentication and authorization in microservices?"
                ],
                'advanced': [
                    "Design a distributed system that can handle millions of concurrent users.",
                    "How would you implement a real-time messaging system like WhatsApp?",
                    "Explain your approach to data consistency in distributed databases.",
                    "How do you design fault-tolerant systems? Circuit breakers, retries, fallbacks?"
                ]
            },
            'databases': {
                'intermediate': [
                    "How do you optimize slow database queries? What tools and techniques do you use?",
                    "Explain ACID properties and how they affect database design decisions.",
                    "What's your approach to database migrations in production systems?",
                    "How do you handle database scaling? Vertical vs horizontal scaling?"
                ],
                'advanced': [
                    "How do you implement database sharding strategies for high-traffic applications?",
                    "Explain your approach to handling eventual consistency in distributed databases.",
                    "How do you design database schemas for time-series data at scale?",
                    "Describe your strategy for database disaster recovery and backup systems."
                ]
            },
            'devops': {
                'intermediate': [
                    "How do you structure Docker containers for production applications?",
                    "Explain your CI/CD pipeline design and deployment strategies.",
                    "What's your approach to monitoring and logging in production systems?",
                    "How do you handle secrets management in containerized applications?"
                ],
                'advanced': [
                    "How do you implement blue-green deployments with zero downtime?",
                    "Explain your approach to Kubernetes cluster management and scaling strategies.",
                    "How do you design infrastructure as code for multi-environment deployments?",
                    "Describe your strategy for handling security vulnerabilities in production systems."
                ]
            }
        }
        
        # Determine which category to ask about based on tech stack
        available_categories = []
        
        # Map tech stack to question categories
        for category, technologies in tech_stack.items():
            if not technologies:
                continue
                
            for tech in technologies:
                tech_lower = tech.lower()
                if tech_lower in ['python', 'django', 'flask', 'fastapi']:
                    available_categories.append('python')
                elif tech_lower in ['javascript', 'typescript', 'node.js', 'nodejs']:
                    available_categories.append('javascript')
                elif tech_lower in ['react', 'vue', 'angular']:
                    available_categories.append('react')
                elif tech_lower in ['postgresql', 'mysql', 'mongodb', 'redis']:
                    available_categories.append('databases')
                elif tech_lower in ['docker', 'kubernetes', 'jenkins', 'aws', 'azure']:
                    available_categories.append('devops')
        
        # Always include system design for intermediate+ candidates
        if skill_level in ['intermediate', 'advanced']:
            available_categories.append('system_design')
        
        # Remove duplicates and select category
        available_categories = list(set(available_categories))
        
        if not available_categories:
            return None
        
        # Rotate through categories to ensure variety
        category = available_categories[question_number % len(available_categories)]
        
        # Select appropriate difficulty level
        difficulty = skill_level if skill_level in ['intermediate', 'advanced'] else 'intermediate'
        
        if category in advanced_questions and difficulty in advanced_questions[category]:
            questions = advanced_questions[category][difficulty]
            question = questions[question_number % len(questions)]
            
            return {
                'category': category.replace('_', ' ').title(),
                'question': question,
                'difficulty': difficulty
            }
        
        return None
    
    def create_contextual_follow_up_aiml(self, feedback: str, aiml_result: Dict[str, Any]) -> str:
        """Create contextual follow-up using AIML analysis"""
        context = aiml_result.get('context', {})
        intent = aiml_result.get('intent', 'general')
        
        # Use AIML to generate contextual questions based on detected intent and entities
        contextual_questions = []
        
        if intent == 'project':
            contextual_questions = [
                "That sounds like an interesting project! What was the most challenging part?",
                "Cool! What technologies did you choose and why?",
                "How did you handle deployment and scaling?"
            ]
        elif intent == 'tech_stack':
            contextual_questions = [
                "How do you approach debugging complex issues?",
                "What's your process for code reviews?",
                "How do you stay current with new technologies?"
            ]
        else:
            # Default behavioral questions
            contextual_questions = [
                "How do you explain complex technical concepts to non-technical stakeholders?",
                "Tell me about a time when you had to learn something new quickly.",
                "What's your approach to handling tight deadlines?"
            ]
        
        import random
        selected_question = random.choice(contextual_questions)
        
        return f"""{feedback} 

I'd love to hear more about your experience. Here's something I'm curious about:

💡 **Behavioral**: {selected_question}

Take your time - I'm interested in your real-world perspective!"""
    
    def is_exit_keyword(self, message: str) -> bool:
        """Check if message contains exit keywords"""
        message_lower = message.lower().strip()
        return any(keyword in message_lower for keyword in Config.EXIT_KEYWORDS)
    
    def handle_conversation_end(self) -> str:
        """Handle conversation ending with AIML"""
        st.session_state.conversation_state = ConversationState.ENDED
        
        # Use AIML for natural goodbye
        aiml_result = self.aiml_engine.process_input("goodbye", self.session_id)
        return aiml_result['response']
    
    def get_fallback_response(self) -> str:
        """Get fallback response using AIML"""
        try:
            aiml_result = self.aiml_engine.process_input("I don't understand", self.session_id)
            return aiml_result['response']
        except:
            return """I'm not quite sure I caught that! Could you help me out?

I'm here to chat about your background and experience for TalentScout. You can:
- Answer whatever question I just asked
- Tell me more about yourself or your experience  
- Say 'bye' if you need to wrap up

What would work best for you?"""
    
    def get_greeting_message(self) -> str:
        """Get greeting message using AIML"""
        try:
            aiml_result = self.aiml_engine.process_input("hello", self.session_id)
            return aiml_result['response']
        except:
            return """Hey there! 👋 Welcome to TalentScout! 

I'm your AI assistant, and I'm excited to chat with you today. Think of this as a friendly conversation rather than a formal interview - I'm here to get to know you and your technical background.

What should I call you?"""
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get comprehensive conversation summary"""
        # Combine rule-based and AIML data
        rule_based_summary = {
            'state': st.session_state.conversation_state.value,
            'candidate_data': st.session_state.candidate_data,
            'generated_questions': st.session_state.generated_questions,
            'questions_answered': st.session_state.get('questions_answered', 0),
            'technical_responses': st.session_state.get('technical_responses', [])
        }
        
        # Get AIML conversation summary
        aiml_summary = self.aiml_engine.get_conversation_summary(self.session_id)
        
        # Merge summaries
        return {
            **rule_based_summary,
            'aiml_analysis': aiml_summary,
            'completion_status': st.session_state.conversation_state in [
                ConversationState.COMPLETED, ConversationState.ENDED
            ]
        }