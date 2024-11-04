pipeline {
    agent any

    environment {
        VENV = 'venv'
        PYPI_CREDS = credentials('pypi-credentials')
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
                        // Use the direct path if the tool configuration isn't working
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
                script {
                    // Extract the username and password from credentials
                    env.PYPI_CREDS_USR = PYPI_CREDS_USR ?: PYPI_CREDS_USR_PSW.split(':')[0]
                    env.PYPI_CREDS_PSW = PYPI_CREDS_PSW ?: PYPI_CREDS_USR_PSW.split(':')[1]
                }
                sh '''
                    # Activate the virtual environment
                    . $VENV/bin/activate

                    # Publish package to PyPI using Twine
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
