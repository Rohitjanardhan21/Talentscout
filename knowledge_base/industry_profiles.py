"""
Industry-Specific Knowledge Base and Requirements
"""

INDUSTRY_PROFILES = {
    'fintech': {
        'name': 'Financial Technology',
        'key_technologies': {
            'languages': ['java', 'c#', 'python', 'scala', 'go'],
            'frameworks': ['spring boot', 'django', 'fastapi', '.net core'],
            'databases': ['postgresql', 'oracle', 'mongodb', 'redis'],
            'tools': ['kafka', 'kubernetes', 'terraform', 'jenkins']
        },
        'compliance_requirements': ['PCI DSS', 'SOX', 'GDPR', 'PSD2'],
        'critical_skills': [
            'Security-first development',
            'High-frequency trading systems',
            'Payment processing',
            'Risk management systems',
            'Regulatory compliance',
            'Real-time data processing'
        ],
        'common_challenges': [
            'Ultra-low latency requirements',
            'Regulatory compliance',
            'Data security and privacy',
            'High availability (99.99%+)',
            'Fraud detection and prevention'
        ]
    },
    
    'healthcare': {
        'name': 'Healthcare Technology',
        'key_technologies': {
            'languages': ['java', 'c#', 'python', 'javascript'],
            'frameworks': ['spring', 'django', 'react', 'angular'],
            'databases': ['postgresql', 'mongodb', 'sql server'],
            'tools': ['docker', 'kubernetes', 'aws', 'azure']
        },
        'compliance_requirements': ['HIPAA', 'HITECH', 'FDA', 'GDPR'],
        'critical_skills': [
            'HIPAA compliance development',
            'Medical device integration',
            'Electronic Health Records (EHR)',
            'Telemedicine platforms',
            'Medical imaging systems',
            'Clinical decision support'
        ],
        'common_challenges': [
            'Patient data privacy',
            'Interoperability standards (HL7, FHIR)',
            'Medical device regulations',
            'Clinical workflow integration',
            'Data accuracy and reliability'
        ]
    },
    
    'ecommerce': {
        'name': 'E-commerce',
        'key_technologies': {
            'languages': ['javascript', 'python', 'java', 'php'],
            'frameworks': ['react', 'vue', 'django', 'laravel', 'magento'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'elasticsearch'],
            'tools': ['docker', 'kubernetes', 'aws', 'redis', 'cdn']
        },
        'compliance_requirements': ['PCI DSS', 'GDPR', 'CCPA'],
        'critical_skills': [
            'High-traffic system design',
            'Payment gateway integration',
            'Inventory management',
            'Recommendation engines',
            'Search optimization',
            'Mobile commerce'
        ],
        'common_challenges': [
            'Peak traffic handling (Black Friday)',
            'Payment security',
            'Inventory synchronization',
            'Personalization at scale',
            'Multi-channel integration'
        ]
    },
    
    'gaming': {
        'name': 'Gaming Industry',
        'key_technologies': {
            'languages': ['c++', 'c#', 'javascript', 'python', 'lua'],
            'frameworks': ['unity', 'unreal engine', 'react native', 'flutter'],
            'databases': ['redis', 'mongodb', 'postgresql'],
            'tools': ['docker', 'kubernetes', 'aws', 'playfab', 'photon']
        },
        'compliance_requirements': ['COPPA', 'GDPR', 'Platform Guidelines'],
        'critical_skills': [
            'Real-time multiplayer systems',
            'Game engine development',
            'Performance optimization',
            'Anti-cheat systems',
            'Monetization systems',
            'Cross-platform development'
        ],
        'common_challenges': [
            'Low-latency networking',
            'Cheating and security',
            'Scalable matchmaking',
            'Platform certification',
            'Performance on various devices'
        ]
    },
    
    'enterprise_saas': {
        'name': 'Enterprise SaaS',
        'key_technologies': {
            'languages': ['java', 'python', 'javascript', 'go', 'c#'],
            'frameworks': ['spring boot', 'django', 'react', 'angular', 'vue'],
            'databases': ['postgresql', 'mysql', 'mongodb', 'redis'],
            'tools': ['kubernetes', 'docker', 'terraform', 'jenkins', 'aws']
        },
        'compliance_requirements': ['SOC 2', 'GDPR', 'HIPAA', 'ISO 27001'],
        'critical_skills': [
            'Multi-tenant architecture',
            'Enterprise integrations',
            'API design and management',
            'Security and compliance',
            'Scalable infrastructure',
            'Business intelligence'
        ],
        'common_challenges': [
            'Multi-tenancy isolation',
            'Enterprise-grade security',
            'Complex integrations',
            'Compliance requirements',
            'Global scalability'
        ]
    },
    
    'media_streaming': {
        'name': 'Media & Streaming',
        'key_technologies': {
            'languages': ['javascript', 'python', 'go', 'rust', 'c++'],
            'frameworks': ['react', 'vue', 'django', 'fastapi', 'express'],
            'databases': ['postgresql', 'mongodb', 'redis', 'cassandra'],
            'tools': ['ffmpeg', 'aws', 'cdn', 'kubernetes', 'docker']
        },
        'compliance_requirements': ['DMCA', 'GDPR', 'Content Licensing'],
        'critical_skills': [
            'Video streaming protocols',
            'Content delivery networks',
            'Real-time processing',
            'Recommendation algorithms',
            'DRM and content protection',
            'Global content distribution'
        ],
        'common_challenges': [
            'Global content delivery',
            'Video encoding optimization',
            'Real-time streaming',
            'Content recommendation',
            'Bandwidth optimization'
        ]
    }
}

