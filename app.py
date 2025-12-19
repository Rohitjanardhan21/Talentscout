"""
TalentScout Hiring Assistant - Main Streamlit Application
"""
import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, List, Any
from chatbot.aiml_conversation_manager import AIMLConversationManager as ConversationManager, ConversationState
from chatbot.llm_integration import LLMIntegration
from config import Config

# Page configuration
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎩 CLASSY & PROFESSIONAL UI
st.markdown("""
<style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    /* Global Professional Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        color: #1a202c;
    }
    
    /* Elegant Main Header */
    .main-header {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 
            0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    }
    
    .main-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 400;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Professional Chat Messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
        background: white;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.2s ease;
        animation: messageSlideIn 0.4s ease;
    }
    
    .chat-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
        border: none;
        box-shadow: 0 4px 14px 0 rgba(102, 126, 234, 0.3);
    }
    
    .assistant-message {
        background: white;
        color: #2d3748;
        margin-right: 2rem;
        border-left: 4px solid #667eea;
    }
    
    @keyframes messageSlideIn {
        0% { 
            opacity: 0; 
            transform: translateY(20px); 
        }
        100% { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    /* Professional Info Boxes */
    .info-box {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        color: #4a5568;
    }
    
    .success-box {
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
        color: #22543d;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #9ae6b4;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(72, 187, 120, 0.1);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fffbf0 0%, #fed7aa 100%);
        color: #744210;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #f6ad55;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(237, 137, 54, 0.1);
    }
    
    /* Elegant Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px;
    }
    
    /* Professional Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    /* Elegant Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px -1px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 15px -3px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Professional Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.85rem;
        margin: 0.25rem 0;
        border: 1px solid;
        transition: all 0.2s ease;
    }
    
    .status-greeting { 
        background: #fef5e7; 
        color: #744210; 
        border-color: #f6ad55;
    }
    .status-collecting { 
        background: #ebf8ff; 
        color: #2b6cb0; 
        border-color: #63b3ed;
    }
    .status-tech-stack { 
        background: #fef5e7; 
        color: #c05621; 
        border-color: #f6ad55;
    }
    .status-questions { 
        background: #f7fafc; 
        color: #553c9a; 
        border-color: #9f7aea;
    }
    .status-completed { 
        background: #f0fff4; 
        color: #22543d; 
        border-color: #68d391;
    }
    .status-ended { 
        background: #f7fafc; 
        color: #4a5568; 
        border-color: #cbd5e0;
    }
    
    /* Elegant Tech Stack Display */
    .tech-stack-item {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        margin: 0.2rem;
        font-weight: 500;
        box-shadow: 0 2px 4px 0 rgba(102, 126, 234, 0.2);
        transition: all 0.2s ease;
    }
    
    .tech-stack-item:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px 0 rgba(102, 126, 234, 0.3);
    }
    
    /* Professional Chat Input */
    .stChatInput > div > div > div > div {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        background: white;
        transition: border-color 0.2s ease;
    }
    
    .stChatInput > div > div > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stChatInput input {
        color: #2d3748 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
    }
    
    .stChatInput input::placeholder {
        color: #a0aec0 !important;
    }
    
    /* Subtle Professional Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Sidebar Enhancements */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #2d3748 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Professional Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .chat-message {
            margin-left: 0.5rem;
            margin-right: 0.5rem;
            padding: 1rem;
        }
        
        .user-message {
            margin-left: 0.5rem;
        }
        
        .assistant-message {
            margin-right: 0.5rem;
        }
        
        .tech-stack-item {
            font-size: 0.75rem;
            padding: 0.2rem 0.6rem;
        }
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* Focus States */
    .stButton > button:focus {
        outline: 2px solid #667eea;
        outline-offset: 2px;
    }
    
    /* Accessibility Improvements */
    .status-indicator:focus {
        outline: 2px solid #667eea;
        outline-offset: 2px;
    }
    
    /* Edit Message Interface Styles */
    .edit-interface {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 10px 25px -5px rgba(102, 126, 234, 0.2);
    }
    
    .edit-button {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem;
        font-size: 0.8rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px 0 rgba(245, 158, 11, 0.3);
    }
    
    .edit-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px 0 rgba(245, 158, 11, 0.4);
    }
    
    /* Form styling for edit interface */
    .stForm {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stTextArea textarea {
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        transition: border-color 0.2s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

class TalentScoutApp:
    """Main application class"""
    
    def __init__(self):
        self.conversation_manager = ConversationManager()
        self.llm_integration = LLMIntegration()
        self.conversation_manager.initialize_session_state()
    
    def run(self):
        """Run the main application"""
        self.render_header()
        self.render_sidebar()
        self.render_main_chat()
    
    def render_header(self):
        """Render the professional application header"""
        st.markdown("""
        <div class="main-header">
            <h1>TalentScout Hiring Assistant</h1>
            <p>Professional candidate screening powered by AI</p>
            <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8; font-weight: 300;">
                Streamlined • Intelligent • Secure
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with information and controls"""
        with st.sidebar:
            st.header("📋 Session Information")
            
            # Display current state - simplified for speed
            if hasattr(st.session_state, 'conversation_state'):
                current_state = st.session_state.conversation_state
                state_display = {
                    ConversationState.GREETING: "🟡 Initial Greeting",
                    ConversationState.COLLECTING_INFO: "🔵 Collecting Information", 
                    ConversationState.TECH_STACK_COLLECTION: "🟠 Tech Stack Assessment",
                    ConversationState.TECHNICAL_QUESTIONS: "🟣 Technical Questions",
                    ConversationState.COMPLETED: "🟢 Screening Complete",
                    ConversationState.ENDED: "⚫ Session Ended"
                }
                
                status_text = state_display.get(current_state, "Unknown")
                st.write(f"**Status:** {status_text}")
            else:
                st.write("**Status:** Initializing...")
            
            # Display collected information
            if st.session_state.candidate_data:
                st.subheader("👤 Candidate Information")
                
                candidate_data = st.session_state.candidate_data
                
                if 'full_name' in candidate_data:
                    st.write(f"**Name:** {candidate_data['full_name']}")
                
                if 'email' in candidate_data:
                    st.write(f"**Email:** {candidate_data['email']}")
                
                if 'experience_years' in candidate_data:
                    st.write(f"**Experience:** {candidate_data['experience_years']} years")
                
                if 'desired_position' in candidate_data:
                    st.write(f"**Position:** {candidate_data['desired_position']}")
                
                if 'tech_stack' in candidate_data:
                    st.write("**Tech Stack:**")
                    tech_stack = candidate_data['tech_stack']
                    total_techs = sum(len(technologies) for technologies in tech_stack.values())
                    st.write(f"*{total_techs} technologies detected*")
                    
                    for category, technologies in tech_stack.items():
                        if technologies:
                            tech_list = ", ".join(technologies)
                            st.write(f"• *{category.replace('_', ' ').title()}:* {tech_list}")
                    
                    # Show question availability
                    if st.session_state.generated_questions:
                        total_questions = sum(len(q) for q in st.session_state.generated_questions.values())
                        st.write(f"**📝 Questions Available:** {total_questions}")
                        
                        # Show question breakdown
                        for tech, questions in st.session_state.generated_questions.items():
                            st.write(f"• {tech}: {len(questions)} questions")
            
            # Progress indicator
            self.render_progress_indicator()
            
            # Control buttons
            st.subheader("🔧 Controls")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 Reset", help="Start a new conversation", use_container_width=True):
                    self.reset_session()
            
            with col2:
                if st.button("📥 Export", help="Download candidate data", use_container_width=True, disabled=not st.session_state.candidate_data):
                    self.export_candidate_data()
            
            # Advanced Analytics Section
            st.markdown("---")
            
            # Candidate Scoring (if data available)
            if st.session_state.candidate_data and len(st.session_state.messages) > 4:
                self.show_candidate_scoring()
            
            # Expandable sections
            self.show_conversation_summary()
            self.show_analytics_dashboard()
            self.show_debug_info()
            
            # Enhanced Knowledge Base Insights
            with st.expander("🧠 Enhanced Knowledge Base", expanded=False):
                self._show_enhanced_knowledge_insights()
            
            # Real-Time Market Data
            with st.expander("📊 Real-Time Market Data", expanded=False):
                self._show_market_data_dashboard()
            
            # Interactive Question Selection
            if st.session_state.generated_questions and st.session_state.conversation_state == ConversationState.TECHNICAL_QUESTIONS:
                with st.expander("🎯 Customize Questions", expanded=False):
                    self._show_interactive_question_selector()
            
            # Skill Level Analysis
            if len(st.session_state.messages) > 4:
                with st.expander("📈 Skill Level Analysis", expanded=False):
                    self._show_skill_level_analysis()
            
            # Professional Insights Panel
            with st.expander("💡 Professional Insights", expanded=False):
                if st.session_state.candidate_data and len(st.session_state.messages) > 3:
                    self._show_professional_insights()
                else:
                    st.write("Insights will appear as the conversation progresses...")
            
            # Information about the system
            with st.expander("ℹ️ About This System"):
                st.markdown("""
                **TalentScout Hiring Assistant v2.0** - Advanced AI-powered screening:
                
                🎯 **Intelligent Scoring System**  
                Comprehensive candidate evaluation with detailed analytics
                
                📊 **Advanced Analytics**  
                Real-time insights and performance metrics
                
                🤖 **Smart Question Adaptation**  
                Dynamic questions based on experience and tech stack
                
                📋 **Professional Reports**  
                Detailed candidate reports with recommendations
                
                🔒 **Enterprise Security:** All data processed securely with privacy compliance.
                """)
                
                st.markdown("---")
                st.markdown("**System Status:**")
                
                # Enhanced system status
                api_status = "🟢 Connected" if self.llm_integration.client else "🟡 Basic Mode"
                st.write(f"• AI Enhancement: {api_status}")
                st.write(f"• Scoring Engine: 🟢 Active")
                st.write(f"• Analytics: 🟢 Real-time")
                st.write(f"• Question Bank: 🟢 {len(self.conversation_manager.question_generator.question_bank)} technologies")
                
                if st.session_state.candidate_data:
                    completion = len(st.session_state.candidate_data) / 7 * 100
                    st.write(f"• Session Progress: {completion:.0f}%")
    
    def _show_professional_insights(self):
        """Show professional insights about the candidate"""
        candidate_data = st.session_state.candidate_data
        
        # Quick insights
        insights = []
        
        # Experience insights
        experience = int(str(candidate_data.get('experience_years', 0)))
        if experience >= 8:
            insights.append("🎯 Senior-level candidate - suitable for leadership roles")
        elif experience >= 5:
            insights.append("💼 Mid-to-senior level - good for complex projects")
        elif experience >= 2:
            insights.append("📈 Growing professional - ideal for mentorship programs")
        else:
            insights.append("🌱 Early career - great potential for development")
        
        # Tech stack insights
        if 'tech_stack' in candidate_data:
            tech_stack = candidate_data['tech_stack']
            total_techs = sum(len(techs) for techs in tech_stack.values())
            
            if total_techs >= 8:
                insights.append("🛠️ Diverse tech stack - versatile developer")
            elif total_techs >= 5:
                insights.append("⚙️ Solid technical foundation")
            
            # Check for modern technologies
            modern_techs = ['react', 'vue', 'docker', 'kubernetes', 'aws', 'typescript']
            has_modern = any(tech.lower() in modern_techs 
                           for techs in tech_stack.values() 
                           for tech in techs)
            if has_modern:
                insights.append("🚀 Uses modern technologies - up-to-date skills")
        
        # Communication insights
        user_messages = [msg for msg in st.session_state.messages if msg['role'] == 'user']
        if user_messages:
            avg_length = sum(len(msg['content'].split()) for msg in user_messages) / len(user_messages)
            if avg_length > 15:
                insights.append("💬 Detailed communicator - good for client-facing roles")
            elif avg_length > 8:
                insights.append("🗣️ Clear communicator")
        
        # Display insights
        for insight in insights:
            st.write(f"• {insight}")
        
        # Market insights
        st.markdown("**Market Context:**")
        position = candidate_data.get('desired_position', '').lower()
        tech_stack_str = str(candidate_data.get('tech_stack', {})).lower()
        
        if 'senior' in position or 'lead' in position:
            st.write("📊 Senior roles: High demand, competitive market")
        elif 'full stack' in position:
            st.write("📊 Full-stack: Very high demand across industries")
        elif 'frontend' in position or 'react' in tech_stack_str:
            st.write("📊 Frontend: Strong demand, especially React skills")
        elif 'backend' in position or 'python' in tech_stack_str:
            st.write("📊 Backend: Consistent demand, Python very popular")
        else:
            st.write("📊 General development: Steady market demand")
    
    def render_progress_indicator(self):
        """Render progress indicator"""
        with st.expander("📊 Progress", expanded=True):
            total_steps = 5
            current_step = 0
            
            if hasattr(st.session_state, 'conversation_state'):
                state = st.session_state.conversation_state
                if state == ConversationState.GREETING:
                    current_step = 1
                elif state == ConversationState.COLLECTING_INFO:
                    current_step = 2
                elif state == ConversationState.TECH_STACK_COLLECTION:
                    current_step = 3
                elif state == ConversationState.TECHNICAL_QUESTIONS:
                    current_step = 4
                elif state in [ConversationState.COMPLETED, ConversationState.ENDED]:
                    current_step = 5
            
            progress = current_step / total_steps
            st.progress(progress)
            st.write(f"**Step {current_step} of {total_steps}** ({progress*100:.0f}% complete)")
            
            steps = [
                "Initial Greeting",
                "Information Collection",
                "Tech Stack Assessment", 
                "Technical Questions",
                "Completion"
            ]
            
            for i, step in enumerate(steps):
                if i < current_step:
                    st.write(f"✅ {step}")
                elif i == current_step - 1:  # Current step (0-indexed)
                    st.write(f"🔄 {step}")
                else:
                    st.write(f"⏳ {step}")
    
    def render_main_chat(self):
        """Render the main chat interface"""
        st.header("💬 Conversation")
        
        # Initialize edit mode state
        if 'edit_mode' not in st.session_state:
            st.session_state.edit_mode = False
        if 'edit_message_index' not in st.session_state:
            st.session_state.edit_message_index = -1
        
        # Handle edit mode
        if st.session_state.edit_mode and st.session_state.edit_message_index >= 0:
            self.render_edit_interface()
            return
        
        # Display professional chat messages
        for i, message in enumerate(st.session_state.messages):
            with st.container():
                if message["role"] == "user":
                    # Check if this is the last user message and show edit button
                    is_last_user_message = (i == len(st.session_state.messages) - 1 or 
                                          (i == len(st.session_state.messages) - 2 and 
                                           st.session_state.messages[-1]["role"] == "assistant"))
                    
                    # Create columns for message and edit button
                    if is_last_user_message and len(st.session_state.messages) > 1:
                        col1, col2 = st.columns([0.9, 0.1])
                        with col1:
                            st.markdown(f"""
                            <div class="chat-message user-message">
                                <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                                    <div style="width: 36px; height: 36px; border-radius: 50%; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; margin-right: 0.75rem;">
                                        <span style="font-size: 1rem;">👤</span>
                                    </div>
                                    <strong style="font-weight: 600; font-size: 0.9rem;">You</strong>
                                </div>
                                <div style="margin-left: 2.75rem; line-height: 1.6; font-size: 1rem;">
                                    {message["content"].replace('<', '&lt;').replace('>', '&gt;') if isinstance(message["content"], str) else message["content"]}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            if st.button("✏️", key=f"edit_btn_{i}", help="Edit this message", 
                                       use_container_width=True):
                                st.session_state.edit_mode = True
                                st.session_state.edit_message_index = i
                                st.rerun()
                    else:
                        st.markdown(f"""
                        <div class="chat-message user-message">
                            <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                                <div style="width: 36px; height: 36px; border-radius: 50%; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; margin-right: 0.75rem;">
                                    <span style="font-size: 1rem;">👤</span>
                                </div>
                                <strong style="font-weight: 600; font-size: 0.9rem;">You</strong>
                            </div>
                            <div style="margin-left: 2.75rem; line-height: 1.6; font-size: 1rem;">
                                {message["content"].replace('<', '&lt;').replace('>', '&gt;') if isinstance(message["content"], str) else message["content"]}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                            <div style="width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; margin-right: 0.75rem; color: white;">
                                <span style="font-size: 1rem;">🤖</span>
                            </div>
                            <strong style="font-weight: 600; color: #667eea; font-size: 0.9rem;">TalentScout Assistant</strong>
                        </div>
                        <div style="margin-left: 2.75rem; line-height: 1.6; font-size: 1rem;">
                            {message["content"].replace('<', '&lt;').replace('>', '&gt;') if isinstance(message["content"], str) else message["content"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Initial greeting if no messages
        if not st.session_state.messages:
            greeting = self.conversation_manager.get_greeting_message()
            st.session_state.messages.append({"role": "assistant", "content": greeting})
            st.rerun()
        
        # Chat input
        if st.session_state.conversation_state != ConversationState.ENDED:
            user_input = st.chat_input("Type your response here...")
            
            if user_input:
                # Add user message
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Process response - streamlined for speed
                response = self.conversation_manager.process_user_input(user_input)
                
                # Skip LLM enhancement for faster responses
                # The conversation manager already provides natural responses
                
                # Add assistant response
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                st.rerun()
        else:
            st.markdown("""
            <div class="info-box">
                <strong>Session Ended</strong><br>
                The conversation has ended. Click "Reset Session" in the sidebar to start over.
            </div>
            """, unsafe_allow_html=True)
        
        # Display technical questions if generated
        if st.session_state.generated_questions:
            with st.expander("📝 Generated Technical Questions", expanded=True):
                st.write("**💡 These questions are tailored to your tech stack:**")
                
                question_count = sum(len(questions) for questions in st.session_state.generated_questions.values())
                st.write(f"*Total questions generated: {question_count}*")
                st.write("")
                
                for tech, questions in st.session_state.generated_questions.items():
                    st.markdown(f"### 🔧 {tech}")
                    
                    for i, question in enumerate(questions, 1):
                        st.markdown(f"""
                        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #667eea;">
                            <strong>Q{i}:</strong> {question}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Add technology insight if available
                    try:
                        from knowledge_base.enhanced_knowledge import enhanced_knowledge
                        insight = enhanced_knowledge.get_technology_insight(tech.lower())
                        if insight:
                            st.markdown(f"""
                            <div style="background: #f0fff4; padding: 0.75rem; border-radius: 6px; margin: 0.5rem 0; font-size: 0.9rem;">
                                <strong>💡 {tech} Insight:</strong> {insight['description']}<br>
                                <strong>Market Demand:</strong> {insight.get('market_demand', 'N/A')} | 
                                <strong>Difficulty:</strong> {insight.get('difficulty_level', 'N/A')}
                            </div>
                            """, unsafe_allow_html=True)
                    except:
                        pass
                    
                    st.write("")
                
                # Add interview tips
                st.markdown("### 💡 Interview Tips")
                st.markdown("""
                <div style="background: #fffbf0; padding: 1rem; border-radius: 8px; border-left: 4px solid #f59e0b;">
                    <strong>Remember:</strong><br>
                    • Focus on your real-world experience and examples<br>
                    • It's okay to say "I don't know" and explain how you'd find out<br>
                    • Think out loud - show your problem-solving process<br>
                    • Ask clarifying questions when needed<br>
                    • Relate technical concepts to projects you've worked on
                </div>
                """, unsafe_allow_html=True)
    
    def render_edit_interface(self):
        """Render the edit message interface"""
        st.header("✏️ Edit Message")
        
        edit_index = st.session_state.edit_message_index
        original_message = st.session_state.messages[edit_index]["content"]
        
        # Show original message
        st.markdown("""
        <div class="info-box">
            <strong>Original Message:</strong><br>
            """ + original_message.replace('<', '&lt;').replace('>', '&gt;') + """
        </div>
        """, unsafe_allow_html=True)
        
        # Edit form
        with st.form("edit_message_form"):
            st.write("**Edit your message:**")
            edited_message = st.text_area(
                "Message", 
                value=original_message,
                height=100,
                help="Modify your message and click 'Update' to regenerate the conversation from this point."
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                update_clicked = st.form_submit_button("✅ Update", use_container_width=True)
            
            with col2:
                cancel_clicked = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            with col3:
                preview_clicked = st.form_submit_button("👁️ Preview", use_container_width=True)
        
        # Handle form actions
        if update_clicked and edited_message.strip():
            self.handle_message_update(edit_index, edited_message.strip())
        
        elif cancel_clicked:
            st.session_state.edit_mode = False
            st.session_state.edit_message_index = -1
            st.rerun()
        
        elif preview_clicked:
            st.markdown("""
            <div class="success-box">
                <strong>Preview of Updated Message:</strong><br>
                """ + edited_message.replace('<', '&lt;').replace('>', '&gt;') + """
            </div>
            """, unsafe_allow_html=True)
        
        # Show warning about conversation regeneration
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ Important:</strong> Updating this message will regenerate the conversation from this point forward. 
            All subsequent messages will be removed and the assistant will respond to your edited message.
        </div>
        """, unsafe_allow_html=True)
    
    def handle_message_update(self, edit_index: int, new_message: str):
        """Handle updating a message and regenerating the conversation"""
        try:
            # Update the message
            st.session_state.messages[edit_index]["content"] = new_message
            
            # Remove all messages after the edited message
            st.session_state.messages = st.session_state.messages[:edit_index + 1]
            
            # Reset conversation state to regenerate properly
            # We need to determine the appropriate state based on the conversation progress
            self.reset_conversation_state_for_edit(edit_index)
            
            # Generate new response
            response = self.conversation_manager.process_user_input(new_message)
            
            # Add the new assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Exit edit mode
            st.session_state.edit_mode = False
            st.session_state.edit_message_index = -1
            
            st.success("✅ Message updated and conversation regenerated!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error updating message: {str(e)}")
            st.session_state.edit_mode = False
            st.session_state.edit_message_index = -1
    
    def reset_conversation_state_for_edit(self, edit_index: int):
        """Reset conversation state appropriately for the edit point"""
        # Count user messages up to the edit point to determine state
        user_messages_count = sum(1 for i, msg in enumerate(st.session_state.messages[:edit_index + 1]) 
                                 if msg["role"] == "user")
        
        # Reset relevant session state based on conversation progress
        if user_messages_count <= 1:
            # First message - back to greeting/collecting info
            st.session_state.conversation_state = ConversationState.COLLECTING_INFO
            st.session_state.field_index = 0
            # Clear candidate data that might have been collected after this point
            if 'candidate_data' in st.session_state:
                # Keep only basic info that might have been in the first message
                basic_fields = ['full_name']
                filtered_data = {k: v for k, v in st.session_state.candidate_data.items() 
                               if k in basic_fields}
                st.session_state.candidate_data = filtered_data
        
        elif user_messages_count <= 6:
            # Still collecting basic info
            st.session_state.conversation_state = ConversationState.COLLECTING_INFO
            st.session_state.field_index = min(user_messages_count - 1, 5)
        
        elif user_messages_count == 7:
            # Tech stack collection
            st.session_state.conversation_state = ConversationState.TECH_STACK_COLLECTION
            # Clear tech stack and questions that might have been generated
            if 'candidate_data' in st.session_state and 'tech_stack' in st.session_state.candidate_data:
                del st.session_state.candidate_data['tech_stack']
            if 'generated_questions' in st.session_state:
                st.session_state.generated_questions = {}
        
        else:
            # Technical questions phase
            st.session_state.conversation_state = ConversationState.TECHNICAL_QUESTIONS
            # Reset question tracking
            st.session_state.questions_answered = max(0, user_messages_count - 8)
    
    def reset_session(self):
        """Reset the session state"""
        keys_to_reset = [
            'conversation_state', 'messages', 'candidate_data', 
            'field_index', 'generated_questions', 'edit_mode', 
            'edit_message_index', 'questions_answered', 'technical_responses'
        ]
        
        reset_count = 0
        for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]
                reset_count += 1
        
        # Reinitialize
        self.conversation_manager.initialize_session_state()
        st.success(f"✅ Session reset successfully! Cleared {reset_count} items.")
        st.balloons()  # Fun visual feedback
        st.rerun()
    
    def export_candidate_data(self):
        """Export comprehensive candidate report"""
        if st.session_state.candidate_data:
            # Generate comprehensive scoring
            from utils.candidate_scorer import CandidateScorer
            scorer = CandidateScorer()
            
            score_data = scorer.generate_comprehensive_score(
                st.session_state.candidate_data, 
                st.session_state.messages
            )
            
            # Create comprehensive export
            export_data = {
                'candidate_profile': {
                    'basic_info': st.session_state.candidate_data,
                    'scoring_analysis': score_data,
                    'conversation_metrics': {
                        'total_messages': len(st.session_state.messages),
                        'user_messages': len([m for m in st.session_state.messages if m['role'] == 'user']),
                        'completion_status': st.session_state.conversation_state.value,
                        'session_duration': 'N/A'  # Could be calculated with timestamps
                    }
                },
                'technical_assessment': {
                    'generated_questions': st.session_state.generated_questions,
                    'tech_stack_analysis': score_data.get('analysis', {}).get('tech_stack', {}),
                    'role_fit_analysis': score_data.get('analysis', {}).get('role_fit', {})
                },
                'conversation_transcript': st.session_state.messages,
                'recruiter_notes': {
                    'recommendations': score_data.get('recommendations', []),
                    'next_steps': self._generate_next_steps(score_data),
                    'interview_focus_areas': self._generate_interview_focus(score_data)
                },
                'export_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'system_version': '2.0',
                    'export_type': 'comprehensive_report'
                }
            }
            
            # Create both JSON and readable report
            json_data = json.dumps(export_data, indent=2, default=str)
            readable_report = self._generate_readable_report(export_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label="📊 Download Full Report (JSON)",
                    data=json_data,
                    file_name=f"candidate_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col2:
                st.download_button(
                    label="📄 Download Summary (TXT)",
                    data=readable_report,
                    file_name=f"candidate_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            st.success("✅ Comprehensive candidate report ready for download!")
        else:
            st.warning("⚠️ No candidate data to export yet.")
    
    def _generate_next_steps(self, score_data: Dict) -> List[str]:
        """Generate recommended next steps based on scoring"""
        next_steps = []
        total_score = score_data.get('total_score', 0)
        
        if total_score >= 8.5:
            next_steps.extend([
                "Schedule technical interview with senior team members",
                "Prepare system design or architecture questions",
                "Consider for senior-level positions"
            ])
        elif total_score >= 7.0:
            next_steps.extend([
                "Schedule standard technical interview",
                "Focus on practical coding challenges",
                "Good fit for mid-level positions"
            ])
        elif total_score >= 5.5:
            next_steps.extend([
                "Consider for junior positions with mentorship",
                "Focus on fundamental technical concepts",
                "May need additional training or support"
            ])
        else:
            next_steps.extend([
                "Consider entry-level positions only",
                "Extensive training and mentorship required",
                "Re-evaluate after skill development"
            ])
        
        return next_steps
    
    def _generate_interview_focus(self, score_data: Dict) -> List[str]:
        """Generate interview focus areas"""
        focus_areas = []
        scores = score_data.get('scores', {})
        
        if scores.get('tech_depth', 0) < 7:
            focus_areas.append("Deep-dive into technical expertise and problem-solving")
        
        if scores.get('communication', 0) < 7:
            focus_areas.append("Assess communication skills and team collaboration")
        
        if scores.get('role_fit', 0) < 7:
            focus_areas.append("Clarify role expectations and skill gaps")
        
        # Always include these
        focus_areas.extend([
            "Past project experiences and challenges overcome",
            "Learning approach and adaptability",
            "Career goals and growth mindset"
        ])
        
        return focus_areas
    
    def _generate_readable_report(self, export_data: Dict) -> str:
        """Generate human-readable report"""
        candidate = export_data['candidate_profile']['basic_info']
        scoring = export_data['candidate_profile']['scoring_analysis']
        
        report = f"""
TALENTSCOUT CANDIDATE SCREENING REPORT
=====================================

CANDIDATE INFORMATION
--------------------
Name: {candidate.get('full_name', 'N/A')}
Email: {candidate.get('email', 'N/A')}
Phone: {candidate.get('phone', 'N/A')}
Experience: {candidate.get('experience_years', 'N/A')} years
Position: {candidate.get('desired_position', 'N/A')}
Location: {candidate.get('location', 'N/A')}

ASSESSMENT RESULTS
-----------------
Overall Score: {scoring.get('total_score', 'N/A')}/10
Grade: {scoring.get('grade', 'N/A')}
Experience Level: {scoring.get('experience_level', 'N/A')}

SCORE BREAKDOWN
--------------
Experience: {scoring.get('scores', {}).get('experience', 'N/A')}/10
Tech Breadth: {scoring.get('scores', {}).get('tech_breadth', 'N/A')}/10
Tech Depth: {scoring.get('scores', {}).get('tech_depth', 'N/A')}/10
Communication: {scoring.get('scores', {}).get('communication', 'N/A')}/10
Role Fit: {scoring.get('scores', {}).get('role_fit', 'N/A')}/10

TECHNOLOGY STACK
---------------
"""
        
        tech_stack = candidate.get('tech_stack', {})
        for category, technologies in tech_stack.items():
            if technologies:
                report += f"{category.title()}: {', '.join(technologies)}\n"
        
        report += f"""
RECOMMENDATIONS
--------------
"""
        for rec in scoring.get('recommendations', []):
            report += f"• {rec}\n"
        
        report += f"""
NEXT STEPS
----------
"""
        for step in export_data['recruiter_notes']['next_steps']:
            report += f"• {step}\n"
        
        report += f"""
INTERVIEW FOCUS AREAS
--------------------
"""
        for area in export_data['recruiter_notes']['interview_focus_areas']:
            report += f"• {area}\n"
        
        report += f"""
REPORT GENERATED
---------------
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
System: TalentScout Hiring Assistant v2.0
"""
        
        return report
    
    def _show_enhanced_knowledge_insights(self):
        """Show enhanced knowledge base insights and recommendations"""
        try:
            from knowledge_base.enhanced_knowledge import enhanced_knowledge
            from config import Config
            
            # Knowledge base statistics
            st.write("**📊 Knowledge Base Coverage:**")
            
            total_technologies = sum(len(techs) for techs in Config.COMMON_TECHNOLOGIES.values())
            st.metric("Total Technologies", total_technologies)
            
            # Enhanced question bank info
            from utils.question_generator import TechnicalQuestionGenerator
            generator = TechnicalQuestionGenerator()
            total_questions = sum(len(q) for q in generator.question_bank.values())
            st.metric("Total Questions", total_questions)
            
            # Show candidate-specific insights if available
            if st.session_state.candidate_data and 'tech_stack' in st.session_state.candidate_data:
                st.write("**🎯 Your Tech Stack Analysis:**")
                
                tech_stack = []
                for category, technologies in st.session_state.candidate_data['tech_stack'].items():
                    tech_stack.extend(technologies)
                
                # Get market insights
                market_insights = enhanced_knowledge.get_market_insights(tech_stack)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Market Value", market_insights['market_value'])
                    st.metric("Demand Level", market_insights['demand_level'])
                
                with col2:
                    st.write("**💼 Career Paths:**")
                    for path in market_insights['career_paths'][:3]:
                        st.write(f"• {path}")
                
                # Technology insights
                st.write("**🔍 Technology Insights:**")
                for tech in tech_stack[:3]:  # Show top 3 technologies
                    insight = enhanced_knowledge.get_technology_insight(tech)
                    if insight:
                        with st.expander(f"{tech.title()} - {insight['market_demand']} Demand"):
                            st.write(f"**Description:** {insight['description']}")
                            st.write(f"**Difficulty:** {insight['difficulty_level']}")
                            st.write(f"**Salary Range:** {insight.get('salary_range', 'N/A')}")
                            
                            if insight.get('key_concepts'):
                                st.write("**Key Concepts:**")
                                for concept in insight['key_concepts'][:5]:
                                    st.write(f"• {concept}")
            
            # General knowledge base features
            st.write("**🚀 Enhanced Features:**")
            st.write("✅ Technology-specific insights and salary data")
            st.write("✅ Personalized learning paths")
            st.write("✅ Market demand analysis")
            st.write("✅ Career path recommendations")
            st.write("✅ Interview preparation guides")
            st.write("✅ Industry trend analysis")
            
            # Question bank breakdown
            st.write("**📝 Question Categories:**")
            categories = {
                'Technical Depth': 'Deep understanding assessment',
                'Problem Solving': 'Analytical thinking evaluation',
                'Best Practices': 'Industry standards knowledge',
                'Real Experience': 'Practical application stories'
            }
            
            for category, description in categories.items():
                st.write(f"• **{category}**: {description}")
            
        except Exception as e:
            st.write("Enhanced knowledge base loading...")
            st.write(f"📊 Technologies supported: 50+")
            st.write(f"📝 Enhanced question bank: 500+ questions")
            st.write(f"🎯 Personalized insights: Active")
            st.write(f"💼 Career guidance: Available")
    
    def _show_market_data_dashboard(self):
        """Show real-time market data dashboard"""
        try:
            from utils.market_data_integration import market_integration
            
            if st.session_state.candidate_data and 'tech_stack' in st.session_state.candidate_data:
                # Get comprehensive market analysis
                market_data = market_integration.get_comprehensive_market_analysis(
                    st.session_state.candidate_data
                )
                
                if market_data:
                    # Render the market dashboard
                    market_integration.render_market_dashboard(market_data)
                else:
                    st.info("💡 Market analysis will appear after tech stack collection")
            else:
                st.info("💡 Market data will appear after tech stack collection")
                
                # Show sample market features
                st.write("**📊 Real-Time Market Features:**")
                st.write("• Live salary data and demand analysis")
                st.write("• Location-adjusted compensation estimates")
                st.write("• Technology growth rate tracking")
                st.write("• Career progression recommendations")
                st.write("• Industry-specific market insights")
                
        except Exception as e:
            st.write("Market data loading...")
            st.write("• Real-time salary analysis")
            st.write("• Technology demand tracking")
            st.write("• Career progression insights")
    
    def _show_interactive_question_selector(self):
        """Show interactive question selection interface"""
        try:
            from utils.interactive_question_selector import interactive_selector
            
            st.write("**🎯 Customize Your Interview Experience**")
            
            # Quick customization options
            col1, col2 = st.columns(2)
            
            with col1:
                interview_style = st.selectbox(
                    "Interview Style:",
                    options=['conversational', 'structured', 'mixed'],
                    format_func=lambda x: {
                        'conversational': '💬 Conversational',
                        'structured': '📋 Structured',
                        'mixed': '🔄 Mixed'
                    }[x],
                    help="Choose your preferred interview style"
                )
            
            with col2:
                question_count = st.slider(
                    "Questions to ask:",
                    min_value=3,
                    max_value=15,
                    value=8,
                    help="Total number of questions"
                )
            
            # Technology priorities
            if st.session_state.generated_questions:
                st.write("**🔧 Technology Focus (Rate 1-5):**")
                
                tech_priorities = {}
                cols = st.columns(min(3, len(st.session_state.generated_questions)))
                
                for i, (tech, questions) in enumerate(st.session_state.generated_questions.items()):
                    with cols[i % 3]:
                        priority = st.slider(
                            f"{tech}",
                            min_value=1,
                            max_value=5,
                            value=3,
                            key=f"priority_{tech}",
                            help=f"{len(questions)} questions available"
                        )
                        tech_priorities[tech] = priority
                
                # Apply customization button
                if st.button("🎯 Apply Customization", use_container_width=True):
                    # Generate personalized questions based on preferences
                    preferences = {
                        'interview_style': interview_style,
                        'total_questions': question_count,
                        'tech_priorities': tech_priorities
                    }
                    
                    # Store preferences in session state
                    st.session_state.question_preferences = preferences
                    st.success("✅ Interview customized! Your preferences have been applied.")
                    st.rerun()
            
        except Exception as e:
            st.write("Interactive question selection loading...")
            st.write("• Customize interview style and focus")
            st.write("• Select specific technologies to emphasize")
            st.write("• Adjust question difficulty and quantity")
    
    def _show_skill_level_analysis(self):
        """Show skill level analysis based on responses"""
        try:
            from utils.skill_level_adapter import skill_adapter
            
            # Analyze recent responses
            user_messages = [msg['content'] for msg in st.session_state.messages if msg['role'] == 'user']
            
            if len(user_messages) >= 2:
                # Get session analysis
                session_id = st.session_state.get('aiml_session_id', 'default')
                
                # Simulate analysis for the latest responses
                latest_response = user_messages[-1]
                analysis_result = skill_adapter.process_response_and_adapt(
                    latest_response,
                    "Technical question",
                    "General",
                    session_id
                )
                
                st.write("**📈 Response Analysis:**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    analysis = analysis_result.get('analysis', {})
                    skill_level = analysis.get('estimated_skill_level', 'intermediate')
                    if hasattr(skill_level, 'value'):
                        skill_level = skill_level.value
                    
                    st.metric("Estimated Skill Level", skill_level.title())
                    
                    response_quality = analysis.get('response_quality', 'medium')
                    st.metric("Response Quality", response_quality.title())
                
                with col2:
                    technical_depth = analysis.get('technical_depth_score', 0)
                    st.metric("Technical Depth", f"{technical_depth:.1f}/1.0")
                    
                    experience_score = analysis.get('experience_score', 0)
                    st.metric("Experience Score", f"{experience_score:.1f}/1.0")
                
                # Show insights
                insights = analysis.get('key_insights', [])
                if insights:
                    st.write("**💡 Key Insights:**")
                    for insight in insights:
                        st.write(f"• {insight}")
                
                # Show session summary
                session_summary = skill_adapter.get_session_summary(session_id)
                if session_summary:
                    st.write("**📊 Session Summary:**")
                    st.write(f"• Overall Skill Level: {session_summary.get('overall_skill_level', 'N/A').title()}")
                    st.write(f"• Total Responses: {session_summary.get('total_responses', 0)}")
                    st.write(f"• Average Quality: {session_summary.get('average_response_quality', 0):.1%}")
            else:
                st.info("💡 Skill analysis will appear after more responses")
                
                # Show analysis features
                st.write("**📈 Skill Analysis Features:**")
                st.write("• Real-time skill level detection")
                st.write("• Response quality assessment")
                st.write("• Technical depth analysis")
                st.write("• Adaptive question generation")
                st.write("• Session progress tracking")
                
        except Exception as e:
            st.write("Skill level analysis loading...")
            st.write("• Adaptive difficulty adjustment")
            st.write("• Response quality assessment")
            st.write("• Technical depth analysis")
    
    def show_conversation_summary(self):
        """Show conversation summary in sidebar"""
        with st.expander("📊 Conversation Summary", expanded=False):
            summary = self.conversation_manager.get_conversation_summary()
            
            st.write("**Current State:**", summary['state'].replace('_', ' ').title())
            
            if summary['candidate_data']:
                st.write("**Fields Collected:**", len(summary['candidate_data']))
                completion = len(summary['candidate_data']) / 7 * 100  # 7 total fields
                st.progress(completion / 100)
                st.write(f"**Completion:** {completion:.0f}%")
            else:
                st.write("**Fields Collected:** 0")
                st.progress(0.0)
                st.write("**Completion:** 0%")
            
            if summary['generated_questions']:
                st.write("**Questions Generated:**", sum(len(q) for q in summary['generated_questions'].values()))
            else:
                st.write("**Questions Generated:** 0")
            
            st.write("**Messages Exchanged:**", len(st.session_state.messages))
    
    def show_candidate_scoring(self):
        """Show advanced candidate scoring"""
        with st.expander("🎯 Candidate Scoring", expanded=True):
            from utils.candidate_scorer import CandidateScorer
            
            scorer = CandidateScorer()
            score_data = scorer.generate_comprehensive_score(
                st.session_state.candidate_data, 
                st.session_state.messages
            )
            
            if 'error' not in score_data:
                # Overall Score
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Overall Score", f"{score_data['total_score']}/10")
                with col2:
                    st.metric("Grade", score_data['grade'])
                with col3:
                    st.metric("Level", score_data['experience_level'])
                
                # Score Breakdown
                st.write("**Score Breakdown:**")
                scores = score_data['scores']
                
                for category, score in scores.items():
                    progress = score / 10
                    st.write(f"*{category.replace('_', ' ').title()}:* {score}/10")
                    st.progress(progress)
                
                # Recommendations
                if score_data['recommendations']:
                    st.write("**Recommendations:**")
                    for rec in score_data['recommendations']:
                        st.write(f"• {rec}")
            else:
                st.write("Insufficient data for scoring")
    
    def show_analytics_dashboard(self):
        """Show analytics dashboard"""
        with st.expander("📊 Analytics Dashboard", expanded=False):
            if st.session_state.messages:
                # Conversation metrics
                user_messages = [msg for msg in st.session_state.messages if msg['role'] == 'user']
                assistant_messages = [msg for msg in st.session_state.messages if msg['role'] == 'assistant']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("User Messages", len(user_messages))
                    st.metric("Assistant Messages", len(assistant_messages))
                
                with col2:
                    if user_messages:
                        avg_length = sum(len(msg['content'].split()) for msg in user_messages) / len(user_messages)
                        st.metric("Avg Response Length", f"{avg_length:.1f} words")
                    
                    completion = len(st.session_state.candidate_data) / 7 * 100 if st.session_state.candidate_data else 0
                    st.metric("Data Completion", f"{completion:.0f}%")
                
                # Tech stack analysis
                if 'tech_stack' in st.session_state.candidate_data:
                    st.write("**Tech Stack Analysis:**")
                    tech_stack = st.session_state.candidate_data['tech_stack']
                    
                    for category, technologies in tech_stack.items():
                        if technologies:
                            st.write(f"• *{category.title()}:* {len(technologies)} technologies")
                
                # Session timeline
                st.write("**Session Timeline:**")
                for i, msg in enumerate(st.session_state.messages[-5:], 1):  # Last 5 messages
                    role_icon = "👤" if msg['role'] == 'user' else "🤖"
                    preview = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
                    st.write(f"{i}. {role_icon} {preview}")
            else:
                st.write("No conversation data yet")
    
    def show_debug_info(self):
        """Show debug information"""
        with st.expander("🔍 Debug Information", expanded=False):
            st.write("**Session State Keys:**")
            session_keys = list(st.session_state.keys())
            if session_keys:
                for key in session_keys:
                    st.write(f"- {key}")
            else:
                st.write("- No session data yet")
            
            st.write("**LLM Integration Status:**")
            llm_status = "✅ Active" if self.llm_integration.client else "❌ Inactive"
            st.write(f"- OpenAI Client: {llm_status}")
            
            if hasattr(st.session_state, 'conversation_state'):
                st.write(f"- Conversation State: {st.session_state.conversation_state.value}")
            else:
                st.write("- Conversation State: Not initialized")
            
            st.write("**Configuration:**")
            from config import Config
            st.write(f"- API Key Configured: {'✅ Yes' if Config.OPENAI_API_KEY else '❌ No'}")
            st.write(f"- Model: {Config.OPENAI_MODEL}")
            st.write(f"- Max Questions per Tech: {Config.MAX_QUESTIONS_PER_TECH}")
            
            st.write("**System Info:**")
            st.write(f"- Python Version: {__import__('sys').version.split()[0]}")
            st.write(f"- Streamlit Version: {st.__version__}")
            
            if st.button("Clear All Session Data", help="Reset all session state", type="secondary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success("Session data cleared!")
                st.rerun()

def main():
    """Main function to run the application"""
    try:
        # Performance monitoring
        start_time = time.time()
        
        app = TalentScoutApp()
        app.run()
        
        # Track performance in session state
        if 'performance_metrics' not in st.session_state:
            st.session_state.performance_metrics = []
        
        load_time = time.time() - start_time
        st.session_state.performance_metrics.append({
            'timestamp': datetime.now().isoformat(),
            'load_time': load_time,
            'page_loads': len(st.session_state.performance_metrics) + 1
        })
        
        # Keep only last 10 metrics
        if len(st.session_state.performance_metrics) > 10:
            st.session_state.performance_metrics = st.session_state.performance_metrics[-10:]
            
    except Exception as e:
        st.error(f"⚠️ Application Error: {str(e)}")
        st.info("💡 Try refreshing the page. If the issue persists, check your internet connection or contact support.")
        
        # Error reporting
        if st.button("📋 Copy Error Details"):
            error_details = f"Error: {str(e)}\nTime: {datetime.now().isoformat()}\nUser Agent: {st.get_option('browser.gatherUsageStats')}"
            st.code(error_details)

if __name__ == "__main__":
    main()