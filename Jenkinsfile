pipeline {
    agent any
    stages {
        stage('Build compose image') {
            steps {
                script {
                    sh "docker compose up -d"
                }
            }
        }

        stage ('Unit and regular tests'){
            parallel {
                stage('Unit tests') {
                    steps {
                        dir('automated_tests/') {
                            sh 'tox -e lint'
                        }
                    }
                }
                stage('Automated tests') {
                    steps {
                        script {
                            dir('automated_tests/') {
                                sh 'tox -e regular'
                            }
                        }
                    }
                }
            }
        }
        post {
            always {
                script {
                    sh 'docker compose down'
                }
            }
        }

        stage('Build and deploy image') {
            when {
                branch pattern "release/*"
            }
            steps {
                script {
                    sh "docker build -t burly_pronghorn:${env.GIT_COMMIT} ."
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