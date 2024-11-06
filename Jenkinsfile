pipeline {
    agent any
    
    environment {
        VENV = 'venv'
        TARGET_DIR = '/var/jenkins_home/artifacts'
        VERSION = '0.1.0'
        PYTHON_VERSION = '3.11'
        SEMGREP_RULES = "p/python p/security-audit p/owasp-top-ten"
    }
    
    stages {
        stage('Setup Virtual Environment') {
            steps {
                sh '''
                    # Remove existing virtual environment if it exists
                    rm -rf venv
                    
                    # Create new virtual environment
                    python3 -m venv venv
                    
                    # Activate virtual environment and install basic packages
                    . venv/bin/activate
                    python3 -m pip install --upgrade pip
                    python3 -m pip install wheel setuptools twine pytest
                    
                    # Verify installation
                    python3 -m pip list
                    
                    # Deactivate virtual environment
                    deactivate
                '''
            }
        }

        stage('Check Python Installation') {
            steps {
                script {
                    def pythonVersion = sh(
                        script: '''
                            . venv/bin/activate
                            python3 --version
                            deactivate
                        ''',
                        returnStdout: true
                    ).trim()
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
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    . venv/bin/activate
                    
                    echo "Upgrading pip and installing basic tools"
                    python -m pip install --upgrade pip wheel setuptools twine || exit 1
                    
                    if [ -f requirements.txt ]; then
                        echo "Installing project dependencies"
                        python -m pip install -r requirements.txt || exit 1
                        # Freeze dependencies for reproducibility
                        python -m pip freeze > requirements.lock
                    else
                        echo "No requirements.txt found - creating minimal requirements"
                        echo "wheel>=0.37.1" > requirements.txt
                        echo "setuptools>=65.5.1" >> requirements.txt
                        python -m pip install -r requirements.txt || exit 1
                    fi
                    
                    deactivate
                '''
            }
        }
        
        stage('Build Package') {
            steps {
                sh '''
                    . venv/bin/activate
                    
                    echo "Cleaning previous builds"
                    rm -rf dist/ build/ *.egg-info
                    
                    echo "Building package"
                    if [ -f setup.py ]; then
                        python setup.py sdist bdist_wheel || {
                            echo "Package build failed"
                            exit 1
                        }
                    else
                        echo "No setup.py found - creating minimal setup.py"
                        cat > setup.py << EOF
from setuptools import setup, find_packages

setup(
    name="my-python-app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("requirements.txt")
        if line.strip() and not line.startswith("#")
    ],
)
EOF
                        python setup.py sdist bdist_wheel || exit 1
                    fi
                    
                    echo "Built packages:"
                    ls -l dist/
                    
                    deactivate
                '''
            }
        }
        
        stage('Test Package') {
            steps {
                sh '''
                    . venv/bin/activate
                    
                    echo "Validating built distributions"
                    if [ -d "dist" ] && [ "$(ls -A dist)" ]; then
                        twine check dist/* || {
                            echo "Package validation failed"
                            exit 1
                        }
                    else
                        echo "No distributions found to validate"
                        exit 1
                    fi
                    
                    # Run tests if they exist
                    if [ -f pytest.ini ] || [ -d tests ]; then
                        echo "Installing pytest"
                        pip install pytest
                        echo "Running tests"
                        pytest tests/ || exit 1
                    else
                        echo "No tests found - skipping test stage"
                    fi
                    
                    deactivate
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

        stage('Security Scan') {
            steps {
                script {
                    sh "mkdir -p security-reports"
                    
                    sh '''
                        # Install semgrep in the virtual environment
                        . venv/bin/activate
                        pip install semgrep
                        
                        # Create .semgrepignore file
                        cat << EOF > .semgrepignore
                        # Python virtual environment
                        venv/
                        .venv/
                        env/
                        
                        # Build directories
                        build/
                        dist/
                        *.egg-info/
                        
                        # Cache directories
                        __pycache__/
                        .pytest_cache/
                        .coverage
                        htmlcov/
                        
                        # Other common ignores
                        .git/
                        node_modules/
                        *.min.js
                        *.pyc
                        
                        # Test files
                        tests/
                        test_*.py
                        
                        # Documentation
                        docs/
                        *.md
                        EOF
                        
                        echo "Running Semgrep security scan..."
                        
                        # Generate human-readable report
                        semgrep scan \
                            --config "p/python" \
                            --config "p/security-audit" \
                            --config "p/owasp-top-ten" \
                            --output security-reports/semgrep-results.txt \
                            --verbose \
                            .
                        
                        deactivate
                        
                        # Print summary
                        echo "Security Scan Summary:"
                        echo "===================="
                        if [ -f security-reports/semgrep-results.txt ]; then
                            grep "findings" security-reports/semgrep-results.txt || echo "No findings summary available"
                        fi
                    '''
                    
                    archiveArtifacts artifacts: 'security-reports/**,.semgrepignore', allowEmptyArchive: true
                }
            }
            post {
                always {
                    script {
                        if (fileExists('security-reports/semgrep-results.txt')) {
                            def findingsCount = sh(
                                script: 'grep -c "^  ■" security-reports/semgrep-results.txt || true',
                                returnStdout: true
                            ).trim()
                            echo "Security scan completed with ${findingsCount} findings."
                        }
                    }
                }
                failure {
                    error "Security scan failed. Please check the logs for details."
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up workspace...'
            sh 'rm -rf venv'  // Clean up virtual environment
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
            }
        }
    }
}
