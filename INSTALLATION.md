# Installation Guide - TalentScout Hiring Assistant

## Quick Start (Local Development)

### Prerequisites
- Python 3.8 or higher
- pip package manager
- OpenAI API key (optional but recommended)

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd talentscout-hiring-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_api_key_here
```

### 4. Run the Application
```bash
# Option 1: Using the run script
python run_app.py

# Option 2: Direct streamlit command
streamlit run app.py
```

### 5. Access the Application
Open your browser and go to: `http://localhost:8501`

## Detailed Installation Options

### Option 1: Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run_app.py
```

### Option 2: Docker Deployment
```bash
# Build and run with Docker Compose
cd deployment/docker
docker-compose up --build

# Access at http://localhost:8501
```

### Option 3: AWS Cloud Deployment
```bash
# Configure AWS CLI first
aws configure

# Run deployment script
cd deployment/aws
chmod +x deploy.sh
./deploy.sh
```

## Configuration Options

### Environment Variables
Create a `.env` file with the following variables:

```env
# Required for enhanced LLM features
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Specify OpenAI model
OPENAI_MODEL=gpt-3.5-turbo
```

### Application Settings
You can modify settings in `config.py`:

- `MAX_QUESTIONS_PER_TECH`: Number of questions per technology (default: 2)
- `EXIT_KEYWORDS`: Keywords that end the conversation
- `REQUIRED_FIELDS`: Fields that must be collected from candidates

## Testing

### Run Unit Tests
```bash
# Run all tests
python run_tests.py

# Run specific test file
python -m unittest tests.test_data_handler

# Run with coverage (if coverage is installed)
pip install coverage
coverage run -m unittest discover tests
coverage report
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**
   ```bash
   # Ensure you're in the correct directory and have installed dependencies
   pip install -r requirements.txt
   ```

2. **OpenAI API Key Issues**
   ```bash
   # Check if .env file exists and contains your API key
   cat .env
   ```

3. **Port Already in Use**
   ```bash
   # Use a different port
   streamlit run app.py --server.port 8502
   ```

4. **Permission Denied (AWS Deployment)**
   ```bash
   # Make deployment script executable
   chmod +x deployment/aws/deploy.sh
   ```

### Performance Optimization

1. **For Large Scale Deployment**
   - Use a production WSGI server like Gunicorn
   - Implement Redis for session management
   - Use a load balancer for multiple instances

2. **For Better Response Times**
   - Cache frequently used questions
   - Implement async processing for LLM calls
   - Use CDN for static assets

## Security Considerations

### Data Privacy
- The application doesn't store candidate data permanently
- All data is processed in session state only
- Implement HTTPS in production deployments

### API Key Security
- Never commit API keys to version control
- Use environment variables or secure key management
- Rotate API keys regularly

### Network Security
- Configure proper firewall rules
- Use VPC for AWS deployments
- Implement rate limiting for production use

## Production Deployment Checklist

- [ ] Set up HTTPS/SSL certificates
- [ ] Configure proper logging
- [ ] Set up monitoring and alerting
- [ ] Implement backup strategies
- [ ] Configure auto-scaling (if needed)
- [ ] Set up CI/CD pipeline
- [ ] Perform security audit
- [ ] Test disaster recovery procedures

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the application logs
3. Check GitHub issues (if applicable)
4. Contact the development team

## Next Steps

After successful installation:
1. Customize the question bank in `utils/question_generator.py`
2. Modify the UI styling in `app.py`
3. Add additional tech stacks in `config.py`
4. Implement additional features as needed