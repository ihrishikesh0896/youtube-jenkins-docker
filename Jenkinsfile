pipeline {
    agent any
    environment {
        VENV = 'venv'
        TARGET_DIR = '/var/jenkins_home/artifacts'
        // Add version tracking from your setup.py or a version file
        VERSION = sh(script: 'python3 setup.py --version', returnStdout: true).trim()
    }
    
    stages {
        stage('Check Python Installation') {
            steps {
                script {
                    def pythonVersion = sh(script: 'python3 --version', returnStdout: true).trim()
                    echo "Using Python: ${pythonVersion}"
                }
            }
        }

        stage('Debug Git Setup') {
    steps {
        script {
            sh 'pwd'  // Print the current working directory
            sh 'ls -la'  // List all files in the current directory
            sh 'git status'  // Show the Git status to confirm it's a Git repository
            sh 'git remote -v'  // List current remote configurations
        }
    }
}
        
        stage('Prepare Environment') {
            steps {
                script {
                    // Delete existing venv if it exists to ensure clean environment
                    sh 'rm -rf ${VENV}'
                    echo 'Creating new virtual environment'
                    sh 'python3 -m venv ${VENV}'
                    
                    // Make sure target directory exists with proper permissions
                    sh 'mkdir -p ${TARGET_DIR}'
                    sh 'chmod 755 ${TARGET_DIR}'
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''#!/bin/bash
                    source ${VENV}/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install wheel setuptools twine
                    if [ -f requirements.txt ]; then
                        python -m pip install -r requirements.txt
                    else
                        echo "No requirements.txt found"
                    fi
                '''
            }
        }
        
        stage('Build Package') {
            steps {
                sh '''#!/bin/bash
                    source ${VENV}/bin/activate
                    # Clean previous builds
                    rm -rf dist/ build/ *.egg-info
                    python setup.py sdist bdist_wheel
                '''
            }
        }
        
        stage('Test Package') {
            steps {
                sh '''#!/bin/bash
                    source ${VENV}/bin/activate
                    # Basic validation of the wheel
                    twine check dist/*
                '''
            }
        }
        
        stage('Copy Packages') {
            steps {
                script {
                    def buildDate = new Date().format('yyyyMMdd')
                    def targetSubDir = "${TARGET_DIR}/${buildDate}_${VERSION}"
                    
                    sh """
                        mkdir -p ${targetSubDir}
                        cp dist/* ${targetSubDir}/
                        echo "Packages copied to ${targetSubDir}"
                        ls -la ${targetSubDir}
                    """
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
            script {
                echo """Build successful!
                    Version: ${VERSION}
                    Artifacts location: ${TARGET_DIR}
                """
            }
        }
        failure {
            script {
                echo 'Build failed. Check logs for details.'
                // You might want to add notification here
                // emailext or slackSend for notifications
            }
        }
    }
}
