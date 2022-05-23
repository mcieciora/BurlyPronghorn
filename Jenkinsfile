pipeline {
    agent any
    stages {
        stage('Docker cleanup') {
            steps {
                script {
                    def return_1 = sh(script: 'docker ps -aq', returnStdout: true)
                    echo return_1
                    def return_2 = sh(script: 'docker ps -q', returnStdout: true)
                    echo return_2
                    def return_3 = sh(script: 'docker ps -aq', returnStdout: true).trim()
                    echo return_3
                    def return_4 = sh(script: 'docker ps -q', returnStdout: true).trim()
                    echo return_4
                    // sh "docker ps -aq | xargs docker stop"
                    // sh 'docker system prune -af'
                }
            }
        }

        stage ('MongoDB unittests'){
            steps {
                script {
                    sh "sed -i 's/mongodb/localhost/1' src/mongodb.py"
                    sh 'docker compose up -d'
                    dir('automated_tests/') {
                        sh 'tox -e mongodb'
                    }
                }
            }
            post {
                always {
                    script {
                        sh "sed -i 's/localhost/mongodb/1' src/mongodb.py"
                        sh 'docker compose down'
                        sh 'docker system prune -af'
                    }
                }
                failure {
                    script {
                        sh 'docker logs api'
                    }
                }
            }
        }

        stage('Compose Docker image') {
            steps {
                script {
                    sh 'docker compose up -d'
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
                    post {
                        failure {
                            script {
                                sh 'docker logs api'
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
            post {
                failure {
                    script {
                        sh 'docker logs api'
                    }
                }
            }
        }

        stage('Scan for skipped tests') {
            when {
                expression {
                    return env.BRANCH_NAME == 'develop' || env.BRANCH_NAME == 'release'
                }
            }
            steps {
                script {
                    dir('automated_tests/tools') {
                        def skipped_tests = sh(script: 'python3.10 scan_for_skipped_tests.py', returnStdout: true)
                        if (skipped_tests.contains('[ERR]')) {
                            error('Found @mark.skip among test scripts.\n${skipped_tests}')
                        }
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
            archiveArtifacts artifacts: 'automated_tests/*results.xml', fingerprint: true
            junit 'automated_tests/*results.xml'
            cleanWs()
        }
    }
}