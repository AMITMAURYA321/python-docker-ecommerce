pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'amit8192/python-docker-ecommerce'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

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
                sh 'docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ./backend'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh 'docker push ${DOCKER_IMAGE}:${IMAGE_TAG}'
            }
        }

        stage('Deploy to Production') {
            steps {
                sh '''
                    docker pull ${DOCKER_IMAGE}:${IMAGE_TAG}

                    export IMAGE_TAG=${IMAGE_TAG}

                    docker compose \
                      --env-file .env \
                      -f docker-compose.prod.yml \
                      up -d backend

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
```

**`DOCKER_CI_DC` same rakha hai.** सिर्फ extra `}` हटाया है.
