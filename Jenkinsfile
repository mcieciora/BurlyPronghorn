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
                stage ('Unit tests'){
                    steps {
                        script {
                            dir('automated_tests/') {
                                sh 'tox -e unittest'
                            }
                        }
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

        stage('Build and deploy image') {
            when {
                expression {
                    return env.BRANCH_NAME == 'develop'
                }
            }
            steps {
                script {
                    def commit_value = env.GIT_COMMIT.take(7)
                    def tag_value = "dev-${commit_value}"
                    echo "Tagging with ${tag_value}"
                    sh "docker build -t burly_pronghorn:${tag_value} ."
                    sh "docker run -d -p 5000:5000 --restart=always --name registry -v /mnt/registry:/var/lib/registry registry:2"
                    sh "docker image tag burly_pronghorn:${tag_value} localhost:5000/burly_pronghorn:${tag_value}"
                    sh "docker push localhost:5000/burly_pronghorn:${tag_value}"
                    sh "docker stop registry"
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
            archiveArtifacts artifacts: 'automated_tests/result.xml', fingerprint: true
            junit 'automated_tests/result.xml'
            cleanWs()
        }
    }
}