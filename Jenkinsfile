pipeline {
    agent any

    environment {
        VENV = 'venv'
        TARGET_DIR = '/home/artifacts/'  // Make sure this directory exists or is created
    }

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    if (fileExists("${VENV}")) {
                        echo 'Using existing virtual environment'
                    } else {
                        echo 'Creating a new virtual environment'
                        sh '/usr/bin/python3 -m venv $VENV'
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . $VENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build Package') {
            steps {
                sh '''
                    . $VENV/bin/activate
                    python setup.py sdist bdist_wheel
                '''
            }
        }

        stage('Copy Packages') {
            steps {
                script {
                    if (!fileExists("${TARGET_DIR}")) {
                        sh "mkdir -p ${TARGET_DIR}"
                    }
                    sh "cp dist/* ${TARGET_DIR}"
                }
            }
        }
    }

    post {
        success {
            echo 'Build and deployment successful!'
        }
        failure {
            echo 'Build or deployment failed.'
        }
    }
}

