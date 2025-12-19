"""
Knowledge Base Analytics and Insights
"""
from typing import Dict, List, Any, Tuple
from collections import Counter
import json
from datetime import datetime

class KnowledgeBaseAnalytics:
    """Analytics for knowledge base usage and effectiveness"""
    
    def __init__(self):
        self.question_usage = Counter()
        self.technology_frequency = Counter()
        self.industry_distribution = Counter()
        self.experience_level_distribution = Counter()
        self.session_data = []
    
    def track_question_usage(self, question: str, technology: str, experience_level: str):
        """Track which questions are being used"""
        self.question_usage[f"{technology}_{experience_level}_{question[:50]}"] += 1
        self.technology_frequency[technology] += 1
        self.experience_level_distribution[experience_level] += 1
    
    def track_session(self, candidate_data: Dict[str, Any], questions_generated: Dict[str, List[str]]):
        """Track complete session data"""
        session = {
            'timestamp': datetime.now().isoformat(),
            'experience_years': candidate_data.get('experience_years', 0),
            'tech_stack': candidate_data.get('tech_stack', {}),
            'desired_position': candidate_data.get('desired_position', ''),
            'questions_count': sum(len(q) for q in questions_generated.values()),
            'technologies_covered': len(questions_generated)
        }
        self.session_data.append(session)
    
    def get_popular_technologies(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Get most popular technologies"""
        return self.technology_frequency.most_common(top_n)
    
    def get_experience_distribution(self) -> Dict[str, int]:
        """Get distribution of experience levels"""
        return dict(self.experience_level_distribution)
    
    def get_question_effectiveness_score(self, technology: str) -> float:
        """Calculate question effectiveness score for a technology"""
        tech_questions = [q for q in self.question_usage if q.startswith(technology)]
        if not tech_questions:
            return 0.0
        
        total_usage = sum(self.question_usage[q] for q in tech_questions)
        unique_questions = len(tech_questions)
        
        # Score based on usage distribution and variety
        if unique_questions == 0:
            return 0.0
        
        avg_usage = total_usage / unique_questions
        return min(avg_usage * 10, 100.0)  # Scale to 0-100
    
    def generate_knowledge_gaps_report(self) -> Dict[str, Any]:
        """Identify gaps in knowledge base"""
        gaps = {
            'underrepresented_technologies': [],
            'missing_experience_levels': [],
            'low_engagement_questions': [],
            'recommendations': []
        }
        
        # Find technologies with low question coverage
        all_techs = set(self.technology_frequency.keys())
        for tech in all_techs:
            effectiveness = self.get_question_effectiveness_score(tech)
            if effectiveness < 20:  # Low effectiveness threshold
                gaps['underrepresented_technologies'].append({
                    'technology': tech,
                    'effectiveness_score': effectiveness,
                    'usage_count': self.technology_frequency[tech]
                })
        
        # Find experience levels with low coverage
        exp_levels = ['junior', 'mid', 'senior', 'architect']
        for level in exp_levels:
            level_usage = self.experience_level_distribution.get(level, 0)
            if level_usage < 5:  # Low usage threshold
                gaps['missing_experience_levels'].append({
                    'level': level,
                    'usage_count': level_usage
                })
        
        # Generate recommendations
        if gaps['underrepresented_technologies']:
            gaps['recommendations'].append("Add more questions for underrepresented technologies")
        
        if gaps['missing_experience_levels']:
            gaps['recommendations'].append("Create questions targeting underused experience levels")
        
        return gaps
    
    def get_technology_trends(self) -> Dict[str, Any]:
        """Analyze technology trends from candidate data"""
        trends = {
            'emerging_technologies': [],
            'declining_technologies': [],
            'stable_technologies': [],
            'hot_combinations': []
        }
        
        # Analyze technology combinations
        tech_combinations = Counter()
        for session in self.session_data:
            tech_stack = session.get('tech_stack', {})
            all_techs = []
            for category, techs in tech_stack.items():
                all_techs.extend(techs)
            
            # Count combinations of 2 technologies
            for i, tech1 in enumerate(all_techs):
                for tech2 in all_techs[i+1:]:
                    combo = tuple(sorted([tech1.lower(), tech2.lower()]))
                    tech_combinations[combo] += 1
        
        # Get top combinations
        trends['hot_combinations'] = [
            {'technologies': list(combo), 'frequency': count}
            for combo, count in tech_combinations.most_common(5)
        ]
        
        return trends
    
    def generate_insights_report(self) -> Dict[str, Any]:
        """Generate comprehensive insights report"""
        total_sessions = len(self.session_data)
        
        if total_sessions == 0:
            return {'error': 'No session data available'}
        
        # Calculate averages
        avg_experience = sum(int(str(s.get('experience_years', 0))) for s in self.session_data) / total_sessions
        avg_questions = sum(s.get('questions_count', 0) for s in self.session_data) / total_sessions
        avg_techs = sum(s.get('technologies_covered', 0) for s in self.session_data) / total_sessions
        
        # Most common positions
        positions = [s.get('desired_position', '') for s in self.session_data]
        position_counter = Counter(positions)
        
        report = {
            'summary': {
                'total_sessions': total_sessions,
                'average_experience_years': round(avg_experience, 1),
                'average_questions_per_session': round(avg_questions, 1),
                'average_technologies_per_candidate': round(avg_techs, 1)
            },
            'popular_technologies': self.get_popular_technologies(10),
            'experience_distribution': self.get_experience_distribution(),
            'popular_positions': position_counter.most_common(5),
            'technology_trends': self.get_technology_trends(),
            'knowledge_gaps': self.generate_knowledge_gaps_report(),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def export_analytics_data(self) -> str:
        """Export analytics data as JSON"""
        data = {
            'question_usage': dict(self.question_usage),
            'technology_frequency': dict(self.technology_frequency),
            'industry_distribution': dict(self.industry_distribution),
            'experience_level_distribution': dict(self.experience_level_distribution),
            'session_data': self.session_data,
            'insights_report': self.generate_insights_report()
        }
        
        return json.dumps(data, indent=2, default=str)

# Global analytics instance
knowledge_analytics = KnowledgeBaseAnalytics()