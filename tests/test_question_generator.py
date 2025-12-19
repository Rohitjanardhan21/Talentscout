"""
Unit tests for the question generator module
"""
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.question_generator import TechnicalQuestionGenerator

class TestTechnicalQuestionGenerator(unittest.TestCase):
    """Test cases for TechnicalQuestionGenerator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TechnicalQuestionGenerator()
    
    def test_generate_questions_python(self):
        """Test question generation for Python"""
        tech_stack = {
            'languages': ['Python'],
            'frameworks': ['Django']
        }
        
        questions = self.generator.generate_questions(tech_stack, max_questions_per_tech=2)
        
        self.assertIn('Python', questions)
        self.assertIn('Django', questions)
        self.assertEqual(len(questions['Python']), 2)
        self.assertEqual(len(questions['Django']), 2)
    
    def test_generate_questions_javascript(self):
        """Test question generation for JavaScript"""
        tech_stack = {
            'languages': ['JavaScript'],
            'frameworks': ['React']
        }
        
        questions = self.generator.generate_questions(tech_stack, max_questions_per_tech=1)
        
        self.assertIn('JavaScript', questions)
        self.assertIn('React', questions)
        self.assertEqual(len(questions['JavaScript']), 1)
        self.assertEqual(len(questions['React']), 1)
    
    def test_generate_questions_unknown_tech(self):
        """Test question generation for unknown technologies"""
        tech_stack = {
            'languages': ['UnknownLanguage'],
            'frameworks': ['UnknownFramework']
        }
        
        questions = self.generator.generate_questions(tech_stack)
        
        # Should return empty dict for unknown technologies
        self.assertEqual(len(questions), 0)
    
    def test_get_fallback_questions_general(self):
        """Test fallback questions for general level"""
        questions = self.generator.get_fallback_questions("general")
        
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)
        self.assertIsInstance(questions[0], str)
    
    def test_get_fallback_questions_senior(self):
        """Test fallback questions for senior level"""
        questions = self.generator.get_fallback_questions("senior")
        
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)
        # Senior questions should be different from general
        general_questions = self.generator.get_fallback_questions("general")
        self.assertNotEqual(questions, general_questions)
    
    def test_format_questions_for_display(self):
        """Test question formatting for display"""
        questions_dict = {
            'Python': ['Question 1', 'Question 2'],
            'Django': ['Question 3']
        }
        
        formatted = self.generator.format_questions_for_display(questions_dict)
        
        self.assertIn('Python', formatted)
        self.assertIn('Django', formatted)
        self.assertIn('Question 1', formatted)
        self.assertIn('Question 2', formatted)
        self.assertIn('Question 3', formatted)
    
    def test_format_questions_empty(self):
        """Test question formatting with empty input"""
        formatted = self.generator.format_questions_for_display({})
        
        self.assertIn('No specific technical questions', formatted)

if __name__ == '__main__':
    unittest.main()