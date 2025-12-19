"""
Sample conversations for demonstrating the TalentScout Hiring Assistant
"""

SAMPLE_CONVERSATIONS = {
    "python_developer": {
        "candidate_info": {
            "full_name": "Alice Johnson",
            "email": "alice.johnson@email.com",
            "phone": "+1-555-0123",
            "experience_years": "5",
            "desired_position": "Senior Python Developer",
            "location": "San Francisco, CA",
            "tech_stack": "Python, Django, PostgreSQL, Docker, AWS, React"
        },
        "conversation_flow": [
            "Hello! I'm Alice Johnson",
            "alice.johnson@email.com",
            "+1-555-0123",
            "5",
            "Senior Python Developer",
            "San Francisco, CA",
            "Python, Django, PostgreSQL, Docker, AWS, React",
            "I'd be happy to answer questions about Python. Decorators are functions that modify other functions..."
        ]
    },
    
    "javascript_developer": {
        "candidate_info": {
            "full_name": "Bob Smith",
            "email": "bob.smith@email.com", 
            "phone": "+1-555-0456",
            "experience_years": "3",
            "desired_position": "Frontend Developer",
            "location": "New York, NY",
            "tech_stack": "JavaScript, React, Node.js, MongoDB, Git"
        },
        "conversation_flow": [
            "Hi, I'm Bob Smith",
            "bob.smith@email.com",
            "+1-555-0456", 
            "3",
            "Frontend Developer",
            "New York, NY",
            "JavaScript, React, Node.js, MongoDB, Git",
            "Sure! The main difference between == and === is that == performs type coercion..."
        ]
    },
    
    "full_stack_developer": {
        "candidate_info": {
            "full_name": "Carol Davis",
            "email": "carol.davis@email.com",
            "phone": "+1-555-0789",
            "experience_years": "7",
            "desired_position": "Full Stack Developer",
            "location": "Austin, TX", 
            "tech_stack": "Java, Spring Boot, Angular, MySQL, Kubernetes, Jenkins"
        },
        "conversation_flow": [
            "Hello, Carol Davis here",
            "carol.davis@email.com",
            "+1-555-0789",
            "7", 
            "Full Stack Developer",
            "Austin, TX",
            "Java, Spring Boot, Angular, MySQL, Kubernetes, Jenkins",
            "I can discuss Spring Boot's auto-configuration. It automatically configures beans based on classpath..."
        ]
    },
    
    "junior_developer": {
        "candidate_info": {
            "full_name": "David Wilson",
            "email": "david.wilson@email.com",
            "phone": "+1-555-0321",
            "experience_years": "1",
            "desired_position": "Junior Software Developer",
            "location": "Seattle, WA",
            "tech_stack": "Python, Flask, SQLite, Git, HTML, CSS"
        },
        "conversation_flow": [
            "Hi there! I'm David Wilson",
            "david.wilson@email.com",
            "+1-555-0321",
            "1",
            "Junior Software Developer", 
            "Seattle, WA",
            "Python, Flask, SQLite, Git, HTML, CSS",
            "I'm excited to learn more about Python! I recently worked on a Flask project where..."
        ]
    }
}

def get_sample_conversation(developer_type: str) -> dict:
    """Get a sample conversation by developer type"""
    return SAMPLE_CONVERSATIONS.get(developer_type, SAMPLE_CONVERSATIONS["python_developer"])

def get_all_sample_types() -> list:
    """Get all available sample conversation types"""
    return list(SAMPLE_CONVERSATIONS.keys())

def print_sample_conversation(developer_type: str):
    """Print a formatted sample conversation"""
    conversation = get_sample_conversation(developer_type)
    
    print(f"\n{'='*50}")
    print(f"SAMPLE CONVERSATION: {developer_type.upper().replace('_', ' ')}")
    print(f"{'='*50}")
    
    print("\n📋 CANDIDATE INFORMATION:")
    for key, value in conversation["candidate_info"].items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\n💬 CONVERSATION FLOW:")
    questions = [
        "What's your full name?",
        "What's your email address?", 
        "What's your phone number?",
        "How many years of professional experience do you have?",
        "What position(s) are you interested in?",
        "What's your current location?",
        "Please describe your tech stack:",
        "Technical question response:"
    ]
    
    for i, (question, response) in enumerate(zip(questions, conversation["conversation_flow"])):
        print(f"\n  Assistant: {question}")
        print(f"  Candidate: {response}")
    
    print(f"\n{'='*50}")

if __name__ == "__main__":
    print("🤖 TalentScout Hiring Assistant - Sample Conversations")
    print("\nAvailable sample types:")
    for i, sample_type in enumerate(get_all_sample_types(), 1):
        print(f"  {i}. {sample_type.replace('_', ' ').title()}")
    
    # Print all sample conversations
    for sample_type in get_all_sample_types():
        print_sample_conversation(sample_type)