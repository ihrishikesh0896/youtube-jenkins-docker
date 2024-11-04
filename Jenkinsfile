pipeline {
    agent any

    environment {
        VENV = 'venv'
        PYPI_CREDS = credentials('pypi-credentials')
    }

    tools {
        python3 'Python3'  // Define the Python tool configuration
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

        stage('Publish to PyPI') {
            steps {
                sh '''
                    # Activate the virtual environment
                    . $VENV/bin/activate

                    # Publish package to PyPI
                    twine upload -u $PYPI_CREDS_USR -p $PYPI_CREDS_PSW dist/*
                '''
            }
        }
    }

    post {
        always {
            // Clean up the workspace to free space
            deleteDir()
        }
        success {
            echo 'Build and deployment successful!'
        }
        failure {
            echo 'Build or deployment failed.'
        }
    }
}
