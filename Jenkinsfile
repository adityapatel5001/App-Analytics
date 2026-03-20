
pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-2"
        ECR_REPO = "analytics-app"
        CLUSTER_NAME = "analytics-eks-dev"
        DEPLOYMENT_NAME = "analytics-app"
        CONTAINER_NAME = "analytics-app"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/adityapatel5001/App-Analytics.git'
            }
        }

        stage('Get AWS Account ID') {
            steps {
                script {
                    env.AWS_ACCOUNT_ID = sh(
                        script: "aws sts get-caller-identity --query Account --output text",
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    env.IMAGE_TAG = "${env.BUILD_ID}"
                    sh "docker build -t ${ECR_REPO}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Login to ECR') {
            steps {
                sh """
                aws ecr get-login-password --region ${AWS_REGION} \
                | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                """
            }
        }

        stage('Tag and Push Image') {
            steps {
                script {
                    env.IMAGE_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"

                    sh """
                    docker tag ${ECR_REPO}:${IMAGE_TAG} ${IMAGE_URI}
                    docker push ${IMAGE_URI}
                    """
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh """
                aws eks update-kubeconfig --region ${AWS_REGION} --name ${CLUSTER_NAME}

                kubectl set image deployment/${DEPLOYMENT_NAME} \
                ${CONTAINER_NAME}=${IMAGE_URI}

                kubectl rollout status deployment/${DEPLOYMENT_NAME}
                """
            }
        }
    }
}

