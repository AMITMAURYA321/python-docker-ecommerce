pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'DOCKER_CI_DC',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                        -u "$DOCKER_USERNAME" \
                        --password-stdin
                    '''
                }
            }
        }

        stage('Verify Docker') {
            steps {
                sh 'docker --version'
                sh 'docker ps'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t amit8192/python-docker-ecommerce:latest ./backend'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh 'docker push amit8192/python-docker-ecommerce:latest'
            }
        }

        stage('Deploy to Production') {
            steps {
                sh '''
                    export IMAGE_TAG=latest

                    docker pull amit8192/python-docker-ecommerce:$IMAGE_TAG

                    docker compose -f docker-compose.prod.yml up -d backend

                    sleep 10

                    curl -f http://localhost:8082/health
                '''
            }
        }

        stage('Docker Logout') {
            steps {
                sh 'docker logout'
            }
        }
    }
}
