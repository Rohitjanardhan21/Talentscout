"""
Technical question generation based on candidate's tech stack
"""
from typing import Dict, List, Any
import random

class TechnicalQuestionGenerator:
    """Generates technical questions based on candidate's tech stack"""
    
    def __init__(self):
        self.question_bank = {
            # Programming Languages
            'python': [
                "I'm curious about your Python experience - can you walk me through the difference between lists and tuples? When do you choose one over the other?",
                "Have you worked with Python decorators? I'd love to hear about a time you used one or how you'd explain them to someone new.",
                "What's your take on Python's memory management? Have you ever had to think about garbage collection in your projects?",
                "Tell me about generators in Python - have you used them in any real projects? What made you choose them over regular functions?",
                "I love Python's flexibility - what do you think about duck typing? Any interesting examples from your work?",
                "How do you handle exception handling in Python? Any best practices you follow?",
                "What's your experience with Python's asyncio? When would you choose it over threading?",
                "Tell me about Python's GIL (Global Interpreter Lock) - how does it affect your code design?",
                "What are context managers in Python and when do you use them?",
                "How do you approach testing in Python? Any favorite testing frameworks?",
                "Explain Python's metaclasses - have you ever needed to create custom ones?",
                "How do you optimize Python code for performance? Any profiling tools you use?",
                "What's your experience with Python's descriptor protocol?",
                "How do you handle memory leaks in long-running Python applications?",
                "Explain the difference between deep copy and shallow copy in Python.",
                "What's your approach to implementing design patterns in Python?",
                "How do you handle concurrent programming in Python beyond asyncio?",
                "What's your experience with Python's import system and package management?",
                "How do you implement caching strategies in Python applications?",
                "What are your thoughts on type hints and static analysis in Python?"
            ],
            'javascript': [
                "JavaScript can be tricky with comparisons - how do you handle the difference between == and ===? Any gotchas you've run into?",
                "Closures are such a cool JavaScript feature! Can you share an example of when you've used them or how you'd explain them?",
                "The event loop is fascinating - how would you explain how JavaScript handles asynchronous operations to someone learning the language?",
                "What's your experience with JavaScript's prototypal inheritance? How does it compare to class-based inheritance you might know from other languages?",
                "I'm curious about your async JavaScript experience - do you prefer Promises, async/await, or callbacks? What's driven those choices in your projects?"
            ],
            'java': [
                "Explain the difference between abstract classes and interfaces in Java.",
                "What is the Java Virtual Machine (JVM) and how does it work?",
                "Describe the concept of multithreading in Java.",
                "What are Java Streams and how do they improve code readability?",
                "Explain the principles of Object-Oriented Programming in Java."
            ],
            'c++': [
                "What is the difference between stack and heap memory in C++?",
                "Explain RAII (Resource Acquisition Is Initialization) in C++.",
                "What are smart pointers and why are they important?",
                "Describe the concept of virtual functions in C++.",
                "What is the difference between pass by value and pass by reference?"
            ],
            'c#': [
                "What is the difference between value types and reference types in C#?",
                "Explain LINQ and provide an example of its usage.",
                "What are delegates and events in C#?",
                "Describe the concept of async/await in C#.",
                "What is the Global Assembly Cache (GAC) in .NET?"
            ],
            
            # Frameworks
            'react': [
                "React's Virtual DOM is pretty clever - how would you explain its performance benefits to someone who's new to React?",
                "I see you work with React! Do you prefer functional components or class components? What's influenced that choice in your projects?",
                "React Hooks really changed the game - what's your experience with them? Any favorites or ones you find particularly useful?",
                "State management can get complex in React apps - how do you typically handle it? Any patterns or libraries you swear by?",
                "Here's a fun one - why do you think React needs keys in lists? Have you ever run into issues when they're missing?",
                "How do you handle side effects in React? What's your approach with useEffect?",
                "What's your experience with React performance optimization? Any techniques you use regularly?",
                "How do you approach component composition in React? Any patterns you find particularly useful?",
                "What's your take on React Context vs external state management libraries?",
                "How do you handle forms in React? Any libraries or patterns you prefer?",
                "Explain React's reconciliation algorithm and how it affects rendering performance.",
                "How do you implement custom React hooks for complex business logic?",
                "What's your experience with React's Concurrent Mode and Suspense?",
                "How do you handle code splitting and lazy loading in React applications?",
                "What's your approach to testing React components? Unit vs integration testing?",
                "How do you implement error boundaries in React applications?",
                "What's your experience with React's new server components?",
                "How do you handle React application performance at scale?",
                "What's your approach to React component styling? CSS-in-JS vs traditional CSS?",
                "How do you implement accessibility (a11y) in React applications?"
            ],
            'django': [
                "Django's MTV architecture is interesting - how would you explain it compared to traditional MVC?",
                "What's your experience with Django ORM? Any complex queries you've had to optimize?",
                "How do you handle user authentication and authorization in Django projects?",
                "Tell me about Django middlewares - have you written custom ones? What for?",
                "Django's migration system is powerful - any tricky migration scenarios you've handled?",
                "What's your approach to Django project structure for larger applications?",
                "How do you handle API development in Django? DRF or something else?",
                "What's your experience with Django's caching framework?",
                "How do you approach testing in Django applications?",
                "What are your thoughts on Django's admin interface? Do you customize it much?"
            ],
            'flask': [
                "Flask is quite minimalist compared to Django - what draws you to it for certain projects?",
                "How do you structure larger Flask applications? Any patterns you follow?",
                "What's your experience with Flask extensions? Any must-haves in your toolkit?",
                "How do you handle database operations in Flask? SQLAlchemy or something else?",
                "What's your approach to authentication and authorization in Flask?",
                "How do you handle configuration management in Flask applications?",
                "What's your experience with Flask blueprints for organizing code?",
                "How do you approach API development with Flask? Any frameworks you layer on top?",
                "What's your strategy for error handling and logging in Flask apps?",
                "How do you handle deployment and scaling of Flask applications?"
            ],
            'angular': [
                "What is dependency injection in Angular?",
                "Explain the difference between components and directives.",
                "What are Angular services and how do you create them?",
                "How does data binding work in Angular?",
                "What is the Angular CLI and what are its main features?"
            ],
            'spring': [
                "What is Inversion of Control (IoC) in Spring?",
                "Explain the concept of Aspect-Oriented Programming (AOP).",
                "What are Spring Boot's auto-configuration features?",
                "How does Spring handle transaction management?",
                "What is the difference between @Component, @Service, and @Repository?"
            ],
            
            # Databases
            'mysql': [
                "What's your experience with different types of JOINs in MySQL? Any performance considerations you keep in mind?",
                "How do you approach database design and normalization in your projects?",
                "Tell me about your experience with MySQL indexing - any optimization stories?",
                "What's your process for debugging slow MySQL queries? Any tools you rely on?",
                "How do you handle database migrations and schema changes in production?",
                "What's your experience with MySQL replication or clustering?",
                "How do you approach backup and recovery strategies for MySQL?",
                "What are your thoughts on stored procedures vs application-level logic?",
                "How do you handle database security and user permissions in MySQL?",
                "What's your experience with MySQL performance tuning and configuration?"
            ],
            'postgresql': [
                "What are PostgreSQL's advanced data types?",
                "Explain the concept of MVCC (Multi-Version Concurrency Control).",
                "What are PostgreSQL extensions and name a few useful ones?",
                "How do you handle full-text search in PostgreSQL?",
                "What is the difference between PostgreSQL and MySQL?"
            ],
            'mongodb': [
                "What is the difference between SQL and NoSQL databases?",
                "Explain MongoDB's document structure and collections.",
                "What are MongoDB aggregation pipelines?",
                "How does sharding work in MongoDB?",
                "What are the advantages and disadvantages of using MongoDB?"
            ],
            
            # Tools & Technologies
            'docker': [
                "What is containerization and how does Docker implement it?",
                "Explain the difference between Docker images and containers.",
                "What is a Dockerfile and what are its key instructions?",
                "How do you manage data persistence in Docker containers?",
                "What are Docker networks and how do containers communicate?"
            ],
            'kubernetes': [
                "What is Kubernetes and what problems does it solve?",
                "Explain the concept of pods in Kubernetes.",
                "What are Kubernetes services and how do they work?",
                "How does Kubernetes handle application scaling?",
                "What is the difference between Deployment and StatefulSet?"
            ],
            'aws': [
                "What are the main AWS compute services?",
                "How do you design fault-tolerant systems on AWS?",
                "What's your experience with AWS Lambda and serverless architecture?",
                "How do you implement auto-scaling strategies on AWS?",
                "What's your approach to AWS security and IAM management?"
            ],
            
            # System Design & Architecture
            'system_design': [
                "How would you design a URL shortener like bit.ly that handles millions of requests?",
                "Design a chat application that can handle millions of concurrent users.",
                "How would you architect a social media feed that updates in real-time?",
                "Design a distributed cache system like Redis Cluster.",
                "How would you build a recommendation system for an e-commerce platform?",
                "Design a file storage system like Dropbox or Google Drive.",
                "How would you architect a ride-sharing application like Uber?",
                "Design a search engine that can index billions of web pages.",
                "How would you build a real-time analytics system for tracking user behavior?",
                "Design a payment processing system that handles high transaction volumes.",
                "How would you architect a video streaming platform like Netflix?",
                "Design a distributed database that ensures ACID properties.",
                "How would you build a notification system that supports multiple channels?",
                "Design a load balancer that can handle millions of requests per second.",
                "How would you architect a microservices system with proper service discovery?"
            ],
            
            # Advanced Architecture Questions
            'architecture': [
                "Explain the trade-offs between microservices and monolithic architecture.",
                "How do you handle data consistency in distributed systems?",
                "What's your approach to implementing circuit breakers and retry mechanisms?",
                "How do you design APIs for backward compatibility?",
                "What's your strategy for handling database migrations in production?",
                "How do you implement event-driven architecture in practice?",
                "What's your approach to caching strategies in distributed systems?",
                "How do you handle authentication and authorization in microservices?",
                "What's your experience with CQRS (Command Query Responsibility Segregation)?",
                "How do you implement distributed tracing and monitoring?",
                "What's your approach to handling eventual consistency?",
                "How do you design systems for high availability and disaster recovery?",
                "What's your strategy for API rate limiting and throttling?",
                "How do you implement blue-green deployments and canary releases?",
                "What's your approach to handling cross-cutting concerns in distributed systems?"
            ],
            
            # Performance & Optimization
            'performance': [
                "How do you identify and resolve performance bottlenecks in web applications?",
                "What's your approach to database query optimization?",
                "How do you implement effective caching strategies?",
                "What tools do you use for application performance monitoring?",
                "How do you optimize frontend performance for large applications?",
                "What's your experience with CDN implementation and optimization?",
                "How do you handle memory management in high-traffic applications?",
                "What's your approach to load testing and capacity planning?",
                "How do you optimize API response times?",
                "What's your strategy for handling large file uploads and downloads?",
                "How do you implement efficient search functionality?",
                "What's your approach to optimizing mobile application performance?",
                "How do you handle real-time data processing at scale?",
                "What's your experience with performance profiling tools?",
                "How do you optimize database indexing strategies?"
            ],
            
            # Security
            'security': [
                "How do you implement secure authentication and authorization?",
                "What's your approach to preventing SQL injection attacks?",
                "How do you handle sensitive data encryption and storage?",
                "What's your experience with implementing OAuth and JWT?",
                "How do you secure API endpoints and prevent abuse?",
                "What's your approach to handling CORS and XSS vulnerabilities?",
                "How do you implement secure session management?",
                "What's your strategy for handling security vulnerabilities in dependencies?",
                "How do you implement proper input validation and sanitization?",
                "What's your experience with penetration testing and security audits?",
                "How do you handle secure communication between microservices?",
                "What's your approach to implementing role-based access control?",
                "How do you secure database connections and queries?",
                "What's your strategy for handling security in CI/CD pipelines?",
                "How do you implement secure file upload and processing?"
            ]
                "Explain the difference between S3 storage classes.",
                "What is AWS Lambda and when would you use it?",
                "How does AWS VPC work?",
                "What are the benefits of using AWS CloudFormation?"
            ],
            'git': [
                "What's your preferred Git workflow? How do you handle branching in team projects?",
                "Tell me about a time you had to resolve a complex merge conflict - what was your approach?",
                "What's the difference between git merge and git rebase, and when do you use each?",
                "How do you handle code reviews and collaboration using Git?",
                "What's your strategy for keeping a clean Git history?",
                "How do you approach hotfixes and emergency deployments with Git?",
                "What Git hooks have you used, and what problems did they solve?",
                "How do you handle large files or binary assets in Git repositories?",
                "What's your experience with Git submodules or subtrees?",
                "How do you approach versioning and tagging in your Git workflow?"
            ],
            
            # Frontend Technologies
            'bootstrap': [
                "What draws you to Bootstrap for your projects? How do you customize it?",
                "How do you approach responsive design with Bootstrap's grid system?",
                "What's your experience with Bootstrap components vs custom CSS?",
                "How do you handle Bootstrap customization without bloating your CSS?",
                "What's your approach to Bootstrap theming and branding?",
                "How do you optimize Bootstrap for performance in production?",
                "What are your thoughts on Bootstrap vs other CSS frameworks?",
                "How do you handle Bootstrap updates in existing projects?",
                "What's your experience with Bootstrap's JavaScript components?",
                "How do you approach accessibility when using Bootstrap?"
            ],
            
            'css': [
                "What's your approach to organizing CSS in larger projects?",
                "How do you handle CSS specificity and avoid conflicts?",
                "What's your experience with CSS preprocessors like Sass or Less?",
                "How do you approach responsive design and mobile-first development?",
                "What CSS methodologies (BEM, OOCSS, etc.) have you used?",
                "How do you handle cross-browser compatibility issues?",
                "What's your strategy for CSS performance optimization?",
                "How do you approach CSS animations and transitions?",
                "What's your experience with CSS Grid vs Flexbox?",
                "How do you handle CSS testing and quality assurance?"
            ],
            
            'html': [
                "How do you approach semantic HTML and accessibility?",
                "What's your strategy for SEO optimization in HTML?",
                "How do you handle forms and form validation in HTML?",
                "What's your experience with HTML5 APIs and features?",
                "How do you approach progressive enhancement in web development?",
                "What's your strategy for HTML performance optimization?",
                "How do you handle internationalization in HTML?",
                "What's your approach to HTML templating and reusability?",
                "How do you ensure HTML validation and standards compliance?",
                "What's your experience with web components and custom elements?"
            ],
            
            # Additional Backend Technologies
            'nodejs': [
                "What draws you to Node.js for backend development?",
                "How do you handle asynchronous programming in Node.js?",
                "What's your experience with Node.js performance optimization?",
                "How do you approach error handling in Node.js applications?",
                "What's your strategy for Node.js package management and security?",
                "How do you handle database connections and pooling in Node.js?",
                "What's your experience with Node.js clustering and scaling?",
                "How do you approach testing in Node.js applications?",
                "What's your experience with Node.js streams and buffers?",
                "How do you handle authentication and authorization in Node.js?"
            ],
            
            'express': [
                "What's your experience structuring Express.js applications?",
                "How do you handle middleware in Express? Any custom ones you've built?",
                "What's your approach to routing and route organization in Express?",
                "How do you handle error handling and logging in Express apps?",
                "What's your experience with Express security best practices?",
                "How do you approach API versioning in Express applications?",
                "What's your strategy for Express performance optimization?",
                "How do you handle file uploads and static assets in Express?",
                "What's your experience with Express templating engines?",
                "How do you approach testing Express applications?"
            ],
            
            # DevOps and Tools
            'nginx': [
                "What's your experience configuring Nginx for web applications?",
                "How do you approach load balancing with Nginx?",
                "What's your strategy for Nginx performance tuning?",
                "How do you handle SSL/TLS configuration in Nginx?",
                "What's your experience with Nginx as a reverse proxy?",
                "How do you approach Nginx security hardening?",
                "What's your experience with Nginx caching strategies?",
                "How do you handle Nginx logging and monitoring?",
                "What's your approach to Nginx configuration management?",
                "How do you handle Nginx updates and maintenance?"
            ],
            
            'redis': [
                "What use cases have you implemented Redis for?",
                "How do you approach Redis data modeling and key design?",
                "What's your experience with Redis persistence and durability?",
                "How do you handle Redis performance monitoring and optimization?",
                "What's your strategy for Redis clustering and high availability?",
                "How do you approach Redis security and access control?",
                "What's your experience with Redis pub/sub messaging?",
                "How do you handle Redis memory management and eviction policies?",
                "What's your approach to Redis backup and disaster recovery?",
                "How do you integrate Redis with your application architecture?"
            ]
        }
    
    def generate_questions(self, tech_stack: Dict[str, List[str]], 
                          max_questions_per_tech: int = 2) -> Dict[str, List[str]]:
        """Generate technical questions based on candidate's tech stack - with intelligence"""
        generated_questions = {}
        
        # Skip intelligent selector for now and use direct method
        # The intelligent selector is causing fallback to general questions
        
        # Enhanced method with better question selection
        tech_count = 0
        max_techs = 5  # Increased to cover more technologies
        
        # Prioritize technologies by category importance
        category_priority = {
            'languages': 1,
            'frameworks': 2, 
            'databases': 3,
            'devops_tools': 4,
            'web_servers': 5,
            'cloud_platforms': 6
        }
        
        # Sort technologies by priority and select diverse questions
        prioritized_techs = []
        for category, technologies in tech_stack.items():
            priority = category_priority.get(category, 7)
            for tech in technologies:
                prioritized_techs.append((priority, tech, category))
        
        # Sort by priority and select questions
        prioritized_techs.sort(key=lambda x: x[0])
        
        for priority, tech, category in prioritized_techs:
            if tech_count >= max_techs:
                break
                
            tech_lower = tech.lower()
            if tech_lower in self.question_bank:
                available_questions = self.question_bank[tech_lower]
                num_questions = min(max_questions_per_tech, len(available_questions))
                
                # Randomly select questions for variety
                if len(available_questions) > num_questions:
                    selected_questions = random.sample(available_questions, num_questions)
                else:
                    selected_questions = available_questions[:num_questions]
                
                generated_questions[tech] = selected_questions
                tech_count += 1
        
        # If we don't have enough questions, add some general ones
        if len(generated_questions) < 2:
            fallback_questions = self.get_fallback_questions("general")
            generated_questions["General"] = fallback_questions[:max_questions_per_tech]
        
        return generated_questions
    
    def get_fallback_questions(self, experience_level: str = "general") -> List[str]:
        """Generate fallback questions for unknown technologies"""
        fallback_questions = {
            "general": [
                "I'd love to hear about your debugging process - what's your approach when you hit a really tricky bug?",
                "The tech world moves so fast! How do you keep up with new technologies and trends?",
                "Tell me about a project you're particularly proud of - what made it challenging or interesting?",
                "What's your favorite development setup? Any tools or workflows you can't live without?",
                "How do you make sure your code is solid? What's your approach to quality and testing?"
            ],
            "senior": [
                "With your experience, I'm curious about your approach to system design - how do you tackle architecture decisions?",
                "What's your philosophy on code reviews and mentoring? Any memorable experiences helping junior developers?",
                "Technical debt is always a challenge - how do you balance new features with maintaining existing code?",
                "Performance can make or break an application - what's your strategy for optimization?",
                "When you're making technology choices for a team, what factors do you consider most important?"
            ],
            "junior": [
                "What aspects of programming are you most excited to dive deeper into?",
                "I love seeing how people learn - what's your approach when picking up a new technology or framework?",
                "Can you tell me about a recent challenge you faced and how you worked through it?",
                "What practices have you picked up for writing clean, maintainable code?",
                "How do you approach testing your code? Any strategies that have worked well for you?"
            ]
        }
        
        return fallback_questions.get(experience_level, fallback_questions["general"])
    
    def format_questions_for_display(self, questions_dict: Dict[str, List[str]]) -> str:
        """Format questions for display in the chat interface"""
        if not questions_dict:
            return "No specific technical questions generated. Let's proceed with general questions."
        
        formatted_output = "Based on your tech stack, here are some technical questions:\n\n"
        
        for tech, questions in questions_dict.items():
            formatted_output += f"**{tech}:**\n"
            for i, question in enumerate(questions, 1):
                formatted_output += f"{i}. {question}\n"
            formatted_output += "\n"
        
        return formatted_output