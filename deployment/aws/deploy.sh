#!/bin/bash

# TalentScout Hiring Assistant AWS Deployment Script
# This script helps deploy the application to AWS EC2

echo "🚀 TalentScout Hiring Assistant - AWS Deployment"
echo "================================================"

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS CLI not configured. Please run 'aws configure' first."
    exit 1
fi

echo "✅ AWS CLI configured"

# Variables
INSTANCE_TYPE="t3.micro"
KEY_NAME="talentscout-key"
SECURITY_GROUP="talentscout-sg"
AMI_ID="ami-0c02fb55956c7d316"  # Amazon Linux 2 AMI (update as needed)

echo "📋 Deployment Configuration:"
echo "   Instance Type: $INSTANCE_TYPE"
echo "   Key Name: $KEY_NAME"
echo "   Security Group: $SECURITY_GROUP"
echo "   AMI ID: $AMI_ID"

# Create security group
echo "🔒 Creating security group..."
aws ec2 create-security-group \
    --group-name $SECURITY_GROUP \
    --description "Security group for TalentScout Hiring Assistant" \
    --output text > /dev/null 2>&1

# Add rules to security group
aws ec2 authorize-security-group-ingress \
    --group-name $SECURITY_GROUP \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0 > /dev/null 2>&1

aws ec2 authorize-security-group-ingress \
    --group-name $SECURITY_GROUP \
    --protocol tcp \
    --port 8501 \
    --cidr 0.0.0.0/0 > /dev/null 2>&1

echo "✅ Security group configured"

# Create user data script
cat > user-data.sh << 'EOF'
#!/bin/bash
yum update -y
yum install -y python3 python3-pip git

# Clone repository (replace with your actual repo URL)
cd /home/ec2-user
git clone https://github.com/your-username/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant

# Install dependencies
pip3 install -r requirements.txt

# Create .env file (you'll need to add your API key)
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Install and start the application as a service
cat > /etc/systemd/system/talentscout.service << 'EOL'
[Unit]
Description=TalentScout Hiring Assistant
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/talentscout-hiring-assistant
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
EOL

systemctl enable talentscout
systemctl start talentscout
EOF

echo "🖥️  Launching EC2 instance..."

# Launch EC2 instance
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-groups $SECURITY_GROUP \
    --user-data file://user-data.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=TalentScout-Hiring-Assistant}]' \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "✅ Instance launched: $INSTANCE_ID"

# Wait for instance to be running
echo "⏳ Waiting for instance to be running..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "================================================"
echo "🎉 Deployment Complete!"
echo "📍 Instance ID: $INSTANCE_ID"
echo "🌐 Public IP: $PUBLIC_IP"
echo "🔗 Application URL: http://$PUBLIC_IP:8501"
echo ""
echo "⚠️  Important Notes:"
echo "   1. Update the .env file on the server with your OpenAI API key"
echo "   2. SSH into the instance: ssh -i $KEY_NAME.pem ec2-user@$PUBLIC_IP"
echo "   3. The application may take a few minutes to start"
echo "   4. Check logs: sudo journalctl -u talentscout -f"
echo "================================================"

# Clean up
rm user-data.sh