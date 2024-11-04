pipeline {
    agent any

    environment {
        VENV = 'venv'  // Virtual environment directory
        TARGET_DIR = '/var/jenkins_home/artifacts'  // Ensure this directory exists or is created
    }

    stages {
        stage('Check Python Installation') {
            steps {
                echo 'Checking Python installation...'
                sh 'python3 --version'  // This will print the Python version to the console
            }
        }

        stage('Prepare Environment') {
            steps {
                script {
                    // Check if the virtual environment already exists
                    if (fileExists("${VENV}")) {
                        echo 'Using existing virtual environment'
                    } else {
                        echo 'Creating a new virtual environment'
                        sh 'python3 -m venv ${VENV}'  // Creates a new virtual environment
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . ${VENV}/bin/activate
                    pip install --upgrade pip  // Ensure the latest version of pip is installed
                    pip install -r requirements.txt  // Install required Python packages from requirements.txt
                    pip install wheel  // Ensure wheel is installed to enable building wheels
                '''
            }
        }

        stage('Build Package') {
            steps {
                sh '''
                    . ${VENV}/bin/activate
                    python setup.py sdist bdist_wheel  // Build both source and wheel package
                '''
            }
        }

        stage('Copy Packages') {
            steps {
                script {
                    // Ensure the target directory exists
                    if (!fileExists("${TARGET_DIR}")) {
                        sh "mkdir -p ${TARGET_DIR}"
                    }
                    // Copy all packages from dist to the target directory
                    sh "cp dist/* ${TARGET_DIR}"
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()  // Cleans up the workspace after the job completes, important for managing disk space
        }
        success {
            echo 'Build and deployment successful!'
        }
        failure {
            echo 'Build or deployment failed.'
        }
    }
}
