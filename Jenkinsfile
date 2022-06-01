pipeline {
    agent any
    stages {
        stage('Prepare for tests') {
            parallel {
                stage ('Code linting'){
                    steps {
                        script {
                            dir('automated_tests/') {
                                sh 'tox -e lint src'
                                sh 'tox -e lint automated_tests'
                            }
                        }
                    }
                }
                stage ('Setup docker image'){
                    steps {
                        script {
                            dir('automated_tests/') {
                                sh 'docker compose down'
                            }
                            def all_images = sh(script: 'docker images', returnStdout: true)
                            if (all_images.contains('burlypronghorn_api')) {
                                sh "docker rmi burlypronghorn_api -f"
                            }
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
                        sh 'docker rmi burlypronghorn_api:latest -f'
                    }
                }
                failure {
                    script {
                        sh 'docker logs burlypronghorn_api'
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
                        sh 'docker logs burlypronghorn_api'
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

        stage('Staging') {
            parallel {
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

                stage('Generate release docs') {
                    when {
                        expression {
                            return env.BRANCH_NAME.contains('release/')
                        }
                    }
                    steps {
                        script {
                            dir('automated_tests/tools') {
                                def html_report_generation = sh(script: 'tox -e report python3 generate_html_report_from_xml.py', returnStdout: true)
                                echo html_report_generation
                                if (html_report_generation.contains('[ERR]')) {
                                    error("generate_html_report_from_xml.py script failed due to\n${html_report_generation}")
                                }
                            }
                        }
                    }
                }

                stage('Check release files') {
                    when {
                        expression {
                            return env.BRANCH_NAME.contains('release/')
                        }
                    }
                    steps {
                        script {
                            def build_version = '0_1'
                            dir('automated_tests/tools') {
                                def script_result = sh(script: "python3.10 check_release_doc_files.py ${build_version}", returnStdout: true)
                                if (script_result.contains('[ERR]')) {
                                    error("${script_result}")
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            script{
                sh 'docker compose down'
                sh "docker rmi burlypronghorn_api -f"
            }
            archiveArtifacts artifacts: 'automated_tests/*results.xml,automated_tests/results.html', fingerprint: true
            junit 'automated_tests/*results.xml'
        }
    }
}