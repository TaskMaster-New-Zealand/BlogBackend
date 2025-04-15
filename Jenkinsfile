import hudson.Util;
def current_stage
def build_duration_msg = "\n *Detail by Stage* \n"
pipeline {
    agent any

    environment {
        DATABASE_URL = 'postgres://test_user:test_password@localhost:5432/test_db'
        DEBUG = 'true'
        SECRET_KEY = 'dummy'
        PYTHON_VERSION = '3.12'
    }

    stages {
        stage('Setup Python Virtual Environment!') {
            steps {
                script {
                    start = System.currentTimeMillis()
                    current_stage =env.STAGE_NAME
                    if (isUnix()) {
                        sh '''
                            python3 -m venv venv
                            . venv/bin/activate
                            pip install -r requirements.txt
                            pip install coverage flake8
                        '''
                    } else {
                        bat '''
                            python -m venv venv
                            .\\venv\\Scripts\\activate
                            pip install -r requirements.txt
                            pip install coverage flake8
                        '''
                    }
                    end = System.currentTimeMillis()
                    build_duration_msg = build_duration_msg +  "*" + current_stage + "*" + " : "  + Util.getTimeSpanString(end - start) +"\n"
                }
            }
        }

        stage('Linter Check!') {
            steps {
                script {
                    start = System.currentTimeMillis()
                    current_stage =env.STAGE_NAME 
                    if (isUnix()) {
                        sh '''
                            . venv/bin/activate
                            flake8 . --exclude=./venv --ignore=E501 || echo "Flake8 finished with warnings."
                        '''
                    } else {
                        bat '''
                            .\\venv\\Scripts\\activate
                            flake8 . --exclude=./venv --ignore=E501 || echo "Flake8 finished with warnings."
                        '''
                    }
                    end = System.currentTimeMillis()
                    build_duration_msg = build_duration_msg +  "*" + current_stage + "*" + " : "  + Util.getTimeSpanString(end - start) +"\n"
                }
            }
        }

        stage('Run Tests with Coverage') {
            steps {
                script {
                    start = System.currentTimeMillis()
                    current_stage =env.STAGE_NAME 
                    if (isUnix()) {
                        sh '''
                            . venv/bin/activate
                            coverage run manage.py test
                            coverage report -m
                        '''
                    } else {
                        bat '''
                            .\\venv\\Scripts\\activate
                            coverage run manage.py test
                            coverage report -m
                        '''
                    }
                    end = System.currentTimeMillis()
                    build_duration_msg = build_duration_msg +  "*" + current_stage + "*" + " : "  + Util.getTimeSpanString(end - start) +"\n"
                }
            }
        }
    }

    post {
        always {
            script{
                build_duration_msg = build_duration_msg + "\n *Total build time:* " +  "${currentBuild.durationString}".replaceAll(' and counting', "")
            }
            cleanWs()
        }
        success{
            script{
                    current_stage = "Post Build"
                    slackSend color: 'good', message: "[${env.JOB_NAME}][Rama : ${env.BRANCH_NAME}] [Stage :${current_stage}][Resultado: ${currentBuild.result}](<${env.BUILD_URL}|Detalle>)${build_duration_msg}", tokenCredentialId: 'slack-group3-token'
                }
            }
    }
}