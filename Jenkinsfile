pipeline {
    agent any
    stages {
        stage ('Prepare test container'){
            steps {
                sh 'docker build -f automated_tests/Dockerfile -t test_image .'
            }
        }

        stage('Code quality and unit tests'){
            parallel {
                stage('Lint code') {
                    steps {
                        sh 'docker run --name lint_code test_image -m pycodestyle --filename=*.py --max-line-length=120 .'
                    }
                }

                stage('Unit tests') {
                    steps {
                        sh 'docker run --name mongodb_test -d -p 27017:27017 mongo'
                        sh 'docker run --name unit_test test_image -m pytest -m unit automated_tests/'
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
                    sh 'docker start mongodb_test'
                    sh "docker run -d -p 8000:8000 --name tested_image burly_pronghorn:${env.GIT_COMMIT}"
                    sh 'docker run test_image --name automated_tests -m pytest automated_tests/ --log-cli-level=10'
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