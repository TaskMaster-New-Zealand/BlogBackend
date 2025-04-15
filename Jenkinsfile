import hudson.Util;
def current_stage
def build_duration_msg = "\n *Detail by Stage* \n"
def dockerImage

pipeline {
    agent any

    environment {
        DATABASE_URL = 'postgres://test_user:test_password@localhost:5432/test_db'
        DEBUG = 'true'
        SECRET_KEY = 'dummy'
        PYTHON_VERSION = '3.12'
        DOCKER_IMAGE = 'blog-backend'
        AWS_REGION = 'us-east-1'
        ECR_REPOSITORY = 'your-ecr-repo-name'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
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
        

        stage('Build Docker Image') {
            steps {
                script {
                    start = System.currentTimeMillis()
                    current_stage = env.STAGE_NAME
                    // Build Docker image
                    sh """
                        docker build -t taskmaster/backend .
                    """
                    end = System.currentTimeMillis()
                    build_duration_msg = build_duration_msg + "*" + current_stage + "*" + " : " + Util.getTimeSpanString(end - start) + "\n"
                }
            }
        }

        stage('Push to AWS ECR') {
            steps {
                script {
                    start = System.currentTimeMillis()
                    current_stage = env.STAGE_NAME
                    sh """
                        aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 016456419140.dkr.ecr.ap-southeast-2.amazonaws.com
                        docker tag taskmaster/backend:latest 016456419140.dkr.ecr.ap-southeast-2.amazonaws.com/taskmaster/backend:latest
                        docker push 016456419140.dkr.ecr.ap-southeast-2.amazonaws.com/taskmaster/backend:latest
                    """                    
                    end = System.currentTimeMillis()
                    build_duration_msg = build_duration_msg + "*" + current_stage + "*" + " : " + Util.getTimeSpanString(end - start) + "\n"
                }
            }
        }
        stage('Clean images') {
            steps {
                script {
                    start = System.currentTimeMillis()
                    current_stage = env.STAGE_NAME
                    sh """
                        docker rmi -f taskmaster/backend:latest
                        docker system prune -f
                    """                    
                    end = System.currentTimeMillis()
                    build_duration_msg = build_duration_msg + "*" + current_stage + "*" + " : " + Util.getTimeSpanString(end - start) + "\n"
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
                    slackSend color: 'good', message: "[${env.JOB_NAME}][Branch : ${env.GIT_BRANCH}] [Stage :${current_stage}][Resultado: ${currentBuild.result}](<${env.BUILD_URL}|Detail>)${build_duration_msg}", tokenCredentialId: 'slack-group3-token'
                }
            }
    }
}