"""
Unit tests for the data handler module
"""
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_handler import CandidateDataHandler

class TestCandidateDataHandler(unittest.TestCase):
    """Test cases for CandidateDataHandler"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.handler = CandidateDataHandler()
    
    def test_validate_email_valid(self):
        """Test email validation with valid emails"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "firstname+lastname@company.org"
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(self.handler.validate_email(email))
    
    def test_validate_email_invalid(self):
        """Test email validation with invalid emails"""
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "user@",
            "user@domain",
            ""
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(self.handler.validate_email(email))
    
    def test_validate_phone_valid(self):
        """Test phone validation with valid numbers"""
        valid_phones = [
            "+1234567890",
            "123-456-7890",
            "(123) 456-7890",
            "1234567890"
        ]
        
        for phone in valid_phones:
            with self.subTest(phone=phone):
                self.assertTrue(self.handler.validate_phone(phone))
    
    def test_validate_phone_invalid(self):
        """Test phone validation with invalid numbers"""
        invalid_phones = [
            "123",
            "abc-def-ghij",
            "",
            "12345678901234567890"  # Too long
        ]
        
        for phone in invalid_phones:
            with self.subTest(phone=phone):
                self.assertFalse(self.handler.validate_phone(phone))
    
    def test_validate_experience_valid(self):
        """Test experience validation with valid inputs"""
        valid_experiences = ["5", "10", "0", "25"]
        expected_results = [5, 10, 0, 25]
        
        for exp, expected in zip(valid_experiences, expected_results):
            with self.subTest(experience=exp):
                result = self.handler.validate_experience(exp)
                self.assertEqual(result, expected)
    
    def test_validate_experience_invalid(self):
        """Test experience validation with invalid inputs"""
        invalid_experiences = ["abc", "-5", "100", ""]
        
        for exp in invalid_experiences:
            with self.subTest(experience=exp):
                result = self.handler.validate_experience(exp)
                self.assertIsNone(result)
    
    def test_parse_tech_stack(self):
        """Test tech stack parsing"""
        tech_input = "Python, Django, PostgreSQL, Docker, AWS, React"
        result = self.handler.parse_tech_stack(tech_input)
        
        self.assertIn('languages', result)
        self.assertIn('Python', result['languages'])
        self.assertIn('frameworks', result)
        self.assertIn('Django', result['frameworks'])
        self.assertIn('React', result['frameworks'])
    
    def test_store_candidate_info(self):
        """Test storing candidate information"""
        # Test valid data
        self.assertTrue(self.handler.store_candidate_info('full_name', 'John Doe'))
        self.assertTrue(self.handler.store_candidate_info('email', 'john@example.com'))
        self.assertTrue(self.handler.store_candidate_info('experience_years', '5'))
        
        # Test invalid data
        self.assertFalse(self.handler.store_candidate_info('email', 'invalid-email'))
        self.assertFalse(self.handler.store_candidate_info('phone', '123'))
    
    def test_get_candidate_data(self):
        """Test getting candidate data"""
        self.handler.store_candidate_info('full_name', 'Jane Doe')
        self.handler.store_candidate_info('email', 'jane@example.com')
        
        data = self.handler.get_candidate_data()
        self.assertEqual(data['full_name'], 'Jane Doe')
        self.assertEqual(data['email'], 'jane@example.com')

if __name__ == '__main__':
    unittest.main()