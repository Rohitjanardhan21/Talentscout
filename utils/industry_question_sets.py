"""
Industry-Specific Question Sets
Tailored questions for different industry domains
"""
from typing import Dict, List, Any, Optional
from enum import Enum
import random

class Industry(Enum):
    FINTECH = "fintech"
    HEALTHCARE = "healthcare"
    ECOMMERCE = "ecommerce"
    GAMING = "gaming"
    ENTERPRISE = "enterprise"
    STARTUP = "startup"
    EDUCATION = "education"
    MEDIA = "media"
    GOVERNMENT = "government"
    GENERAL = "general"

class IndustryQuestionSets:
    """Manages industry-specific technical questions and scenarios"""
    
    def __init__(self):
        self.industry_questions = {
            Industry.FINTECH: {
                'technical_focus': ['security', 'performance', 'compliance', 'data_integrity'],
                'questions': {
                    'python': [
                        "How would you implement secure payment processing in Python while ensuring PCI compliance?",
                        "What's your approach to handling financial calculations to avoid floating-point precision issues?",
                        "How do you implement audit trails for financial transactions in Python applications?",
                        "What security measures do you implement when building financial APIs?",
                        "How would you design a system to handle high-frequency trading data in Python?"
                    ],
                    'react': [
                        "How do you ensure sensitive financial data is not exposed in React applications?",
                        "What's your approach to implementing secure authentication flows in fintech React apps?",
                        "How do you handle real-time financial data updates in React without performance issues?",
                        "What strategies do you use for form validation in financial applications?",
                        "How do you implement accessibility features for financial dashboards?"
                    ],
                    'django': [
                        "How do you implement role-based access control for financial applications in Django?",
                        "What's your approach to database transactions for financial operations in Django?",
                        "How do you handle regulatory compliance requirements in Django applications?",
                        "What security middleware do you implement for fintech Django applications?",
                        "How do you design Django models for complex financial instruments?"
                    ],
                    'mysql': [
                        "How do you ensure ACID compliance for financial transactions in MySQL?",
                        "What's your approach to database backup and recovery for financial data?",
                        "How do you implement audit logging for financial database operations?",
                        "What indexing strategies do you use for high-volume financial data?",
                        "How do you handle database encryption for sensitive financial information?"
                    ]
                },
                'scenarios': [
                    "Design a payment processing system that can handle 10,000 transactions per second",
                    "Implement a fraud detection system that processes transactions in real-time",
                    "Create a compliance reporting system that meets SOX requirements",
                    "Design a cryptocurrency trading platform with real-time price updates"
                ]
            },
            
            Industry.HEALTHCARE: {
                'technical_focus': ['privacy', 'compliance', 'reliability', 'integration'],
                'questions': {
                    'python': [
                        "How do you ensure HIPAA compliance when processing patient data in Python?",
                        "What's your approach to integrating with HL7 FHIR standards in Python applications?",
                        "How do you implement secure data anonymization for medical research?",
                        "What strategies do you use for handling large medical imaging datasets?",
                        "How do you ensure data integrity in critical healthcare applications?"
                    ],
                    'react': [
                        "How do you design accessible interfaces for healthcare professionals with varying tech skills?",
                        "What's your approach to displaying complex medical data in React applications?",
                        "How do you implement secure patient portals with React?",
                        "What strategies do you use for offline functionality in healthcare apps?",
                        "How do you handle real-time patient monitoring data in React?"
                    ],
                    'django': [
                        "How do you implement audit trails for patient data access in Django?",
                        "What's your approach to integrating with Electronic Health Record systems?",
                        "How do you handle patient consent management in Django applications?",
                        "What security measures do you implement for healthcare Django apps?",
                        "How do you design Django models for complex medical workflows?"
                    ]
                },
                'scenarios': [
                    "Design a telemedicine platform that ensures patient privacy",
                    "Create a hospital management system that integrates with existing EHR systems",
                    "Implement a medical device data collection system with real-time monitoring",
                    "Design a clinical trial management system with regulatory compliance"
                ]
            },
            
            Industry.ECOMMERCE: {
                'technical_focus': ['scalability', 'performance', 'user_experience', 'analytics'],
                'questions': {
                    'python': [
                        "How do you implement a recommendation engine for an e-commerce platform?",
                        "What's your approach to handling inventory management at scale?",
                        "How do you implement dynamic pricing algorithms in Python?",
                        "What strategies do you use for processing large volumes of order data?",
                        "How do you handle cart abandonment recovery systems?"
                    ],
                    'react': [
                        "How do you optimize React applications for fast product catalog loading?",
                        "What's your approach to implementing infinite scroll for product listings?",
                        "How do you handle complex shopping cart state management?",
                        "What strategies do you use for A/B testing in React e-commerce apps?",
                        "How do you implement progressive web app features for mobile shopping?"
                    ],
                    'django': [
                        "How do you design Django models for complex product catalogs with variants?",
                        "What's your approach to implementing multi-tenant e-commerce platforms?",
                        "How do you handle order processing workflows in Django?",
                        "What caching strategies do you use for high-traffic e-commerce sites?",
                        "How do you implement search functionality for large product databases?"
                    ]
                },
                'scenarios': [
                    "Design a flash sale system that can handle traffic spikes",
                    "Create a marketplace platform supporting multiple vendors",
                    "Implement a global e-commerce platform with multi-currency support",
                    "Design a subscription-based e-commerce system with recurring billing"
                ]
            },
            
            Industry.GAMING: {
                'technical_focus': ['performance', 'real_time', 'scalability', 'user_engagement'],
                'questions': {
                    'python': [
                        "How do you implement game server logic that can handle thousands of concurrent players?",
                        "What's your approach to anti-cheat systems in multiplayer games?",
                        "How do you handle real-time game state synchronization?",
                        "What strategies do you use for game analytics and player behavior tracking?",
                        "How do you implement matchmaking algorithms for competitive games?"
                    ],
                    'react': [
                        "How do you create responsive game UIs that work across different screen sizes?",
                        "What's your approach to implementing real-time leaderboards and statistics?",
                        "How do you handle game asset loading and optimization in web games?",
                        "What strategies do you use for implementing in-game chat systems?",
                        "How do you create engaging onboarding experiences for new players?"
                    ]
                },
                'scenarios': [
                    "Design a real-time multiplayer game architecture",
                    "Create a game analytics system that tracks player engagement",
                    "Implement a virtual economy system with in-game purchases",
                    "Design a tournament management system for esports"
                ]
            },
            
            Industry.ENTERPRISE: {
                'technical_focus': ['integration', 'security', 'scalability', 'maintainability'],
                'questions': {
                    'python': [
                        "How do you design Python applications that integrate with legacy enterprise systems?",
                        "What's your approach to implementing enterprise-grade logging and monitoring?",
                        "How do you handle complex business rule engines in Python?",
                        "What strategies do you use for enterprise data migration projects?",
                        "How do you implement workflow automation for business processes?"
                    ],
                    'django': [
                        "How do you implement single sign-on (SSO) integration in Django applications?",
                        "What's your approach to building multi-tenant enterprise applications?",
                        "How do you handle complex approval workflows in Django?",
                        "What strategies do you use for enterprise reporting and analytics?",
                        "How do you implement role-based permissions for large organizations?"
                    ]
                },
                'scenarios': [
                    "Design an enterprise resource planning (ERP) system integration",
                    "Create a document management system with version control",
                    "Implement a customer relationship management (CRM) platform",
                    "Design a business intelligence dashboard for executives"
                ]
            }
        }
        
        self.industry_characteristics = {
            Industry.FINTECH: {
                'key_concerns': ['Security', 'Compliance', 'Performance', 'Audit trails'],
                'common_technologies': ['Python', 'Java', 'PostgreSQL', 'Redis', 'Kafka'],
                'regulations': ['PCI DSS', 'SOX', 'GDPR', 'PSD2'],
                'performance_requirements': 'High throughput, low latency'
            },
            Industry.HEALTHCARE: {
                'key_concerns': ['Privacy', 'HIPAA compliance', 'Reliability', 'Integration'],
                'common_technologies': ['Python', 'Java', 'HL7 FHIR', 'PostgreSQL', 'MongoDB'],
                'regulations': ['HIPAA', 'FDA', 'GDPR', 'HITECH'],
                'performance_requirements': 'High availability, data integrity'
            },
            Industry.ECOMMERCE: {
                'key_concerns': ['Scalability', 'User experience', 'Performance', 'Analytics'],
                'common_technologies': ['React', 'Node.js', 'Python', 'Redis', 'Elasticsearch'],
                'regulations': ['GDPR', 'CCPA', 'PCI DSS'],
                'performance_requirements': 'High traffic handling, fast page loads'
            },
            Industry.GAMING: {
                'key_concerns': ['Real-time performance', 'Scalability', 'User engagement'],
                'common_technologies': ['C++', 'Python', 'Unity', 'Unreal', 'WebGL'],
                'regulations': ['COPPA', 'GDPR'],
                'performance_requirements': 'Low latency, high concurrent users'
            }
        }
    
    def detect_industry_from_context(self, 
                                   candidate_data: Dict[str, Any], 
                                   conversation_context: List[str]) -> Industry:
        """Detect likely industry based on candidate data and conversation"""
        
        # Keywords that indicate specific industries
        industry_keywords = {
            Industry.FINTECH: ['payment', 'banking', 'finance', 'trading', 'cryptocurrency', 'fintech'],
            Industry.HEALTHCARE: ['healthcare', 'medical', 'hospital', 'patient', 'hipaa', 'ehr'],
            Industry.ECOMMERCE: ['ecommerce', 'retail', 'shopping', 'marketplace', 'store'],
            Industry.GAMING: ['game', 'gaming', 'player', 'multiplayer', 'unity', 'unreal'],
            Industry.ENTERPRISE: ['enterprise', 'erp', 'crm', 'business', 'corporate'],
            Industry.STARTUP: ['startup', 'mvp', 'agile', 'rapid', 'prototype'],
            Industry.EDUCATION: ['education', 'learning', 'student', 'course', 'academic'],
            Industry.MEDIA: ['media', 'content', 'streaming', 'publishing', 'news']
        }
        
        # Check desired position and company context
        position = candidate_data.get('desired_position', '').lower()
        
        # Combine all text for analysis
        all_text = position + ' ' + ' '.join(conversation_context)
        all_text_lower = all_text.lower()
        
        # Score each industry
        industry_scores = {}
        for industry, keywords in industry_keywords.items():
            score = sum(1 for keyword in keywords if keyword in all_text_lower)
            industry_scores[industry] = score
        
        # Return industry with highest score, or GENERAL if no clear match
        if industry_scores and max(industry_scores.values()) > 0:
            return max(industry_scores, key=industry_scores.get)
        
        return Industry.GENERAL
    
    def get_industry_specific_questions(self, 
                                      industry: Industry,
                                      tech_stack: Dict[str, List[str]],
                                      num_questions: int = 3) -> Dict[str, List[str]]:
        """Get industry-specific questions for the given tech stack"""
        
        if industry not in self.industry_questions:
            return {}
        
        industry_data = self.industry_questions[industry]
        questions_by_tech = industry_data.get('questions', {})
        
        result = {}
        
        # Get questions for each technology in the stack
        for category, technologies in tech_stack.items():
            for tech in technologies:
                tech_lower = tech.lower()
                if tech_lower in questions_by_tech:
                    available_questions = questions_by_tech[tech_lower]
                    selected_questions = random.sample(
                        available_questions, 
                        min(num_questions, len(available_questions))
                    )
                    result[f"{tech} ({industry.value.title()})"] = selected_questions
        
        return result
    
    def get_industry_scenarios(self, industry: Industry) -> List[str]:
        """Get industry-specific scenarios and system design questions"""
        
        if industry not in self.industry_questions:
            return []
        
        return self.industry_questions[industry].get('scenarios', [])
    
    def get_industry_insights(self, industry: Industry) -> Dict[str, Any]:
        """Get insights about the industry including key concerns and technologies"""
        
        return self.industry_characteristics.get(industry, {
            'key_concerns': ['General software development'],
            'common_technologies': ['Various'],
            'regulations': ['Standard compliance'],
            'performance_requirements': 'Standard performance'
        })
    
    def generate_industry_assessment(self, 
                                   industry: Industry,
                                   candidate_responses: List[str]) -> Dict[str, Any]:
        """Generate an assessment of candidate's industry readiness"""
        
        if industry == Industry.GENERAL:
            return {'industry_readiness': 'general', 'recommendations': []}
        
        industry_data = self.industry_characteristics.get(industry, {})
        key_concerns = industry_data.get('key_concerns', [])
        
        # Analyze responses for industry-specific knowledge
        all_responses = ' '.join(candidate_responses).lower()
        
        concern_coverage = {}
        for concern in key_concerns:
            concern_keywords = {
                'Security': ['security', 'encryption', 'authentication', 'authorization'],
                'Compliance': ['compliance', 'regulation', 'audit', 'gdpr', 'hipaa'],
                'Performance': ['performance', 'optimization', 'scalability', 'latency'],
                'Privacy': ['privacy', 'data protection', 'anonymization', 'consent'],
                'Integration': ['integration', 'api', 'microservices', 'legacy'],
                'User experience': ['ux', 'user experience', 'accessibility', 'usability']
            }
            
            keywords = concern_keywords.get(concern, [concern.lower()])
            mentions = sum(1 for keyword in keywords if keyword in all_responses)
            concern_coverage[concern] = mentions > 0
        
        # Calculate industry readiness score
        covered_concerns = sum(1 for covered in concern_coverage.values() if covered)
        readiness_score = covered_concerns / len(key_concerns) if key_concerns else 0
        
        # Generate recommendations
        recommendations = []
        for concern, covered in concern_coverage.items():
            if not covered:
                recommendations.append(f"Consider learning more about {concern.lower()} in {industry.value} context")
        
        # Determine readiness level
        if readiness_score >= 0.8:
            readiness_level = 'excellent'
        elif readiness_score >= 0.6:
            readiness_level = 'good'
        elif readiness_score >= 0.4:
            readiness_level = 'moderate'
        else:
            readiness_level = 'developing'
        
        return {
            'industry': industry.value,
            'industry_readiness': readiness_level,
            'readiness_score': readiness_score,
            'concern_coverage': concern_coverage,
            'recommendations': recommendations,
            'key_strengths': [concern for concern, covered in concern_coverage.items() if covered]
        }

# Global instance
industry_questions = IndustryQuestionSets()