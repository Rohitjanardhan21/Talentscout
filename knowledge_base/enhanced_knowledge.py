"""
Enhanced Knowledge Base for TalentScout Hiring Assistant
Provides comprehensive technical knowledge and insights
"""
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

class EnhancedKnowledgeBase:
    """Enhanced knowledge base with comprehensive technical information"""
    
    def __init__(self):
        self.technology_insights = {
            'python': {
                'description': 'High-level, interpreted programming language known for readability and versatility',
                'key_concepts': [
                    'Object-oriented programming', 'Dynamic typing', 'Garbage collection',
                    'List comprehensions', 'Decorators', 'Generators', 'Context managers'
                ],
                'common_use_cases': [
                    'Web development', 'Data science', 'Machine learning', 'Automation',
                    'Scientific computing', 'DevOps scripting'
                ],
                'frameworks': ['Django', 'Flask', 'FastAPI', 'Pyramid'],
                'libraries': ['NumPy', 'Pandas', 'Requests', 'SQLAlchemy'],
                'difficulty_level': 'Beginner to Advanced',
                'market_demand': 'Very High',
                'salary_range': '$70k - $150k+',
                'learning_resources': [
                    'Python.org official tutorial',
                    'Automate the Boring Stuff with Python',
                    'Real Python tutorials'
                ]
            },
            'javascript': {
                'description': 'Dynamic programming language essential for web development',
                'key_concepts': [
                    'Prototypal inheritance', 'Closures', 'Event loop', 'Promises',
                    'Async/await', 'DOM manipulation', 'ES6+ features'
                ],
                'common_use_cases': [
                    'Frontend development', 'Backend development (Node.js)',
                    'Mobile apps', 'Desktop applications', 'Game development'
                ],
                'frameworks': ['React', 'Vue', 'Angular', 'Express', 'Next.js'],
                'libraries': ['jQuery', 'Lodash', 'Axios', 'Moment.js'],
                'difficulty_level': 'Beginner to Advanced',
                'market_demand': 'Extremely High',
                'salary_range': '$65k - $140k+',
                'learning_resources': [
                    'MDN Web Docs',
                    'JavaScript.info',
                    'You Don\'t Know JS book series'
                ]
            },
            'react': {
                'description': 'Popular JavaScript library for building user interfaces',
                'key_concepts': [
                    'Virtual DOM', 'Components', 'JSX', 'State management',
                    'Hooks', 'Props', 'Context API', 'Lifecycle methods'
                ],
                'common_use_cases': [
                    'Single-page applications', 'Progressive web apps',
                    'Mobile apps (React Native)', 'Component libraries'
                ],
                'ecosystem': ['Redux', 'MobX', 'React Router', 'Material-UI', 'Styled Components'],
                'difficulty_level': 'Intermediate',
                'market_demand': 'Extremely High',
                'salary_range': '$75k - $150k+',
                'learning_resources': [
                    'Official React documentation',
                    'React Tutorial by Kent C. Dodds',
                    'Scrimba React course'
                ]
            },
            'django': {
                'description': 'High-level Python web framework that encourages rapid development',
                'key_concepts': [
                    'MTV architecture', 'ORM', 'Admin interface', 'Middleware',
                    'Templates', 'Forms', 'Authentication', 'Migrations'
                ],
                'common_use_cases': [
                    'Web applications', 'REST APIs', 'Content management',
                    'E-commerce platforms', 'Social networks'
                ],
                'ecosystem': ['Django REST Framework', 'Celery', 'Channels', 'Wagtail'],
                'difficulty_level': 'Intermediate',
                'market_demand': 'High',
                'salary_range': '$80k - $140k+',
                'learning_resources': [
                    'Django official tutorial',
                    'Django for Beginners book',
                    'Two Scoops of Django'
                ]
            },
            'mysql': {
                'description': 'Popular open-source relational database management system',
                'key_concepts': [
                    'ACID properties', 'Indexing', 'Joins', 'Normalization',
                    'Stored procedures', 'Triggers', 'Replication', 'Partitioning'
                ],
                'common_use_cases': [
                    'Web applications', 'Data warehousing', 'E-commerce',
                    'Content management', 'Analytics'
                ],
                'tools': ['MySQL Workbench', 'phpMyAdmin', 'Percona Toolkit'],
                'difficulty_level': 'Beginner to Advanced',
                'market_demand': 'High',
                'salary_range': '$60k - $120k+',
                'learning_resources': [
                    'MySQL official documentation',
                    'MySQL Crash Course book',
                    'W3Schools SQL tutorial'
                ]
            }
        }
        
        self.interview_insights = {
            'question_categories': {
                'technical_depth': 'Assess deep understanding of technologies',
                'problem_solving': 'Evaluate analytical and debugging skills',
                'system_design': 'Test architectural thinking and scalability',
                'best_practices': 'Check knowledge of industry standards',
                'real_world_experience': 'Understand practical application of skills'
            },
            'evaluation_criteria': {
                'accuracy': 'Correctness of technical information',
                'depth': 'Level of understanding demonstrated',
                'communication': 'Ability to explain complex concepts clearly',
                'experience': 'Evidence of hands-on practical experience',
                'problem_solving': 'Approach to tackling challenges'
            }
        }
        
        self.industry_trends = {
            'hot_technologies': [
                'React/Vue.js for frontend',
                'Python for backend and AI/ML',
                'Docker/Kubernetes for DevOps',
                'AWS/Azure for cloud computing',
                'TypeScript for type safety'
            ],
            'emerging_trends': [
                'Serverless architecture',
                'Microservices',
                'JAMstack development',
                'Edge computing',
                'WebAssembly'
            ],
            'skill_combinations': {
                'full_stack_web': ['JavaScript', 'React/Vue', 'Node.js', 'Database'],
                'data_science': ['Python', 'SQL', 'Pandas', 'Machine Learning'],
                'devops_engineer': ['Docker', 'Kubernetes', 'AWS/Azure', 'CI/CD'],
                'mobile_developer': ['React Native/Flutter', 'JavaScript/Dart', 'APIs']
            }
        }
    
    def get_technology_insight(self, technology: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive insight about a specific technology"""
        tech_lower = technology.lower()
        return self.technology_insights.get(tech_lower)
    
    def get_learning_path(self, tech_stack: List[str], experience_level: str) -> Dict[str, Any]:
        """Generate personalized learning path based on current tech stack"""
        learning_path = {
            'current_strengths': [],
            'recommended_next_steps': [],
            'skill_gaps': [],
            'career_opportunities': []
        }
        
        # Analyze current tech stack
        for tech in tech_stack:
            insight = self.get_technology_insight(tech)
            if insight:
                learning_path['current_strengths'].append({
                    'technology': tech,
                    'market_demand': insight.get('market_demand', 'Unknown'),
                    'difficulty': insight.get('difficulty_level', 'Unknown')
                })
        
        # Recommend next steps based on experience level
        if experience_level.lower() in ['junior', 'entry']:
            learning_path['recommended_next_steps'] = [
                'Master fundamentals of your primary language',
                'Learn version control (Git) thoroughly',
                'Practice data structures and algorithms',
                'Build portfolio projects',
                'Learn testing frameworks'
            ]
        elif experience_level.lower() in ['mid', 'intermediate']:
            learning_path['recommended_next_steps'] = [
                'Learn system design principles',
                'Master database optimization',
                'Explore cloud platforms (AWS/Azure)',
                'Learn containerization (Docker)',
                'Practice architectural patterns'
            ]
        else:  # Senior level
            learning_path['recommended_next_steps'] = [
                'Master distributed systems',
                'Learn leadership and mentoring skills',
                'Explore emerging technologies',
                'Contribute to open source',
                'Develop technical writing skills'
            ]
        
        return learning_path
    
    def get_interview_preparation_guide(self, tech_stack: List[str]) -> Dict[str, Any]:
        """Generate interview preparation guide based on tech stack"""
        guide = {
            'technical_topics_to_review': [],
            'common_questions_by_tech': {},
            'coding_challenges': [],
            'system_design_topics': [],
            'behavioral_questions': []
        }
        
        # Technical topics based on tech stack
        for tech in tech_stack:
            insight = self.get_technology_insight(tech)
            if insight:
                guide['technical_topics_to_review'].extend(insight.get('key_concepts', []))
        
        # Common system design topics
        guide['system_design_topics'] = [
            'Scalability and load balancing',
            'Database design and optimization',
            'Caching strategies',
            'API design and versioning',
            'Security considerations',
            'Monitoring and logging'
        ]
        
        # Behavioral questions
        guide['behavioral_questions'] = [
            'Tell me about a challenging project you worked on',
            'How do you handle tight deadlines?',
            'Describe a time you had to learn a new technology quickly',
            'How do you approach debugging complex issues?',
            'Tell me about a time you disagreed with a team member'
        ]
        
        return guide
    
    def get_market_insights(self, tech_stack: List[str]) -> Dict[str, Any]:
        """Get market insights and career advice based on tech stack"""
        insights = {
            'market_value': 'Medium',
            'demand_level': 'Moderate',
            'salary_estimate': '$70k - $120k',
            'career_paths': [],
            'industry_fit': [],
            'growth_potential': 'Good'
        }
        
        # Analyze tech stack for market value
        high_demand_techs = ['react', 'python', 'javascript', 'aws', 'docker', 'kubernetes']
        stack_lower = [tech.lower() for tech in tech_stack]
        
        demand_score = sum(1 for tech in stack_lower if tech in high_demand_techs)
        
        if demand_score >= 3:
            insights['market_value'] = 'High'
            insights['demand_level'] = 'Very High'
            insights['salary_estimate'] = '$90k - $150k+'
        elif demand_score >= 2:
            insights['market_value'] = 'Good'
            insights['demand_level'] = 'High'
            insights['salary_estimate'] = '$80k - $130k'
        
        # Career path suggestions
        if any(tech in stack_lower for tech in ['react', 'vue', 'angular']):
            insights['career_paths'].append('Frontend Developer')
        if any(tech in stack_lower for tech in ['python', 'django', 'flask', 'nodejs']):
            insights['career_paths'].append('Backend Developer')
        if len(set(stack_lower) & set(['react', 'python', 'mysql'])) >= 2:
            insights['career_paths'].append('Full Stack Developer')
        if any(tech in stack_lower for tech in ['docker', 'kubernetes', 'aws']):
            insights['career_paths'].append('DevOps Engineer')
        
        return insights
    
    def generate_comprehensive_report(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive knowledge-based report for candidate"""
        tech_stack = []
        if 'tech_stack' in candidate_data:
            for category, technologies in candidate_data['tech_stack'].items():
                tech_stack.extend(technologies)
        
        experience_level = candidate_data.get('experience_years', 0)
        if experience_level <= 2:
            exp_level = 'junior'
        elif experience_level <= 5:
            exp_level = 'intermediate'
        else:
            exp_level = 'senior'
        
        report = {
            'technology_analysis': {},
            'learning_path': self.get_learning_path(tech_stack, exp_level),
            'interview_guide': self.get_interview_preparation_guide(tech_stack),
            'market_insights': self.get_market_insights(tech_stack),
            'recommendations': [],
            'generated_at': datetime.now().isoformat()
        }
        
        # Analyze each technology
        for tech in tech_stack:
            insight = self.get_technology_insight(tech)
            if insight:
                report['technology_analysis'][tech] = insight
        
        # Generate recommendations
        recommendations = []
        if len(tech_stack) < 3:
            recommendations.append("Consider expanding your technology stack for better market opportunities")
        
        if not any(tech.lower() in ['git', 'github'] for tech in tech_stack):
            recommendations.append("Ensure strong version control skills (Git) are highlighted")
        
        if experience_level >= 3 and not any(tech.lower() in ['docker', 'aws', 'azure'] for tech in tech_stack):
            recommendations.append("Consider learning cloud technologies or containerization for career growth")
        
        report['recommendations'] = recommendations
        
        return report

# Global instance
enhanced_knowledge = EnhancedKnowledgeBase()