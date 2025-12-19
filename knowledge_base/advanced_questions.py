"""
Advanced Question Bank with Multiple Difficulty Levels and Categories
"""

ADVANCED_QUESTION_BANK = {
    # Programming Languages - Detailed Questions by Experience Level
    'python': {
        'junior': [
            "What's the difference between a list and a tuple in Python? When would you use each?",
            "Can you explain what Python's 'self' parameter does in class methods?",
            "How do you handle exceptions in Python? Give me an example.",
            "What are Python's basic data types and how do you convert between them?",
            "Explain what a Python function is and how to define one with parameters."
        ],
        'mid': [
            "How do Python decorators work? Can you create a simple logging decorator?",
            "What's the difference between deep copy and shallow copy in Python?",
            "Explain Python's Global Interpreter Lock (GIL) and its implications.",
            "How do you work with Python's *args and **kwargs? Give practical examples.",
            "What are Python generators and when would you use them over regular functions?"
        ],
        'senior': [
            "How does Python's memory management and garbage collection work?",
            "Explain metaclasses in Python and provide a use case where they're beneficial.",
            "How would you optimize Python code for performance? What tools would you use?",
            "Describe Python's descriptor protocol and how properties work internally.",
            "How do you implement thread-safe code in Python given the GIL limitations?"
        ],
        'architect': [
            "How would you design a Python microservices architecture for high scalability?",
            "Explain your approach to Python code organization in large enterprise applications.",
            "How do you handle Python dependency management and virtual environments in production?",
            "What strategies do you use for Python application monitoring and debugging in production?",
            "How would you implement a custom Python framework or library for your team?"
        ]
    },
    
    'javascript': {
        'junior': [
            "What's the difference between '==' and '===' in JavaScript?",
            "How do you declare variables in JavaScript? What's the difference between var, let, and const?",
            "What are JavaScript functions and how do you call them?",
            "How do you work with arrays in JavaScript? Show me basic operations.",
            "What's the difference between null and undefined in JavaScript?"
        ],
        'mid': [
            "Explain JavaScript closures with a practical example.",
            "How does the JavaScript event loop work? What are callbacks?",
            "What are Promises in JavaScript and how do they differ from callbacks?",
            "Explain 'this' keyword behavior in different contexts in JavaScript.",
            "How do you handle asynchronous operations with async/await?"
        ],
        'senior': [
            "How does JavaScript's prototypal inheritance work compared to classical inheritance?",
            "Explain the JavaScript module system (CommonJS vs ES6 modules).",
            "How would you optimize JavaScript performance in a large application?",
            "What are Web Workers and when would you use them?",
            "How do you implement proper error handling in complex JavaScript applications?"
        ],
        'architect': [
            "How would you architect a large-scale JavaScript application for maintainability?",
            "What's your approach to JavaScript bundling and code splitting strategies?",
            "How do you implement micro-frontends with JavaScript?",
            "What are your strategies for JavaScript testing at scale (unit, integration, e2e)?",
            "How do you handle JavaScript performance monitoring and optimization in production?"
        ]
    },
    
    # Frameworks - React Example
    'react': {
        'junior': [
            "What is React and why would you use it over vanilla JavaScript?",
            "What's the difference between functional and class components in React?",
            "How do you handle user input in React forms?",
            "What are props in React and how do you pass data between components?",
            "How do you conditionally render elements in React?"
        ],
        'mid': [
            "What are React Hooks and why were they introduced? Explain useState and useEffect.",
            "How does React's Virtual DOM work and why is it beneficial?",
            "What's the purpose of keys in React lists and what happens if you don't use them?",
            "How do you manage state in a React application? Compare local state vs context.",
            "Explain React's component lifecycle methods and their Hook equivalents."
        ],
        'senior': [
            "How would you optimize React performance? Discuss memoization, lazy loading, and code splitting.",
            "What are React patterns like Higher-Order Components and Render Props?",
            "How do you implement error boundaries in React applications?",
            "Explain React's reconciliation algorithm and how it determines what to re-render.",
            "How do you handle complex state management in large React applications?"
        ],
        'architect': [
            "How would you structure a large-scale React application for multiple teams?",
            "What's your approach to React component library design and maintenance?",
            "How do you implement micro-frontends with React?",
            "What are your strategies for React application testing and quality assurance?",
            "How do you handle React application deployment and performance monitoring?"
        ]
    },
    
    # System Design Questions
    'system_design': {
        'mid': [
            "How would you design a simple URL shortener like bit.ly?",
            "Design a basic chat application. What components would you need?",
            "How would you implement a simple caching system?",
            "Design a basic user authentication system.",
            "How would you structure a simple e-commerce product catalog?"
        ],
        'senior': [
            "Design a scalable social media feed system like Twitter.",
            "How would you build a distributed file storage system?",
            "Design a real-time notification system for millions of users.",
            "How would you implement a search engine for a large e-commerce site?",
            "Design a video streaming platform architecture."
        ],
        'architect': [
            "Design a global content delivery network (CDN) architecture.",
            "How would you build a distributed database system with ACID properties?",
            "Design a microservices architecture for a large enterprise application.",
            "How would you implement a real-time analytics system for big data?",
            "Design a fault-tolerant, highly available system for financial transactions."
        ]
    },
    
    # Database Questions
    'database_design': {
        'junior': [
            "What's the difference between SQL and NoSQL databases?",
            "Explain what a primary key is and why it's important.",
            "What are the basic SQL operations (CRUD)?",
            "How do you create relationships between tables?",
            "What's the difference between INNER JOIN and LEFT JOIN?"
        ],
        'mid': [
            "Explain database normalization and why it's important.",
            "What are database indexes and how do they improve performance?",
            "How do you handle database transactions and what is ACID?",
            "What's the difference between clustered and non-clustered indexes?",
            "How do you optimize slow database queries?"
        ],
        'senior': [
            "How do you design a database schema for high performance and scalability?",
            "Explain database sharding and when you would use it.",
            "What are the trade-offs between consistency and availability in distributed databases?",
            "How do you handle database migrations in production systems?",
            "What strategies do you use for database backup and disaster recovery?"
        ],
        'architect': [
            "How would you design a multi-tenant database architecture?",
            "What's your approach to database performance monitoring and optimization?",
            "How do you handle database scaling for applications with millions of users?",
            "What are your strategies for data warehousing and analytics?",
            "How do you implement database security and compliance requirements?"
        ]
    },
    
    # DevOps and Infrastructure
    'devops': {
        'junior': [
            "What is version control and why is Git important?",
            "Explain what CI/CD means and why it's useful.",
            "What's the difference between development, staging, and production environments?",
            "How do you deploy a simple web application?",
            "What is containerization and why use Docker?"
        ],
        'mid': [
            "How do you set up a CI/CD pipeline for a web application?",
            "Explain Infrastructure as Code and tools like Terraform.",
            "What's the difference between horizontal and vertical scaling?",
            "How do you monitor application performance and handle alerts?",
            "What are the benefits of using container orchestration like Kubernetes?"
        ],
        'senior': [
            "How do you design a highly available and fault-tolerant infrastructure?",
            "What's your approach to security in DevOps (DevSecOps)?",
            "How do you handle database migrations and zero-downtime deployments?",
            "What strategies do you use for disaster recovery and business continuity?",
            "How do you implement proper logging, monitoring, and observability?"
        ],
        'architect': [
            "How would you design a multi-cloud or hybrid cloud strategy?",
            "What's your approach to enterprise-scale infrastructure automation?",
            "How do you implement governance and compliance in cloud environments?",
            "What are your strategies for cost optimization in cloud infrastructure?",
            "How do you design infrastructure for global applications with low latency?"
        ]
    }
}

