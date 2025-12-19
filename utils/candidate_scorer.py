"""
Advanced candidate scoring and analysis system
"""
from typing import Dict, List, Any, Tuple
import re
from datetime import datetime

class CandidateScorer:
    """Advanced scoring system for candidate evaluation"""
    
    def __init__(self):
        self.scoring_weights = {
            'experience': 0.25,
            'tech_stack_breadth': 0.20,
            'tech_stack_depth': 0.20,
            'communication': 0.15,
            'role_fit': 0.20
        }
        
        # Technology tier scoring
        self.tech_tiers = {
            'tier_1': {  # High-demand, modern technologies
                'languages': ['python', 'javascript', 'typescript', 'go', 'rust'],
                'frameworks': ['react', 'vue', 'django', 'fastapi', 'spring'],
                'databases': ['postgresql', 'mongodb', 'redis'],
                'tools': ['docker', 'kubernetes', 'aws', 'terraform'],
                'score': 10
            },
            'tier_2': {  # Solid, established technologies
                'languages': ['java', 'c#', 'php', 'ruby'],
                'frameworks': ['angular', 'flask', 'laravel', 'rails'],
                'databases': ['mysql', 'sqlite'],
                'tools': ['git', 'jenkins', 'azure', 'nginx'],
                'score': 7
            },
            'tier_3': {  # Legacy but still relevant
                'languages': ['c++', 'scala', 'kotlin'],
                'frameworks': ['asp.net'],
                'databases': ['oracle', 'cassandra'],
                'tools': ['ansible'],
                'score': 5
            }
        }
    
    def calculate_experience_score(self, years: int) -> Tuple[int, str]:
        """Calculate experience score and level"""
        if years >= 8:
            return 10, "Senior+"
        elif years >= 5:
            return 8, "Senior"
        elif years >= 3:
            return 6, "Mid-level"
        elif years >= 1:
            return 4, "Junior+"
        else:
            return 2, "Entry-level"
    
    def calculate_tech_stack_score(self, tech_stack: Dict[str, List[str]]) -> Tuple[int, int, Dict]:
        """Calculate tech stack breadth and depth scores"""
        breadth_score = 0
        depth_score = 0
        tech_analysis = {
            'tier_1_count': 0,
            'tier_2_count': 0,
            'tier_3_count': 0,
            'total_technologies': 0,
            'categories_covered': len(tech_stack),
            'modern_stack': False,
            'full_stack': False
        }
        
        # Count technologies by tier
        for category, technologies in tech_stack.items():
            for tech in technologies:
                tech_lower = tech.lower()
                tech_analysis['total_technologies'] += 1
                
                # Check which tier this technology belongs to
                for tier_name, tier_data in self.tech_tiers.items():
                    if tech_lower in tier_data.get(category, []):
                        if tier_name == 'tier_1':
                            tech_analysis['tier_1_count'] += 1
                            depth_score += 10
                        elif tier_name == 'tier_2':
                            tech_analysis['tier_2_count'] += 1
                            depth_score += 7
                        elif tier_name == 'tier_3':
                            tech_analysis['tier_3_count'] += 1
                            depth_score += 5
                        break
        
        # Calculate breadth score (diversity of technologies)
        breadth_score = min(tech_analysis['categories_covered'] * 2, 10)
        
        # Bonus for modern stack
        if tech_analysis['tier_1_count'] >= 3:
            tech_analysis['modern_stack'] = True
            depth_score += 5
        
        # Bonus for full-stack capabilities
        has_frontend = any(tech.lower() in ['react', 'vue', 'angular', 'javascript', 'typescript'] 
                          for techs in tech_stack.values() for tech in techs)
        has_backend = any(tech.lower() in ['python', 'java', 'django', 'spring', 'fastapi'] 
                         for techs in tech_stack.values() for tech in techs)
        has_database = 'databases' in tech_stack and len(tech_stack['databases']) > 0
        
        if has_frontend and has_backend and has_database:
            tech_analysis['full_stack'] = True
            breadth_score += 3
        
        return min(breadth_score, 10), min(depth_score, 10), tech_analysis
    
    def calculate_communication_score(self, messages: List[Dict]) -> Tuple[int, Dict]:
        """Analyze communication quality from conversation"""
        if len(messages) < 4:  # Not enough data
            return 5, {'insufficient_data': True}
        
        user_messages = [msg['content'] for msg in messages if msg['role'] == 'user']
        
        analysis = {
            'avg_response_length': 0,
            'detailed_responses': 0,
            'professional_tone': 0,
            'technical_depth': 0
        }
        
        total_length = 0
        for message in user_messages:
            length = len(message.split())
            total_length += length
            
            # Detailed responses (more than 10 words)
            if length > 10:
                analysis['detailed_responses'] += 1
            
            # Professional indicators
            professional_indicators = ['experience', 'project', 'worked', 'developed', 'implemented']
            if any(indicator in message.lower() for indicator in professional_indicators):
                analysis['professional_tone'] += 1
            
            # Technical depth indicators
            technical_indicators = ['algorithm', 'architecture', 'performance', 'optimization', 'design']
            if any(indicator in message.lower() for indicator in technical_indicators):
                analysis['technical_depth'] += 1
        
        analysis['avg_response_length'] = total_length / len(user_messages) if user_messages else 0
        
        # Calculate score
        score = 5  # Base score
        
        if analysis['avg_response_length'] > 15:
            score += 2
        elif analysis['avg_response_length'] > 8:
            score += 1
        
        if analysis['detailed_responses'] > len(user_messages) * 0.6:
            score += 2
        
        if analysis['professional_tone'] > 0:
            score += 1
        
        if analysis['technical_depth'] > 0:
            score += 2
        
        return min(score, 10), analysis
    
    def calculate_role_fit_score(self, desired_position: str, tech_stack: Dict, experience: int) -> Tuple[int, Dict]:
        """Calculate how well candidate fits desired role"""
        position_lower = desired_position.lower()
        
        role_requirements = {
            'senior': {
                'min_experience': 5,
                'required_techs': ['python', 'java', 'javascript', 'react', 'django'],
                'leadership_keywords': ['lead', 'senior', 'architect', 'principal']
            },
            'full stack': {
                'min_experience': 2,
                'required_categories': ['languages', 'frameworks', 'databases'],
                'full_stack_techs': ['react', 'vue', 'angular', 'django', 'spring', 'node']
            },
            'frontend': {
                'min_experience': 1,
                'required_techs': ['javascript', 'react', 'vue', 'angular', 'typescript'],
                'bonus_techs': ['css', 'html', 'webpack', 'sass']
            },
            'backend': {
                'min_experience': 1,
                'required_techs': ['python', 'java', 'django', 'spring', 'fastapi', 'node'],
                'bonus_techs': ['postgresql', 'mongodb', 'redis', 'docker']
            },
            'devops': {
                'min_experience': 2,
                'required_techs': ['docker', 'kubernetes', 'aws', 'azure', 'terraform'],
                'bonus_techs': ['jenkins', 'ansible', 'nginx']
            }
        }
        
        fit_analysis = {
            'role_type': 'general',
            'experience_match': False,
            'tech_match_count': 0,
            'bonus_tech_count': 0,
            'seniority_match': False
        }
        
        score = 5  # Base score
        
        # Determine role type
        for role_type in role_requirements:
            if role_type in position_lower:
                fit_analysis['role_type'] = role_type
                requirements = role_requirements[role_type]
                
                # Check experience requirement
                if experience >= requirements.get('min_experience', 0):
                    fit_analysis['experience_match'] = True
                    score += 2
                
                # Check required technologies
                all_techs = [tech.lower() for techs in tech_stack.values() for tech in techs]
                
                if 'required_techs' in requirements:
                    matches = sum(1 for tech in requirements['required_techs'] if tech in all_techs)
                    fit_analysis['tech_match_count'] = matches
                    score += min(matches * 1.5, 4)
                
                if 'bonus_techs' in requirements:
                    bonus_matches = sum(1 for tech in requirements['bonus_techs'] if tech in all_techs)
                    fit_analysis['bonus_tech_count'] = bonus_matches
                    score += min(bonus_matches, 2)
                
                # Check seniority keywords
                if 'leadership_keywords' in requirements:
                    if any(keyword in position_lower for keyword in requirements['leadership_keywords']):
                        fit_analysis['seniority_match'] = experience >= 5
                        if fit_analysis['seniority_match']:
                            score += 2
                
                break
        
        return min(score, 10), fit_analysis
    
    def generate_comprehensive_score(self, candidate_data: Dict, messages: List[Dict]) -> Dict:
        """Generate comprehensive candidate score and analysis"""
        if not candidate_data:
            return {'error': 'No candidate data available'}
        
        # Extract data
        experience = int(str(candidate_data.get('experience_years', 0)))
        tech_stack = candidate_data.get('tech_stack', {})
        desired_position = candidate_data.get('desired_position', 'Developer')
        
        # Calculate individual scores
        exp_score, exp_level = self.calculate_experience_score(experience)
        breadth_score, depth_score, tech_analysis = self.calculate_tech_stack_score(tech_stack)
        comm_score, comm_analysis = self.calculate_communication_score(messages)
        fit_score, fit_analysis = self.calculate_role_fit_score(desired_position, tech_stack, experience)
        
        # Calculate weighted total score
        total_score = (
            exp_score * self.scoring_weights['experience'] +
            breadth_score * self.scoring_weights['tech_stack_breadth'] +
            depth_score * self.scoring_weights['tech_stack_depth'] +
            comm_score * self.scoring_weights['communication'] +
            fit_score * self.scoring_weights['role_fit']
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            exp_score, breadth_score, depth_score, comm_score, fit_score,
            tech_analysis, comm_analysis, fit_analysis
        )
        
        return {
            'total_score': round(total_score, 1),
            'grade': self._score_to_grade(total_score),
            'experience_level': exp_level,
            'scores': {
                'experience': exp_score,
                'tech_breadth': breadth_score,
                'tech_depth': depth_score,
                'communication': comm_score,
                'role_fit': fit_score
            },
            'analysis': {
                'tech_stack': tech_analysis,
                'communication': comm_analysis,
                'role_fit': fit_analysis
            },
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
    
    def _score_to_grade(self, score: float) -> str:
        """Convert numerical score to letter grade"""
        if score >= 9.0:
            return 'A+'
        elif score >= 8.5:
            return 'A'
        elif score >= 8.0:
            return 'A-'
        elif score >= 7.5:
            return 'B+'
        elif score >= 7.0:
            return 'B'
        elif score >= 6.5:
            return 'B-'
        elif score >= 6.0:
            return 'C+'
        elif score >= 5.5:
            return 'C'
        else:
            return 'C-'
    
    def _generate_recommendations(self, exp_score, breadth_score, depth_score, 
                                comm_score, fit_score, tech_analysis, 
                                comm_analysis, fit_analysis) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if exp_score >= 8:
            recommendations.append("✅ Strong experience level - excellent for senior roles")
        elif exp_score < 6:
            recommendations.append("💡 Consider junior or mid-level positions to build experience")
        
        if tech_analysis['modern_stack']:
            recommendations.append("✅ Modern tech stack - great for current market demands")
        else:
            recommendations.append("💡 Consider learning modern technologies (React, Python, Docker)")
        
        if tech_analysis['full_stack']:
            recommendations.append("✅ Full-stack capabilities - versatile for many roles")
        
        if comm_score < 6:
            recommendations.append("💡 Encourage more detailed technical discussions in interviews")
        
        if fit_score >= 8:
            recommendations.append("✅ Excellent fit for desired role")
        elif fit_score < 6:
            recommendations.append("💡 May need additional skills for desired role")
        
        return recommendations