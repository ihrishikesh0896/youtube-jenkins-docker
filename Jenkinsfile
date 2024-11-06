pipeline {
    agent any
    
    environment {
        VENV = 'venv'
        TARGET_DIR = '/var/jenkins_home/artifacts'
        // More robust version extraction with error handling
        VERSION = sh(
            script: '''
                if [ -f setup.py ]; then
                    python3 setup.py --version || echo "0.0.0"
                else
                    echo "0.0.0"
                fi
            ''',
            returnStdout: true
        ).trim()
        // Add Python version specification
        PYTHON_VERSION = '3.9'  // Specify your required Python version
    }
    
    options {
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    stages {
        stage('Check Python Installation') {
            steps {
                script {
                    def pythonVersion = sh(
                        script: 'python3 --version || echo "Python not found"',
                        returnStdout: true
                    ).trim()
                    if (!pythonVersion.contains(PYTHON_VERSION)) {
                        error "Required Python version ${PYTHON_VERSION} not found. Found: ${pythonVersion}"
                    }
                    echo "Using Python: ${pythonVersion}"
                }
            }
        }

        stage('Debug Git Setup') {
            steps {
                script {
                    sh '''
                        echo "Current working directory: $(pwd)"
                        echo "Repository contents:"
                        ls -la
                        
                        if git rev-parse --git-dir > /dev/null 2>&1; then
                            echo "Git repository information:"
                            git status
                            git remote -v
                            echo "Current branch: $(git branch --show-current)"
                            echo "Latest commit: $(git log -1 --oneline)"
                        else
                            echo "Not a git repository!"
                            exit 1
                        fi
                    '''
                }
            }
        }
        
        stage('Prepare Environment') {
            steps {
                script {
                    // Add error handling for virtual environment creation
                    sh '''
                        if [ -d "${VENV}" ]; then
                            echo "Removing existing virtual environment"
                            rm -rf ${VENV}
                        fi
                        
                        echo "Creating new virtual environment"
                        python3 -m venv ${VENV} || {
                            echo "Failed to create virtual environment"
                            exit 1
                        }
                        
                        if [ ! -d "${TARGET_DIR}" ]; then
                            echo "Creating target directory"
                            mkdir -p ${TARGET_DIR}
                            chmod 755 ${TARGET_DIR}
                        fi
                    '''
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''#!/bin/bash
                    source ${VENV}/bin/activate || {
                        echo "Failed to activate virtual environment"
                        exit 1
                    }
                    
                    echo "Upgrading pip and installing basic tools"
                    python -m pip install --upgrade pip wheel setuptools twine || exit 1
                    
                    if [ -f requirements.txt ]; then
                        echo "Installing project dependencies"
                        python -m pip install -r requirements.txt || exit 1
                        # Freeze dependencies for reproducibility
                        python -m pip freeze > requirements.lock
                    else
                        echo "No requirements.txt found - skipping dependency installation"
                    fi
                '''
            }
        }
        
        stage('Build Package') {
            steps {
                sh '''#!/bin/bash
                    source ${VENV}/bin/activate || exit 1
                    
                    echo "Cleaning previous builds"
                    rm -rf dist/ build/ *.egg-info
                    
                    echo "Building package"
                    python setup.py sdist bdist_wheel || {
                        echo "Package build failed"
                        exit 1
                    }
                    
                    echo "Built packages:"
                    ls -l dist/
                '''
            }
        }
        
        stage('Test Package') {
            steps {
                sh '''#!/bin/bash
                    source ${VENV}/bin/activate || exit 1
                    
                    echo "Validating built distributions"
                    twine check dist/* || {
                        echo "Package validation failed"
                        exit 1
                    }
                    
                    # Add additional test commands here
                    if [ -f pytest.ini ] || [ -d tests ]; then
                        echo "Running tests"
                        pytest tests/ || exit 1
                    fi
                '''
            }
        }
        
        stage('Copy Packages') {
            steps {
                script {
                    def buildDate = new Date().format('yyyyMMdd')
                    def targetSubDir = "${TARGET_DIR}/${buildDate}_${VERSION}"
                    
                    sh """
                        if [ -d dist ] && [ "\$(ls -A dist)" ]; then
                            echo "Creating target directory: ${targetSubDir}"
                            mkdir -p ${targetSubDir}
                            
                            echo "Copying packages"
                            cp dist/* ${targetSubDir}/
                            
                            echo "Copied packages:"
                            ls -la ${targetSubDir}
                            
                            # Create manifest file
                            {
                                echo "Build Date: ${buildDate}"
                                echo "Version: ${VERSION}"
                                echo "Git Commit: \$(git rev-parse HEAD)"
                                echo "Git Branch: \$(git branch --show-current)"
                                echo "Python Version: \$(python3 --version)"
                            } > ${targetSubDir}/build_info.txt
                        else
                            echo "No packages found in dist directory"
                            exit 1
                        fi
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
                    Build Date: ${new Date().format('yyyy-MM-dd HH:mm:ss')}
                """
            }
        }
        failure {
            script {
                def failureMessage = """Build failed!
                    Job: ${env.JOB_NAME}
                    Build Number: ${env.BUILD_NUMBER}
                    Check console output at: ${env.BUILD_URL}
                """
                echo failureMessage
                
                // Uncomment and configure as needed:
                // emailext (
                //     subject: "Build Failed: ${env.JOB_NAME}",
                //     body: failureMessage,
                //     to: 'team@example.com'
                // )
                
                // slackSend(
                //     color: 'danger',
                //     message: failureMessage
                // )
            }
        }
    }
}
