"""
Real-time Market Data Integration
Provides live salary data, job market trends, and technology demand analysis
"""
import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import streamlit as st
from dataclasses import dataclass
import time

@dataclass
class MarketTrend:
    technology: str
    demand_score: float  # 0-100
    salary_range: Dict[str, int]
    growth_rate: float  # percentage
    job_count: int
    last_updated: datetime

@dataclass
class LocationData:
    city: str
    country: str
    cost_of_living_index: float
    tech_hub_score: float
    average_salary_multiplier: float

class MarketDataProvider:
    """Provides real-time market data from various sources"""
    
    def __init__(self):
        self.cache_duration = timedelta(hours=6)  # Cache data for 6 hours
        self.data_cache = {}
        
        # Simulated real-time data (in production, this would connect to real APIs)
        self.base_salary_data = {
            'python': {'min': 70000, 'max': 150000, 'median': 95000},
            'javascript': {'min': 65000, 'max': 140000, 'median': 85000},
            'react': {'min': 75000, 'max': 150000, 'median': 100000},
            'django': {'min': 80000, 'max': 140000, 'median': 105000},
            'flask': {'min': 70000, 'max': 130000, 'median': 90000},
            'mysql': {'min': 60000, 'max': 120000, 'median': 80000},
            'postgresql': {'min': 65000, 'max': 125000, 'median': 85000},
            'docker': {'min': 80000, 'max': 160000, 'median': 110000},
            'kubernetes': {'min': 90000, 'max': 180000, 'median': 125000},
            'aws': {'min': 85000, 'max': 170000, 'median': 115000},
            'azure': {'min': 80000, 'max': 165000, 'median': 110000},
            'git': {'min': 50000, 'max': 120000, 'median': 75000},
            'bootstrap': {'min': 45000, 'max': 100000, 'median': 65000}
        }
        
        self.demand_trends = {
            'python': {'demand': 95, 'growth': 15.2, 'jobs': 45000},
            'javascript': {'demand': 98, 'growth': 12.8, 'jobs': 52000},
            'react': {'demand': 92, 'growth': 18.5, 'jobs': 38000},
            'django': {'demand': 78, 'growth': 8.3, 'jobs': 12000},
            'flask': {'demand': 65, 'growth': 5.2, 'jobs': 8500},
            'mysql': {'demand': 85, 'growth': 3.1, 'jobs': 25000},
            'postgresql': {'demand': 88, 'growth': 12.4, 'jobs': 18000},
            'docker': {'demand': 89, 'growth': 22.1, 'jobs': 28000},
            'kubernetes': {'demand': 85, 'growth': 35.7, 'jobs': 15000},
            'aws': {'demand': 94, 'growth': 20.3, 'jobs': 42000},
            'azure': {'demand': 87, 'growth': 25.1, 'jobs': 32000},
            'git': {'demand': 99, 'growth': 2.1, 'jobs': 48000},
            'bootstrap': {'demand': 72, 'growth': -2.3, 'jobs': 15000}
        }
        
        self.location_data = {
            'san francisco': LocationData('San Francisco', 'USA', 1.8, 0.95, 1.4),
            'new york': LocationData('New York', 'USA', 1.6, 0.85, 1.3),
            'seattle': LocationData('Seattle', 'USA', 1.4, 0.90, 1.25),
            'london': LocationData('London', 'UK', 1.3, 0.80, 1.15),
            'berlin': LocationData('Berlin', 'Germany', 1.0, 0.75, 0.95),
            'toronto': LocationData('Toronto', 'Canada', 1.1, 0.70, 1.05),
            'bangalore': LocationData('Bangalore', 'India', 0.3, 0.85, 0.25),
            'remote': LocationData('Remote', 'Global', 1.0, 0.80, 1.1)
        }
    
    def get_technology_market_data(self, technology: str) -> Optional[MarketTrend]:
        """Get real-time market data for a specific technology"""
        
        cache_key = f"market_{technology.lower()}"
        
        # Check cache first
        if cache_key in self.data_cache:
            cached_data, timestamp = self.data_cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                return cached_data
        
        # Simulate API call delay
        time.sleep(0.1)
        
        tech_lower = technology.lower()
        
        if tech_lower not in self.base_salary_data:
            return None
        
        # Add some realistic variation to simulate real-time data
        import random
        variation = random.uniform(0.95, 1.05)
        
        salary_data = self.base_salary_data[tech_lower]
        demand_data = self.demand_trends.get(tech_lower, {'demand': 50, 'growth': 0, 'jobs': 1000})
        
        market_trend = MarketTrend(
            technology=technology,
            demand_score=min(100, demand_data['demand'] * variation),
            salary_range={
                'min': int(salary_data['min'] * variation),
                'max': int(salary_data['max'] * variation),
                'median': int(salary_data['median'] * variation)
            },
            growth_rate=demand_data['growth'] * variation,
            job_count=int(demand_data['jobs'] * variation),
            last_updated=datetime.now()
        )
        
        # Cache the result
        self.data_cache[cache_key] = (market_trend, datetime.now())
        
        return market_trend
    
    def get_tech_stack_market_analysis(self, tech_stack: Dict[str, List[str]]) -> Dict[str, Any]:
        """Analyze market data for an entire tech stack"""
        
        all_technologies = []
        for category, technologies in tech_stack.items():
            all_technologies.extend(technologies)
        
        market_data = {}
        total_demand = 0
        total_jobs = 0
        salary_ranges = []
        growth_rates = []
        
        for tech in all_technologies:
            trend = self.get_technology_market_data(tech)
            if trend:
                market_data[tech] = trend
                total_demand += trend.demand_score
                total_jobs += trend.job_count
                salary_ranges.append(trend.salary_range['median'])
                growth_rates.append(trend.growth_rate)
        
        if not market_data:
            return {}
        
        # Calculate aggregate metrics
        avg_demand = total_demand / len(market_data)
        avg_growth = sum(growth_rates) / len(growth_rates)
        estimated_salary = sum(salary_ranges) / len(salary_ranges)
        
        # Determine market strength
        if avg_demand >= 90:
            market_strength = 'Excellent'
        elif avg_demand >= 80:
            market_strength = 'Strong'
        elif avg_demand >= 70:
            market_strength = 'Good'
        elif avg_demand >= 60:
            market_strength = 'Moderate'
        else:
            market_strength = 'Developing'
        
        # Generate insights
        insights = []
        
        high_demand_techs = [tech for tech, data in market_data.items() 
                           if data.demand_score >= 90]
        if high_demand_techs:
            insights.append(f"High-demand technologies: {', '.join(high_demand_techs)}")
        
        growing_techs = [tech for tech, data in market_data.items() 
                        if data.growth_rate >= 15]
        if growing_techs:
            insights.append(f"Fast-growing technologies: {', '.join(growing_techs)}")
        
        if avg_growth > 15:
            insights.append("Your tech stack is in high-growth areas")
        elif avg_growth < 5:
            insights.append("Consider adding emerging technologies to your stack")
        
        return {
            'market_strength': market_strength,
            'average_demand_score': round(avg_demand, 1),
            'estimated_salary_range': {
                'min': int(min(salary_ranges) * 0.9),
                'max': int(max(salary_ranges) * 1.1),
                'median': int(estimated_salary)
            },
            'average_growth_rate': round(avg_growth, 1),
            'total_job_opportunities': total_jobs,
            'technology_breakdown': market_data,
            'market_insights': insights,
            'last_updated': datetime.now().isoformat()
        }
    
    def get_location_adjusted_salary(self, 
                                   base_salary: int, 
                                   location: str) -> Dict[str, Any]:
        """Adjust salary based on location data"""
        
        location_lower = location.lower()
        
        # Find matching location
        location_info = None
        for loc_key, loc_data in self.location_data.items():
            if loc_key in location_lower or location_lower in loc_key:
                location_info = loc_data
                break
        
        if not location_info:
            # Default to moderate adjustment for unknown locations
            location_info = LocationData(location, 'Unknown', 1.0, 0.5, 1.0)
        
        adjusted_salary = int(base_salary * location_info.average_salary_multiplier)
        
        return {
            'base_salary': base_salary,
            'adjusted_salary': adjusted_salary,
            'location': location_info.city,
            'country': location_info.country,
            'cost_of_living_index': location_info.cost_of_living_index,
            'tech_hub_score': location_info.tech_hub_score,
            'salary_multiplier': location_info.average_salary_multiplier
        }
    
    def get_career_progression_data(self, 
                                  current_tech_stack: List[str],
                                  experience_years: int) -> Dict[str, Any]:
        """Get career progression recommendations based on market data"""
        
        # Define career progression paths
        progression_paths = {
            'full_stack_web': {
                'technologies': ['javascript', 'react', 'python', 'django', 'postgresql'],
                'next_level': ['docker', 'kubernetes', 'aws', 'redis'],
                'career_titles': ['Full Stack Developer', 'Senior Developer', 'Tech Lead']
            },
            'backend_specialist': {
                'technologies': ['python', 'django', 'flask', 'postgresql', 'mysql'],
                'next_level': ['microservices', 'kafka', 'elasticsearch', 'redis'],
                'career_titles': ['Backend Developer', 'Senior Backend Engineer', 'Principal Engineer']
            },
            'frontend_specialist': {
                'technologies': ['javascript', 'react', 'vue', 'angular', 'typescript'],
                'next_level': ['next.js', 'webpack', 'testing', 'accessibility'],
                'career_titles': ['Frontend Developer', 'Senior Frontend Engineer', 'UI/UX Engineer']
            },
            'devops_engineer': {
                'technologies': ['docker', 'kubernetes', 'aws', 'terraform', 'jenkins'],
                'next_level': ['helm', 'istio', 'prometheus', 'grafana'],
                'career_titles': ['DevOps Engineer', 'Senior DevOps Engineer', 'Platform Engineer']
            }
        }
        
        current_stack_lower = [tech.lower() for tech in current_tech_stack]
        
        # Find best matching path
        best_path = None
        best_score = 0
        
        for path_name, path_data in progression_paths.items():
            score = sum(1 for tech in path_data['technologies'] if tech in current_stack_lower)
            if score > best_score:
                best_score = score
                best_path = (path_name, path_data)
        
        if not best_path:
            return {}
        
        path_name, path_data = best_path
        
        # Get market data for recommended technologies
        recommended_techs = []
        for tech in path_data['next_level']:
            market_data = self.get_technology_market_data(tech)
            if market_data:
                recommended_techs.append({
                    'technology': tech,
                    'demand_score': market_data.demand_score,
                    'growth_rate': market_data.growth_rate,
                    'salary_impact': market_data.salary_range['median']
                })
        
        # Sort by demand and growth
        recommended_techs.sort(key=lambda x: x['demand_score'] + x['growth_rate'], reverse=True)
        
        # Determine career level based on experience
        if experience_years < 2:
            career_level = 0
        elif experience_years < 5:
            career_level = 1
        else:
            career_level = 2
        
        current_title = path_data['career_titles'][min(career_level, len(path_data['career_titles']) - 1)]
        next_title = path_data['career_titles'][min(career_level + 1, len(path_data['career_titles']) - 1)]
        
        return {
            'career_path': path_name.replace('_', ' ').title(),
            'current_title': current_title,
            'next_title': next_title,
            'path_match_score': best_score / len(path_data['technologies']),
            'recommended_technologies': recommended_techs[:5],
            'timeline_estimate': f"{max(1, 3 - experience_years)} years to next level",
            'market_outlook': 'Strong' if sum(t['demand_score'] for t in recommended_techs[:3]) / 3 > 80 else 'Moderate'
        }

