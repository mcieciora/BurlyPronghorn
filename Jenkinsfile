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

        stage ('Automated tests'){
            parallel {
                stage ('Code linting'){
                    steps {
                        script {
                            dir('automated_tests/') {
                                sh 'tox -e lint'
                            }
                        }
                    }
                }
                stage ('Regular tests'){
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

        stage('Build and deploy image') {
            steps {
                script {
                    sh "docker build -t burly_pronghorn:${env.GIT_COMMIT} ."

                    if (env.BRANCH_NAME.contains('release/')) {
                        sh "docker image tag burly_pronghorn:${env.GIT_COMMIT} mcieciora/burly_pronghorn:${env.GIT_COMMIT}"
                        sh "docker push mcieciora/burly_pronghorn:${env.GIT_COMMIT}"
                    } else {
                        sh "docker run -d -p 5000:5000 --restart=always --name registry -v /mnt/registry:/var/lib/registry registry:2"
                        sh "docker image tag burly_pronghorn:${env.GIT_COMMIT} localhost:5000/burly_pronghorn:${env.GIT_COMMIT}"
                        sh "docker push localhost:5000/burly_pronghorn:${env.GIT_COMMIT}"
                        sh "docker stop registry"
                    }
                }
            }
        }
    }
    post {
        always {
            script{
                sh 'docker compose down'
                sh 'docker system prune -af'
            }
            cleanWs()
        }
    }
}