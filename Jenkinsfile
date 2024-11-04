pipeline {
    agent any

    environment {
        VENV = 'venv'
        // Define the target directory where you want to copy the packages
        TARGET_DIR = '/home/artifacts/'
    }

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    // Check if the virtual environment already exists
                    if (fileExists("${VENV}")) {
                        echo 'Using existing virtual environment'
                    } else {
                        echo 'Creating a new virtual environment'
                        sh 'python3 -m venv $VENV'
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    # Activate the virtual environment
                    . $VENV/bin/activate

                    # Upgrade pip and install package dependencies
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build Package') {
            steps {
                sh '''
                    # Activate the virtual environment
                    . $VENV/bin/activate

                    # Build the package
                    python setup.py sdist bdist_wheel
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
                    // Copy the built packages to the target directory on the host machine
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