ROLE_SPECIFIC_REQUIREMENTS = {
    'frontend_developer': {
        'must_have': ['html', 'css', 'javascript'],
        'preferred': ['react', 'vue', 'angular', 'typescript'],
        'bonus': ['webpack', 'sass', 'testing frameworks'],
        'focus_areas': ['UI/UX implementation', 'Performance optimization', 'Cross-browser compatibility']
    },
    
    'backend_developer': {
        'must_have': ['server-side language', 'databases', 'apis'],
        'preferred': ['python', 'java', 'node.js', 'postgresql', 'mongodb'],
        'bonus': ['microservices', 'caching', 'message queues'],
        'focus_areas': ['API design', 'Database optimization', 'System architecture']
    },
    
    'full_stack_developer': {
        'must_have': ['frontend tech', 'backend tech', 'databases'],
        'preferred': ['react/vue', 'python/node.js', 'postgresql/mongodb'],
        'bonus': ['devops', 'cloud platforms', 'testing'],
        'focus_areas': ['End-to-end development', 'System integration', 'Technology versatility']
    },
    
    'devops_engineer': {
        'must_have': ['linux', 'scripting', 'ci/cd'],
        'preferred': ['docker', 'kubernetes', 'terraform', 'aws/azure'],
        'bonus': ['monitoring', 'security', 'automation'],
        'focus_areas': ['Infrastructure automation', 'Deployment pipelines', 'System reliability']
    },
    
    'data_engineer': {
        'must_have': ['python/scala', 'sql', 'data pipelines'],
        'preferred': ['spark', 'kafka', 'airflow', 'cloud platforms'],
        'bonus': ['machine learning', 'streaming', 'data warehousing'],
        'focus_areas': ['Data pipeline design', 'ETL processes', 'Big data technologies']
    },
    
    'mobile_developer': {
        'must_have': ['mobile platform', 'mobile frameworks'],
        'preferred': ['react native', 'flutter', 'swift', 'kotlin'],
        'bonus': ['app store optimization', 'performance', 'testing'],
        'focus_areas': ['Mobile UI/UX', 'Platform-specific features', 'Performance optimization']
    }
}

def get_industry_profile(industry: str):
    """Get comprehensive industry profile"""
    return INDUSTRY_PROFILES.get(industry.lower().replace(' ', '_'), None)

def get_role_requirements(role: str):
    """Get role-specific requirements"""
    role_key = role.lower().replace(' ', '_').replace('-', '_')
    return ROLE_SPECIFIC_REQUIREMENTS.get(role_key, None)

def calculate_industry_fit_score(candidate_tech_stack: dict, industry: str) -> dict:
    """Calculate how well candidate fits industry requirements"""
    industry_profile = get_industry_profile(industry)
    if not industry_profile:
        return {'score': 0, 'analysis': 'Industry not found'}
    
    candidate_techs = set()
    for category, techs in candidate_tech_stack.items():
        candidate_techs.update([tech.lower() for tech in techs])
    
    industry_techs = set()
    for category, techs in industry_profile['key_technologies'].items():
        industry_techs.update(techs)
    
    # Calculate overlap
    overlap = candidate_techs.intersection(industry_techs)
    fit_percentage = len(overlap) / len(industry_techs) * 100 if industry_techs else 0
    
    # Score based on fit percentage
    if fit_percentage >= 70:
        score = 10
        level = 'Excellent'
    elif fit_percentage >= 50:
        score = 8
        level = 'Good'
    elif fit_percentage >= 30:
        score = 6
        level = 'Fair'
    else:
        score = 4
        level = 'Limited'
    
    return {
        'score': score,
        'fit_percentage': round(fit_percentage, 1),
        'level': level,
        'matching_technologies': list(overlap),
        'missing_technologies': list(industry_techs - candidate_techs),
        'industry_challenges': industry_profile['common_challenges'],
        'compliance_requirements': industry_profile['compliance_requirements']
    }