class RealTimeMarketIntegration:
    """Main class for real-time market data integration"""
    
    def __init__(self):
        self.market_provider = MarketDataProvider()
        self.update_frequency = timedelta(hours=1)
        self.last_update = {}
    
    def get_comprehensive_market_analysis(self, 
                                        candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive market analysis for a candidate"""
        
        tech_stack = candidate_data.get('tech_stack', {})
        experience_years = int(str(candidate_data.get('experience_years', 3)))
        location = candidate_data.get('location', 'Remote')
        
        # Get tech stack market analysis
        market_analysis = self.market_provider.get_tech_stack_market_analysis(tech_stack)
        
        if not market_analysis:
            return {}
        
        # Get location-adjusted salary
        base_salary = market_analysis['estimated_salary_range']['median']
        location_data = self.market_provider.get_location_adjusted_salary(base_salary, location)
        
        # Get career progression data
        all_technologies = []
        for technologies in tech_stack.values():
            all_technologies.extend(technologies)
        
        career_data = self.market_provider.get_career_progression_data(
            all_technologies, experience_years
        )
        
        # Generate market recommendations
        recommendations = self._generate_market_recommendations(
            market_analysis, career_data, experience_years
        )
        
        return {
            'market_analysis': market_analysis,
            'location_data': location_data,
            'career_progression': career_data,
            'recommendations': recommendations,
            'market_summary': self._generate_market_summary(market_analysis, location_data),
            'last_updated': datetime.now().isoformat()
        }
    
    def _generate_market_recommendations(self, 
                                       market_analysis: Dict[str, Any],
                                       career_data: Dict[str, Any],
                                       experience_years: int) -> List[str]:
        """Generate actionable market-based recommendations"""
        
        recommendations = []
        
        # Market strength recommendations
        market_strength = market_analysis.get('market_strength', 'Moderate')
        if market_strength == 'Excellent':
            recommendations.append("🚀 Your tech stack is in extremely high demand - great time to explore new opportunities")
        elif market_strength == 'Developing':
            recommendations.append("📈 Consider adding high-demand technologies to strengthen your market position")
        
        # Growth rate recommendations
        avg_growth = market_analysis.get('average_growth_rate', 0)
        if avg_growth > 20:
            recommendations.append("🔥 Your technologies are experiencing rapid growth - excellent for career advancement")
        elif avg_growth < 5:
            recommendations.append("💡 Consider learning emerging technologies with higher growth rates")
        
        # Career progression recommendations
        if career_data and career_data.get('recommended_technologies'):
            top_tech = career_data['recommended_technologies'][0]['technology']
            recommendations.append(f"🎯 Consider learning {top_tech} to advance in your career path")
        
        # Experience-based recommendations
        if experience_years < 2:
            recommendations.append("📚 Focus on building strong fundamentals in your current tech stack")
        elif experience_years >= 5:
            recommendations.append("👥 Consider leadership roles or specialized expertise in high-demand areas")
        
        return recommendations
    
    def _generate_market_summary(self, 
                               market_analysis: Dict[str, Any],
                               location_data: Dict[str, Any]) -> str:
        """Generate a concise market summary"""
        
        market_strength = market_analysis.get('market_strength', 'Moderate')
        avg_demand = market_analysis.get('average_demand_score', 0)
        adjusted_salary = location_data.get('adjusted_salary', 0)
        location = location_data.get('location', 'Unknown')
        
        return f"Market Outlook: {market_strength} demand ({avg_demand:.0f}/100) • " \
               f"Est. Salary: ${adjusted_salary:,} in {location} • " \
               f"Growth Rate: {market_analysis.get('average_growth_rate', 0):.1f}%"
    
    def render_market_dashboard(self, market_data: Dict[str, Any]):
        """Render real-time market data dashboard in Streamlit"""
        
        if not market_data:
            st.info("💡 Market data will appear after tech stack collection")
            return
        
        st.markdown("### 📊 Real-Time Market Analysis")
        
        market_analysis = market_data.get('market_analysis', {})
        location_data = market_data.get('location_data', {})
        career_data = market_data.get('career_progression', {})
        
        # Market metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Market Strength", 
                market_analysis.get('market_strength', 'N/A'),
                help="Overall demand for your tech stack"
            )
        
        with col2:
            demand_score = market_analysis.get('average_demand_score', 0)
            st.metric(
                "Demand Score", 
                f"{demand_score:.0f}/100",
                help="Average demand across your technologies"
            )
        
        with col3:
            adjusted_salary = location_data.get('adjusted_salary', 0)
            st.metric(
                "Est. Salary", 
                f"${adjusted_salary:,}",
                help="Location-adjusted salary estimate"
            )
        
        with col4:
            growth_rate = market_analysis.get('average_growth_rate', 0)
            st.metric(
                "Growth Rate", 
                f"{growth_rate:.1f}%",
                delta=f"{growth_rate:.1f}%",
                help="Average growth rate of your technologies"
            )
        
        # Technology breakdown
        if 'technology_breakdown' in market_analysis:
            st.markdown("#### 🔧 Technology Market Data")
            
            tech_data = []
            for tech, trend in market_analysis['technology_breakdown'].items():
                tech_data.append({
                    'Technology': tech,
                    'Demand': f"{trend.demand_score:.0f}/100",
                    'Growth': f"{trend.growth_rate:.1f}%",
                    'Jobs': f"{trend.job_count:,}",
                    'Salary Range': f"${trend.salary_range['min']:,} - ${trend.salary_range['max']:,}"
                })
            
            st.dataframe(tech_data, use_container_width=True)
        
        # Career progression
        if career_data:
            st.markdown("#### 🚀 Career Progression")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Current Path:** {career_data.get('career_path', 'N/A')}")
                st.write(f"**Current Level:** {career_data.get('current_title', 'N/A')}")
                st.write(f"**Next Level:** {career_data.get('next_title', 'N/A')}")
            
            with col2:
                if career_data.get('recommended_technologies'):
                    st.write("**Recommended Technologies:**")
                    for tech_rec in career_data['recommended_technologies'][:3]:
                        st.write(f"• {tech_rec['technology'].title()} (Demand: {tech_rec['demand_score']:.0f})")
        
        # Market insights
        insights = market_analysis.get('market_insights', [])
        if insights:
            st.markdown("#### 💡 Market Insights")
            for insight in insights:
                st.write(f"• {insight}")
        
        # Recommendations
        recommendations = market_data.get('recommendations', [])
        if recommendations:
            st.markdown("#### 🎯 Recommendations")
            for rec in recommendations:
                st.write(f"{rec}")
        
        # Last updated
        last_updated = market_data.get('last_updated', '')
        if last_updated:
            st.caption(f"Last updated: {last_updated}")

# Global instance
market_integration = RealTimeMarketIntegration()