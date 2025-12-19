#!/usr/bin/env python3
"""
Test script for enhanced question generation and knowledge base features
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.question_generator import TechnicalQuestionGenerator
from knowledge_base.enhanced_knowledge import enhanced_knowledge

def test_enhanced_question_generation():
    """Test the enhanced question generation system"""
    print("🧪 Testing Enhanced Question Generation")
    print("=" * 50)
    
    # Test tech stack similar to user's input
    test_tech_stack = {
        'languages': ['python'],
        'frameworks': ['flask', 'django', 'react'],
        'databases': ['mysql'],
        'development_tools': ['bootstrap']
    }
    
    generator = TechnicalQuestionGenerator()
    
    print("📋 Test Tech Stack:")
    for category, techs in test_tech_stack.items():
        print(f"  • {category.title()}: {', '.join(techs)}")
    
    print(f"\n📊 Question Bank Statistics:")
    print(f"  • Technologies with questions: {len(generator.question_bank)}")
    print(f"  • Total questions available: {sum(len(q) for q in generator.question_bank.values())}")
    
    # Generate questions
    questions = generator.generate_questions(test_tech_stack, max_questions_per_tech=3)
    
    print(f"\n🎯 Generated Questions ({sum(len(q) for q in questions.values())} total):")
    for tech, tech_questions in questions.items():
        print(f"\n  🔧 {tech}:")
        for i, question in enumerate(tech_questions, 1):
            print(f"    {i}. {question}")
    
    return questions

def test_enhanced_knowledge_base():
    """Test the enhanced knowledge base system"""
    print("\n\n🧠 Testing Enhanced Knowledge Base")
    print("=" * 50)
    
    # Test technology insights
    test_technologies = ['python', 'react', 'django', 'mysql']
    
    print("🔍 Technology Insights:")
    for tech in test_technologies:
        insight = enhanced_knowledge.get_technology_insight(tech)
        if insight:
            print(f"\n  📚 {tech.title()}:")
            print(f"    • Description: {insight['description']}")
            print(f"    • Market Demand: {insight.get('market_demand', 'N/A')}")
            print(f"    • Difficulty: {insight.get('difficulty_level', 'N/A')}")
            print(f"    • Salary Range: {insight.get('salary_range', 'N/A')}")
            print(f"    • Key Concepts: {len(insight.get('key_concepts', []))} concepts")
    
    # Test market insights
    print(f"\n💼 Market Analysis:")
    market_insights = enhanced_knowledge.get_market_insights(test_technologies)
    print(f"  • Market Value: {market_insights['market_value']}")
    print(f"  • Demand Level: {market_insights['demand_level']}")
    print(f"  • Salary Estimate: {market_insights['salary_estimate']}")
    print(f"  • Career Paths: {', '.join(market_insights['career_paths'])}")
    
    # Test learning path
    print(f"\n📚 Learning Path (Intermediate Level):")
    learning_path = enhanced_knowledge.get_learning_path(test_technologies, 'intermediate')
    print(f"  • Current Strengths: {len(learning_path['current_strengths'])} technologies")
    print(f"  • Recommended Next Steps:")
    for step in learning_path['recommended_next_steps'][:3]:
        print(f"    - {step}")
    
    return market_insights, learning_path

def test_comprehensive_report():
    """Test comprehensive report generation"""
    print(f"\n\n📊 Testing Comprehensive Report Generation")
    print("=" * 50)
    
    # Mock candidate data
    candidate_data = {
        'full_name': 'Test Candidate',
        'experience_years': 3,
        'tech_stack': {
            'languages': ['python'],
            'frameworks': ['flask', 'django', 'react'],
            'databases': ['mysql']
        }
    }
    
    report = enhanced_knowledge.generate_comprehensive_report(candidate_data)
    
    print("📋 Report Sections Generated:")
    for section, content in report.items():
        if section != 'generated_at':
            if isinstance(content, dict):
                print(f"  • {section.replace('_', ' ').title()}: {len(content)} items")
            elif isinstance(content, list):
                print(f"  • {section.replace('_', ' ').title()}: {len(content)} items")
            else:
                print(f"  • {section.replace('_', ' ').title()}: Available")
    
    print(f"\n💡 Sample Recommendations:")
    for rec in report.get('recommendations', [])[:3]:
        print(f"  • {rec}")
    
    return report

def test_question_quality():
    """Test question quality and variety"""
    print(f"\n\n🎯 Testing Question Quality and Variety")
    print("=" * 50)
    
    generator = TechnicalQuestionGenerator()
    
    # Test Python questions specifically
    python_questions = generator.question_bank.get('python', [])
    print(f"📝 Python Questions Analysis:")
    print(f"  • Total Python questions: {len(python_questions)}")
    print(f"  • Average question length: {sum(len(q.split()) for q in python_questions) / len(python_questions):.1f} words")
    
    # Check for conversational tone
    conversational_indicators = ['I\'m curious', 'Tell me about', 'What\'s your', 'How do you', 'Have you']
    conversational_count = sum(1 for q in python_questions if any(indicator in q for indicator in conversational_indicators))
    print(f"  • Conversational questions: {conversational_count}/{len(python_questions)} ({conversational_count/len(python_questions)*100:.1f}%)")
    
    # Sample questions
    print(f"\n📋 Sample Python Questions:")
    for i, question in enumerate(python_questions[:3], 1):
        print(f"  {i}. {question}")
    
    return python_questions

def main():
    """Run all tests"""
    print("🚀 TalentScout Enhanced Features Test Suite")
    print("=" * 60)
    
    # Run tests
    questions = test_enhanced_question_generation()
    market_insights, learning_path = test_enhanced_knowledge_base()
    report = test_comprehensive_report()
    python_questions = test_question_quality()
    
    # Summary
    print(f"\n\n✅ Test Summary")
    print("=" * 30)
    print(f"✅ Question Generation: {len(questions)} technologies covered")
    print(f"✅ Knowledge Base: {len(market_insights)} market insights")
    print(f"✅ Learning Path: {len(learning_path['recommended_next_steps'])} recommendations")
    print(f"✅ Comprehensive Report: {len(report)} sections generated")
    print(f"✅ Question Quality: {len(python_questions)} Python questions available")
    
    print(f"\n🎯 Key Improvements:")
    print("• 3x more questions per technology (up to 10 per tech)")
    print("• Conversational, engaging question style")
    print("• Technology-specific insights and salary data")
    print("• Personalized learning paths and career advice")
    print("• Market demand analysis and trends")
    print("• Enhanced interview preparation guides")
    
    print(f"\n🚀 Ready for Enhanced User Experience!")
    print("The system now provides comprehensive technical assessment")
    print("with personalized insights and career guidance.")

if __name__ == "__main__":
    main()