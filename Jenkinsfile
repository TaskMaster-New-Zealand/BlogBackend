pipeline {
    agent any

    environment {
        DATABASE_URL = 'postgres://test_user:test_password@localhost:5432/test_db'
        DEBUG = 'true'
        SECRET_KEY = 'dummy'
        PYTHON_VERSION = '3.12'
    }

    stages {
        stage('Setup Python Virtual Environment') {
            steps {
                script {
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
                }
            }
        }

        stage('Linter Check!') {
            steps {
                script {
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
                }
            }
        }

        stage('Run Tests with Coverage') {
            steps {
                script {
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
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}