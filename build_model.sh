# Set the AWS account ID as an environment variable
export AWS_ACCOUNT_ID=<your-aws-account-id>

# Upload the trained model to AWS Elastic Container Registry
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com

# Build the model container
docker build -t model_deployment:1 .

# Push to ECR
docker tag ml_deployment:1 ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/ml_deployment:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/ml_deployment:latest