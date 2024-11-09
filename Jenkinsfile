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
                    rm -rf ${VENV}
                    python3 -m venv ${VENV}
                    . ${VENV}/bin/activate
                    python3 -m pip install --upgrade pip
                    python3 -m pip install wheel setuptools twine pytest
                    python3 -m pip list
                    deactivate
                '''
            }
        }

        stage('Check Python Installation') {
            steps {
                script {
                    def pythonVersion = sh(
                        script: '''
                            . ${VENV}/bin/activate
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
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    . ${VENV}/bin/activate
                    python -m pip install --upgrade pip wheel setuptools twine || exit 1
                    
                    if [ -f requirements.txt ]; then
                        python -m pip install -r requirements.txt || exit 1
                        python -m pip freeze > requirements.lock
                    else
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
                    . ${VENV}/bin/activate
                    rm -rf dist/ build/ *.egg-info
                    
                    if [ -f setup.py ]; then
                        python setup.py sdist bdist_wheel || exit 1
                    else
                        cat > setup.py << EOF
from setuptools import setup, find_packages
setup(
    name="my-python-app",
    version="${VERSION}",
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
                    
                    deactivate
                '''
            }
        }
        
        stage('Test Package') {
            steps {
                sh '''
                    . ${VENV}/bin/activate
                    if [ -d "dist" ] && [ "$(ls -A dist)" ]; then
                        twine check dist/* || exit 1
                    else
                        exit 1
                    fi
                
                    if [ -f pytest.ini ] || [ -d test ]; then
                        pip install pytest
                        pip install -e .
                        pytest test/ || exit 1
                    else
                        echo "No test found - skipping test stage"
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
                            mkdir -p ${targetSubDir}
                            cp dist/* ${targetSubDir}/
                            ls -la ${targetSubDir}
                            {
                                echo "Build Date: ${buildDate}"
                                echo "Version: ${VERSION}"
                                echo "Git Commit: \$(git rev-parse HEAD)"
                                echo "Git Branch: \$(git branch --show-current)"
                                echo "Python Version: \$(python3 --version)"
                            } > ${targetSubDir}/build_info.txt
                        else
                            exit 1
                        fi
                    """
                }
            }
        }

        stage('Security Scan') {
            steps {
                script {
                    def targetSubDir = "${TARGET_DIR}/security-reports"
                    sh "mkdir -p ${targetSubDir}"
                    
                    sh '''
                        . ${VENV}/bin/activate
                        python -m pip install --upgrade pip
                        python -m pip install semgrep --verbose
                        
                        cat << EOF > .semgrepignore
                        venv/
                        .venv/
                        env/
                        virtualenv/
                        build/
                        dist/
                        *.egg-info/
                        __pycache__/
                        *.pyc
                        *.pyo
                        *.pyd
                        .Python
                        .pytest_cache/
                        .coverage
                        htmlcov/
                        .git/
                        .gitignore
                        .env
                        .idea/
                        .vscode/
                        *.swp
                        *.swo
                        docs/
                        *.md
                        *.rst
                        tests/
                        test_*.py
                        EOF
                        
                        semgrep --test
                        
                        semgrep scan \
                            --config "p/python" \
                            --config "p/security-audit" \
                            --config "p/owasp-top-ten" \
                            --exclude-dir .venv \
                            --output ${targetSubDir}/semgrep-results.txt \
                            --verbose \
                            . || echo "Security audit completed with findings"
                        
                        semgrep scan \
                            --config "p/python" \
                            --config "p/security-audit" \
                            --config "p/owasp-top-ten" \
                            --json \
                            --output ${targetSubDir}/semgrep-results.json \
                            . || echo "JSON report generation completed"
                        
                        deactivate
                    '''
                    
                    archiveArtifacts(
                        artifacts: "${targetSubDir}/**,.semgrepignore",
                        allowEmptyArchive: true,
                        fingerprint: true
                    )
                }
            }
            post {
                always {
                    script {
                        if (fileExists("${TARGET_DIR}/security-reports/semgrep-results.txt")) {
                            def findingsCount = sh(
                                script: "grep -c '^  ■' ${TARGET_DIR}/security-reports/semgrep-results.txt || true",
                                returnStdout: true
                            ).trim()
                            echo "Found ${findingsCount} security findings"
                        } else {
                            echo "Warning: No security scan results file found"
                        }
                    }
                }
                failure {
                    error "Security scan stage failed. Check the logs for details."
                }
            }
        }
    }
    
    post {
        always {
            sh 'rm -rf ${VENV}'
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
