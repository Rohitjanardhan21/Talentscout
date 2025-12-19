"""
Configuration settings for the TalentScout Hiring Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Application Settings
    APP_TITLE = "TalentScout Hiring Assistant"
    APP_DESCRIPTION = "AI-powered candidate screening chatbot"
    
    # Conversation Settings - Enhanced for Better Experience
    MAX_QUESTIONS_PER_TECH = 3  # Increased for more comprehensive assessment
    MIN_EXPERIENCE_YEARS = 0
    MAX_EXPERIENCE_YEARS = 50
    
    # Performance Settings
    ENABLE_LLM_ENHANCEMENT = False  # Disabled for faster responses
    MAX_TECH_STACK_ITEMS = 3  # Limit processing for speed
    CACHE_RESPONSES = True
    
    # Advanced Question Settings
    ENABLE_ADVANCED_QUESTIONS = True  # Enable advanced technical questions
    MAX_QUESTIONS_TOTAL = 10  # Total questions in interview
    ADVANCED_QUESTION_THRESHOLD = 3  # Start advanced questions after this many responses
    
    # Exit Keywords
    EXIT_KEYWORDS = [
        'bye', 'goodbye', 'exit', 'quit', 'end', 'stop', 
        'thanks', 'thank you', 'done', 'finished'
    ]
    
    # Required Candidate Fields
    REQUIRED_FIELDS = [
        'full_name', 'email', 'phone', 'experience_years', 
        'desired_position', 'location', 'tech_stack'
    ]
    
    # Comprehensive Technology Knowledge Base
    COMMON_TECHNOLOGIES = {
        'languages': [
            # Popular Languages
            'python', 'javascript', 'typescript', 'java', 'c#', 'go', 'rust',
            'php', 'ruby', 'swift', 'kotlin', 'scala', 'c++', 'c',
            # Emerging Languages
            'dart', 'elixir', 'haskell', 'clojure', 'f#', 'julia', 'r',
            # Web Languages
            'html', 'css', 'sass', 'less', 'stylus',
            # Shell/Scripting
            'bash', 'powershell', 'perl', 'lua'
        ],
        'frameworks': [
            # Frontend Frameworks
            'react', 'vue', 'angular', 'svelte', 'nextjs', 'nuxtjs', 'gatsby',
            'ember', 'backbone', 'jquery', 'alpine', 'lit', 'stencil', 'bootstrap',
            # Backend Frameworks
            'django', 'flask', 'fastapi', 'tornado', 'pyramid', 'bottle',
            'spring', 'spring boot', 'quarkus', 'micronaut', 'play',
            'express', 'nestjs', 'koa', 'hapi', 'meteor',
            'laravel', 'symfony', 'codeigniter', 'cakephp', 'yii',
            'rails', 'sinatra', 'hanami',
            'asp.net', 'blazor', '.net core',
            # Mobile Frameworks
            'react native', 'flutter', 'ionic', 'xamarin', 'cordova',
            # Desktop Frameworks
            'electron', 'tauri', 'qt', 'tkinter', 'wpf'
        ],
        'databases': [
            # Relational Databases
            'mysql', 'postgresql', 'sqlite', 'mariadb', 'oracle', 'sql server',
            'db2', 'sybase', 'firebird', 'cockroachdb', 'yugabytedb',
            # NoSQL Databases
            'mongodb', 'couchdb', 'couchbase', 'amazon dynamodb', 'firebase',
            # Key-Value Stores
            'redis', 'memcached', 'etcd', 'consul',
            # Graph Databases
            'neo4j', 'amazon neptune', 'arangodb', 'orientdb',
            # Search Engines
            'elasticsearch', 'solr', 'algolia', 'amazon cloudsearch',
            # Time Series
            'influxdb', 'timescaledb', 'prometheus'
        ],
        'cloud_platforms': [
            # Major Cloud Providers
            'aws', 'azure', 'gcp', 'google cloud', 'alibaba cloud',
            'oracle cloud', 'ibm cloud', 'digitalocean', 'linode',
            'vultr', 'hetzner', 'ovh'
        ],
        'devops_tools': [
            # Containerization
            'docker', 'podman', 'containerd', 'lxc',
            # Orchestration
            'kubernetes', 'docker swarm', 'nomad', 'mesos',
            # CI/CD
            'jenkins', 'gitlab ci', 'github actions', 'circleci', 'travis ci',
            'azure devops', 'bamboo', 'teamcity', 'buildkite',
            # Infrastructure as Code
            'terraform', 'pulumi', 'cloudformation', 'arm templates',
            'ansible', 'puppet', 'chef', 'saltstack',
            # Monitoring
            'prometheus', 'grafana', 'datadog', 'new relic', 'splunk',
            'elk stack', 'fluentd', 'jaeger', 'zipkin'
        ],
        'development_tools': [
            # Version Control
            'git', 'svn', 'mercurial', 'perforce',
            # IDEs/Editors
            'vscode', 'intellij', 'eclipse', 'vim', 'emacs', 'sublime text',
            'atom', 'webstorm', 'pycharm', 'visual studio',
            # Build Tools
            'webpack', 'vite', 'rollup', 'parcel', 'gulp', 'grunt',
            'maven', 'gradle', 'sbt', 'leiningen',
            'npm', 'yarn', 'pnpm', 'pip', 'conda', 'composer',
            # Testing
            'jest', 'mocha', 'jasmine', 'cypress', 'selenium', 'playwright',
            'junit', 'testng', 'pytest', 'unittest', 'rspec'
        ],
        'web_servers': [
            'nginx', 'apache', 'iis', 'caddy', 'traefik', 'haproxy',
            'cloudflare', 'fastly', 'cloudfront'
        ],
        'message_queues': [
            'rabbitmq', 'apache kafka', 'redis pub/sub', 'amazon sqs',
            'apache pulsar', 'nats', 'zeromq'
        ],
        'api_technologies': [
            'rest', 'graphql', 'grpc', 'soap', 'websockets', 'sse',
            'openapi', 'swagger', 'postman', 'insomnia'
        ]
    }