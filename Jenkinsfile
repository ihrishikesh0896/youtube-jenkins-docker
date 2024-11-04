pipeline {
    agent any

    environment {
        VENV = 'venv'
        TARGET_DIR = '/home/artifacts/'  // Ensure this directory exists or is created
    }

    stages {
        stage('Check Python Installation') {
            steps {
                echo 'Checking Python installation...'
                sh 'python3 --version'
                sh 'python3 -m venv --help'
            }
        }

        stage('Prepare Environment') {
            steps {
                script {
                    if (fileExists("${VENV}")) {
                        echo 'Using existing virtual environment'
                        sh 'ls -alh ${VENV}' // List contents of the venv directory
                    } else {
                        echo 'Creating a new virtual environment'
                        sh 'python3 -m venv ${VENV}'
                        sh 'ls -alh ${VENV}' // Verify creation
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build Package') {
            steps {
                sh '''
                    . ${VENV}/bin/activate
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
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
        success {
            echo 'Build and deployment successful!'
        }
        failure {
            echo 'Build or deployment failed.'
        }
    }
}
