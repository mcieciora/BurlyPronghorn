pipeline {
    parameters {
        booleanParam(name: 'RELOAD_CONFIGURATION', defaultValue: false, description: '')
    }
    agent any
    stages {
        stage('Reload configuration'){
            when {
                expression { params.RELOAD_CONFIGURATION }
            }
            steps {
                script {
                    currentBuild.result = 'ABORTED'
                    error('Stopping job.')
                }
            }
        }
    }
}