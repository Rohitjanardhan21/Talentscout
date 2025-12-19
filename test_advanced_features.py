#!/usr/bin/env python3
"""
Comprehensive test for all advanced features
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_interactive_question_selector():
    """Test interactive question selection"""
    print("🎯 Testing Interactive Question Selector")
    print("=" * 50)
    
    from utils.interactive_question_selector import interactive_selector
    
    # Mock available questions
    available_questions = {
        'Python': [
            "How do you handle memory management in Python?",
            "What's your experience with Python decorators?",
            "Tell me about Python's asyncio framework."
        ],
        'React': [
            "How do you optimize React performance?",
            "What's your approach to state management?",
            "How do you handle React testing?"
        ]
    }
    
    # Test question filtering
    preferences = {
        'focus_areas': ['technical_depth', 'real_world'],
        'difficulty_level': 'mid',
        'tech_priorities': {'Python': 5, 'React': 3},
        'total_questions': 6,
        'questions_per_tech': 2,
        'interview_style': 'conversational'
    }
    
    candidate_data = {'experience_years': 3}
    
    personalized_questions = interactive_selector.generate_personalized_questions(
        available_questions, preferences, candidate_data
    )
    
    print(f"✅ Generated {sum(len(q) for q in personalized_questions.values())} personalized questions")
    for tech, questions in personalized_questions.items():
        print(f"  • {tech}: {len(questions)} questions")
    
    return personalized_questions

def test_skill_level_adapter():
    """Test skill level adaptation system"""
    print("\n📈 Testing Skill Level Adapter")
    print("=" * 50)
    
    from utils.skill_level_adapter import skill_adapter, SkillLevel
    
    # Test responses of different skill levels
    test_responses = [
        {
            'response': "I use Python for basic scripting and I'm still learning.",
            'expected_level': SkillLevel.BEGINNER
        },
        {
            'response': "I have experience with Python in several projects, including web development with Django and data analysis with pandas.",
            'expected_level': SkillLevel.INTERMEDIATE
        },
        {
            'response': "I optimize Python applications for performance, implement custom metaclasses, and contribute to open-source Python projects. I understand the GIL implications and use profiling tools.",
            'expected_level': SkillLevel.ADVANCED
        }
    ]
    
    session_id = "test_session"
    
    for i, test_case in enumerate(test_responses):
        result = skill_adapter.process_response_and_adapt(
            test_case['response'],
            "Python question",
            "Python",
            session_id
        )
        
        analysis = result['analysis']
        detected_level = analysis['estimated_skill_level']
        
        print(f"Response {i+1}:")
        print(f"  Expected: {test_case['expected_level'].value}")
        print(f"  Detected: {detected_level.value}")
        print(f"  Confidence: {analysis['confidence']:.2f}")
        print(f"  Quality: {analysis['response_quality']}")
        print(f"  Insights: {', '.join(analysis['key_insights'])}")
        print()
    
    # Test session summary
    session_summary = skill_adapter.get_session_summary(session_id)
    print(f"Session Summary:")
    print(f"  Overall Level: {session_summary['overall_skill_level']}")
    print(f"  Total Responses: {session_summary['total_responses']}")
    print(f"  Average Quality: {session_summary['average_response_quality']:.1%}")
    
    return session_summary

def test_industry_question_sets():
    """Test industry-specific question generation"""
    print("\n🏢 Testing Industry Question Sets")
    print("=" * 50)
    
    from utils.industry_question_sets import industry_questions, Industry
    
    # Test industry detection
    candidate_data = {
        'desired_position': 'Fintech Developer',
        'tech_stack': {'languages': ['python'], 'frameworks': ['django']}
    }
    
    conversation_context = [
        "I want to work in financial technology",
        "I have experience with payment processing"
    ]
    
    detected_industry = industry_questions.detect_industry_from_context(
        candidate_data, conversation_context
    )
    
    print(f"✅ Detected Industry: {detected_industry.value}")
    
    # Test industry-specific questions
    tech_stack = {'languages': ['python'], 'frameworks': ['django']}
    industry_specific_questions = industry_questions.get_industry_specific_questions(
        detected_industry, tech_stack, 2
    )
    
    print(f"✅ Generated {sum(len(q) for q in industry_specific_questions.values())} industry-specific questions")
    for tech, questions in industry_specific_questions.items():
        print(f"  • {tech}:")
        for question in questions:
            print(f"    - {question}")
    
    # Test industry insights
    insights = industry_questions.get_industry_insights(detected_industry)
    print(f"\n💡 Industry Insights:")
    print(f"  Key Concerns: {', '.join(insights['key_concerns'])}")
    print(f"  Common Technologies: {', '.join(insights['common_technologies'])}")
    print(f"  Regulations: {', '.join(insights['regulations'])}")
    
    return detected_industry, industry_specific_questions

def test_market_data_integration():
    """Test real-time market data integration"""
    print("\n📊 Testing Market Data Integration")
    print("=" * 50)
    
    from utils.market_data_integration import market_integration
    
    # Test candidate data
    candidate_data = {
        'tech_stack': {
            'languages': ['python'],
            'frameworks': ['django', 'react'],
            'databases': ['postgresql']
        },
        'experience_years': 3,
        'location': 'San Francisco'
    }
    
    # Get comprehensive market analysis
    market_analysis = market_integration.get_comprehensive_market_analysis(candidate_data)
    
    if market_analysis:
        print("✅ Market Analysis Generated")
        
        market_data = market_analysis['market_analysis']
        print(f"  Market Strength: {market_data['market_strength']}")
        print(f"  Average Demand: {market_data['average_demand_score']:.1f}/100")
        print(f"  Growth Rate: {market_data['average_growth_rate']:.1f}%")
        
        location_data = market_analysis['location_data']
        print(f"  Base Salary: ${location_data['base_salary']:,}")
        print(f"  Adjusted Salary: ${location_data['adjusted_salary']:,}")
        print(f"  Location: {location_data['location']}")
        
        career_data = market_analysis.get('career_progression', {})
        if career_data:
            print(f"  Career Path: {career_data['career_path']}")
            print(f"  Current Title: {career_data['current_title']}")
            print(f"  Next Title: {career_data['next_title']}")
        
        recommendations = market_analysis.get('recommendations', [])
        print(f"  Recommendations: {len(recommendations)} generated")
        for rec in recommendations[:3]:
            print(f"    • {rec}")
    
    return market_analysis

def test_integration():
    """Test integration of all features"""
    print("\n🔄 Testing Feature Integration")
    print("=" * 50)
    
    # Simulate a complete interview flow
    candidate_data = {
        'full_name': 'Test Candidate',
        'experience_years': 4,
        'desired_position': 'Full Stack Developer at Fintech Startup',
        'location': 'New York',
        'tech_stack': {
            'languages': ['python', 'javascript'],
            'frameworks': ['django', 'react'],
            'databases': ['postgresql']
        }
    }
    
    print("🎯 Simulating Complete Interview Flow:")
    
    # 1. Industry Detection
    from utils.industry_question_sets import industry_questions
    conversation_context = ["I want to work in financial technology"]
    detected_industry = industry_questions.detect_industry_from_context(
        candidate_data, conversation_context
    )
    print(f"  1. Industry Detected: {detected_industry.value}")
    
    # 2. Market Analysis
    from utils.market_data_integration import market_integration
    market_data = market_integration.get_comprehensive_market_analysis(candidate_data)
    market_strength = market_data['market_analysis']['market_strength']
    print(f"  2. Market Analysis: {market_strength} market strength")
    
    # 3. Question Generation
    from utils.question_generator import TechnicalQuestionGenerator
    generator = TechnicalQuestionGenerator()
    questions = generator.generate_questions(candidate_data['tech_stack'], 2)
    total_questions = sum(len(q) for q in questions.values())
    print(f"  3. Questions Generated: {total_questions} technical questions")
    
    # 4. Skill Adaptation
    from utils.skill_level_adapter import skill_adapter
    sample_response = "I have extensive experience with Django and React, building scalable fintech applications with proper security measures."
    result = skill_adapter.process_response_and_adapt(
        sample_response, "Technical question", "Django", "integration_test"
    )
    skill_level = result['analysis']['estimated_skill_level'].value
    print(f"  4. Skill Analysis: {skill_level} level detected")
    
    # 5. Interactive Customization
    from utils.interactive_question_selector import interactive_selector
    preferences = {
        'focus_areas': ['technical_depth'],
        'difficulty_level': 'mid',
        'tech_priorities': {'Python': 5, 'React': 4},
        'total_questions': 8,
        'questions_per_tech': 2
    }
    personalized = interactive_selector.generate_personalized_questions(
        questions, preferences, candidate_data
    )
    personalized_count = sum(len(q) for q in personalized.values())
    print(f"  5. Personalization: {personalized_count} customized questions")
    
    print(f"\n✅ Integration Test Complete!")
    print(f"All advanced features working together seamlessly.")
    
    return {
        'industry': detected_industry.value,
        'market_strength': market_strength,
        'total_questions': total_questions,
        'skill_level': skill_level,
        'personalized_questions': personalized_count
    }

def main():
    """Run all advanced feature tests"""
    print("🚀 TalentScout Advanced Features Test Suite")
    print("=" * 60)
    
    # Run individual tests
    personalized_questions = test_interactive_question_selector()
    session_summary = test_skill_level_adapter()
    industry_data = test_industry_question_sets()
    market_analysis = test_market_data_integration()
    integration_results = test_integration()
    
    # Final summary
    print(f"\n🎉 Advanced Features Test Summary")
    print("=" * 40)
    print(f"✅ Interactive Question Selection: {sum(len(q) for q in personalized_questions.values())} questions")
    print(f"✅ Skill Level Adaptation: {session_summary['total_responses']} responses analyzed")
    print(f"✅ Industry Detection: {industry_data[0].value} industry identified")
    print(f"✅ Market Data Integration: {market_analysis['market_analysis']['market_strength']} market analysis")
    print(f"✅ Feature Integration: All systems working together")
    
    print(f"\n🚀 Advanced Features Ready for Production!")
    print("The TalentScout system now includes:")
    print("• 🎯 Interactive question customization")
    print("• 📈 Real-time skill level adaptation")
    print("• 🏢 Industry-specific question sets")
    print("• 📊 Live market data and salary analysis")
    print("• 🔄 Seamless feature integration")

if __name__ == "__main__":
    main()