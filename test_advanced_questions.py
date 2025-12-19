#!/usr/bin/env python3
"""
Test script for advanced questions feature
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot.aiml_conversation_manager import AIMLConversationManager
from utils.question_generator import TechnicalQuestionGenerator

def test_advanced_questions():
    """Test the advanced questions functionality"""
    print("🧪 Testing Advanced Questions Feature")
    print("=" * 50)
    
    # Initialize components
    conversation_manager = AIMLConversationManager()
    question_generator = TechnicalQuestionGenerator()
    
    # Test tech stack
    test_tech_stack = {
        'languages': ['python', 'javascript'],
        'frameworks': ['react', 'django'],
        'databases': ['postgresql', 'redis'],
        'devops_tools': ['docker', 'aws']
    }
    
    print("📋 Test Tech Stack:")
    for category, technologies in test_tech_stack.items():
        print(f"  {category}: {', '.join(technologies)}")
    
    print("\n🎯 Generated Questions:")
    print("-" * 30)
    
    # Generate questions
    questions = question_generator.generate_questions(test_tech_stack, 3)
    
    question_count = 0
    for tech, tech_questions in questions.items():
        print(f"\n🔧 {tech.upper()}:")
        for i, question in enumerate(tech_questions, 1):
            question_count += 1
            print(f"  Q{question_count}: {question}")
    
    print(f"\n📊 Total Questions Generated: {question_count}")
    
    # Test advanced question selection
    print("\n🚀 Testing Advanced Question Selection:")
    print("-" * 40)
    
    # Simulate different skill levels
    skill_levels = ['beginner', 'intermediate', 'advanced']
    
    for skill_level in skill_levels:
        print(f"\n📈 {skill_level.upper()} Level Questions:")
        
        for i in range(3):
            advanced_question = conversation_manager.get_advanced_question(
                skill_level, test_tech_stack, i
            )
            
            if advanced_question:
                print(f"  • [{advanced_question['category']}] {advanced_question['question']}")
            else:
                print(f"  • No advanced question available for iteration {i}")
    
    print("\n✅ Advanced Questions Test Complete!")
    print("🎉 The system can now automatically ask advanced technical questions!")

if __name__ == "__main__":
    test_advanced_questions()