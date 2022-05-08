pipeline {
    agent any
    stages {
        stage('Code quality and unit tests'){
            parallel {
                stage('Lint code') {
                    steps {
                        sh 'python3.10 -m pycodestyle --filename=*.py --max-line-length=120 .'
                    }
                }

                stage('Unit tests') {
                    steps {
                        sh 'python3.10 -m pip install -r requirements.txt'
                        sh 'docker run --name mongodb_test -d -p 27017:27017 mongo'
                        sh 'python3.10 -m pytest -m unit automated_tests/'
                        sh 'docker stop --name mongodb_test'
                    }
                }
            }
        }

        stage('Build image') {
            steps {
                script {
                    sh "docker build -t burly_pronghorn:${env.GIT_COMMIT} ."
                }
            }
        }

        stage('Automated tests') {
            steps {
                script {
                    sh 'python3.10 -m pip install -r requirements.txt'
                    sh 'docker start mongodb_test'
                    sh "docker run -d -p 8000:8000 --name tested_image burly_pronghorn:${env.GIT_COMMIT}"
                    sh 'python3.10 -m pytest automated_tests/ --log-cli-level=10'
                    sh 'docker stop mongodb_test'
                    sh 'docker stop tested_image'
                }
            }
        }
        stage('Deploy image') {
            steps {
                script {
                    sh "docker run -d -p 5000:5000 --restart=always --name registry -v /mnt/registry:/var/lib/registry registry:2"
                    sh "docker image tag burly_pronghorn:${env.GIT_COMMIT} localhost:5000/burly_pronghorn:${env.GIT_COMMIT}"
                    sh "docker push localhost:5000/burly_pronghorn:${env.GIT_COMMIT}"
                    sh "docker stop registry"
                }
            }
        }
    }
    post {
        always {
            cleanWs()
            script{
                sh 'docker system prune -af'
            }
        }
    }
}