pipeline {
    agent any
    stages {
        stage('Prepare for tests') {
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
                stage ('Setup docker image'){
                    steps {
                        script {
                            def running_containers = sh(script: 'docker ps -q', returnStdout: true)
                            if (running_containers != '') {
                                sh "docker ps -aq | xargs docker stop"
                            }
                            sh 'docker system prune -af'
                            sh "sed -i 's/mongodb/localhost/1' src/mongodb.py"
                            sh 'docker compose up -d'
                        }
                    }
                }
            }
        }

        stage ('MongoDB and API unittests'){
            steps {
                script {
                    dir('automated_tests/') {
                        sh 'tox -e unittests'
                    }
                }
            }
            post {
                always {
                    script {
                        sh 'docker compose down'
                        sh 'docker rmi burlypronghorn_api:latest'
                    }
                }
                failure {
                    script {
                        sh 'docker logs api'
                    }
                }
            }
        }

        stage ('Regular tests'){
            steps {
                script {
                    sh "sed -i 's/localhost/mongodb/1' src/mongodb.py"
                    sh 'docker compose up -d'
                    dir('automated_tests/') {
                        sh 'tox -e regression'
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
                            error("Found @mark.skip among test scripts.\n${skipped_tests}")
                        }
                    }
                }
            }
        }

        stage('Deploy dev image to local registry') {
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
            archiveArtifacts artifacts: 'automated_tests/*results.xml, automated_tests/*results.html, automated_tests/assets/', fingerprint: true
            junit 'automated_tests/*results.xml'
            cleanWs()
        }
    }
}