# Log into AWS Elastic Container Registry
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.us-east-1.amazonaws.com

# Pull tensorflow-training container from ECR, mount the local directory and train the model
TRAINING_IMAGE=763104351884.dkr.ecr.us-east-1.amazonaws.com/tensorflow-training:2.12.0-gpu-py310-cu118-ubuntu20.04-ec2
docker run -it -v `pwd`:/env -w /env $TRAINING_IMAGE python train_model.py