# Industry-Specific Questions
INDUSTRY_QUESTIONS = {
    'fintech': [
        "How do you ensure data security and compliance in financial applications?",
        "What's your experience with payment processing and PCI compliance?",
        "How do you handle high-frequency trading system requirements?",
        "What are the challenges of building real-time financial data systems?"
    ],
    'healthcare': [
        "How do you ensure HIPAA compliance in healthcare applications?",
        "What's your experience with healthcare data interoperability standards?",
        "How do you handle sensitive patient data in cloud environments?",
        "What are the challenges of building telemedicine platforms?"
    ],
    'ecommerce': [
        "How do you handle high-traffic events like Black Friday sales?",
        "What's your approach to recommendation engine implementation?",
        "How do you ensure payment security in e-commerce platforms?",
        "What strategies do you use for inventory management systems?"
    ],
    'gaming': [
        "How do you handle real-time multiplayer game synchronization?",
        "What's your experience with game engine optimization?",
        "How do you implement anti-cheat systems in online games?",
        "What are the challenges of mobile game development?"
    ]
}

# Behavioral and Soft Skills Questions
BEHAVIORAL_QUESTIONS = {
    'leadership': [
        "Tell me about a time you had to lead a technical project with tight deadlines.",
        "How do you handle disagreements within your development team?",
        "Describe a situation where you had to mentor a junior developer.",
        "How do you prioritize features when everything seems urgent?"
    ],
    'problem_solving': [
        "Walk me through your approach to debugging a complex production issue.",
        "Tell me about the most challenging technical problem you've solved.",
        "How do you approach learning a completely new technology or framework?",
        "Describe a time when you had to make a technical decision with incomplete information."
    ],
    'communication': [
        "How do you explain complex technical concepts to non-technical stakeholders?",
        "Tell me about a time you had to advocate for a technical decision to management.",
        "How do you handle code reviews and give constructive feedback?",
        "Describe your approach to technical documentation."
    ],
    'adaptability': [
        "Tell me about a time when project requirements changed significantly mid-development.",
        "How do you stay current with rapidly evolving technology trends?",
        "Describe a situation where you had to work with a technology you weren't familiar with.",
        "How do you handle working in a fast-paced, changing environment?"
    ]
}

def get_questions_by_experience_and_tech(technology: str, experience_level: str, count: int = 3):
    """Get questions based on technology and experience level"""
    if technology in ADVANCED_QUESTION_BANK:
        tech_questions = ADVANCED_QUESTION_BANK[technology]
        if experience_level in tech_questions:
            questions = tech_questions[experience_level]
            return questions[:count] if len(questions) >= count else questions
    return []

def get_system_design_questions(experience_level: str, count: int = 2):
    """Get system design questions based on experience level"""
    if experience_level in ADVANCED_QUESTION_BANK['system_design']:
        questions = ADVANCED_QUESTION_BANK['system_design'][experience_level]
        return questions[:count] if len(questions) >= count else questions
    return []

def get_industry_questions(industry: str, count: int = 2):
    """Get industry-specific questions"""
    if industry in INDUSTRY_QUESTIONS:
        questions = INDUSTRY_QUESTIONS[industry]
        return questions[:count] if len(questions) >= count else questions
    return []

def get_behavioral_questions(category: str, count: int = 2):
    """Get behavioral questions by category"""
    if category in BEHAVIORAL_QUESTIONS:
        questions = BEHAVIORAL_QUESTIONS[category]
        return questions[:count] if len(questions) >= count else questions
    return []