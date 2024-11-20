pipeline {
    agent any
    
    environment {
        VENV = 'venv'
        ARTIFACTS = '/var/jenkins_home/artifacts'
        VERSION = '0.1.0'
        PYTHON = 'python3'
        BUILD_DATE = sh(script: 'date +%Y%m%d', returnStdout: true).trim()
    }
    
    stages {

        // stage('Setup') {
        //     steps {
        //         sh """
        //             rm -rf ${VENV}
        //             ${PYTHON} -m venv ${VENV}
        //             . ${VENV}/bin/activate
        //             pip install --upgrade pip wheel setuptools twine pytest flake8 safety semgrep
        //             deactivate
        //         """
        //     }
        // }

        stage('Debug Git Configuration') {
                steps {
                    sh """
                        echo "Checking Git version..."
                        git --version
            
                        echo "Checking Git configuration..."
                        git config --list
            
                        echo "Checking current directory..."
                        pwd
            
                        echo "Checking Git branch..."
                        git branch --show-current
                    """
                }
        }
        
        stage('Sensitive Data Scan') {
            steps {
                script {
                    sh """
                        #######--------- Showing Actual Branch ---------#######
                        ls -la
                        git branch --show-current
                        # Assuming the sensitive data scan script is named 'scan_secrets.py' and is located in the project directory.
                        # The script scans for sensitive data and automatically creates a branch if any secrets are found.
                        echo "Running sensitive data scan..."
                        /var/SecretSanitizer/env/bin/python3 /var/SecretSanitizer/main.py -repo-path ${WORKSPACE} || echo "Sensitive data scan completed"
                    """
                }
            }
        }
        
    //     stage('Setup') {
    //         steps {
    //             sh """
    //                 rm -rf ${VENV}
    //                 ${PYTHON} -m venv ${VENV}
    //                 . ${VENV}/bin/activate
    //                 pip install --upgrade pip wheel setuptools twine pytest flake8 safety semgrep
    //                 deactivate
    //             """
    //         }
    //     }

        
    //     stage('Security Scan') {
    //         steps {
    //             script {
    //                 sh """
    //                     . ${VENV}/bin/activate
    //                     mkdir -p ${ARTIFACTS}/security

    //                     semgrep scan \
    //                         --config=p/python \
    //                         --config=p/security-audit \
    //                         --config=p/owasp-top-ten \
    //                         --output=/var/jenkins_home/artifacts/security/results.txt \
    //                         --metrics=off \
    //                         --timeout=300 \
    //                         --jobs=auto \
    //                         . --json > /var/jenkins_home/artifacts/security/results.json || echo "JSON report generation completed"
                        
    //                     deactivate
    //                 """
                    
    //                 archiveArtifacts artifacts: "${ARTIFACTS}/security/**", allowEmptyArchive: true
    //             }
    //         }
    //     }

    //     stage('Build & Test') {
    //         steps {
    //             sh """
    //                 . ${VENV}/bin/activate
                    
    //                 # Install dependencies
    //                 [ -f requirements.txt ] && pip install -r requirements.txt
                    
    //                 # Lint and Security Check
    //                 flake8 . --exclude=${VENV},dist || echo "Linting issues found"
    //                 safety check || echo "Security issues found"
                    
    //                 # Build package
    //                 rm -rf dist build *.egg-info
    //                 if [ ! -f setup.py ]; then
    //                     echo "Creating setup.py"
    //                     echo 'from setuptools import setup, find_packages; setup(name="app", version="'${VERSION}'", packages=find_packages())' > setup.py
    //                 fi
    //                 python setup.py sdist bdist_wheel
                    
    //                 # Test
    //                 pip install -e .
    //                 twine check dist/*
    //                 [ -d test ] && pytest test/
                    
    //                 deactivate
    //             """
    //         }
    //     }

    //     stage('Deploy') {
    //         steps {
    //             script {
    //                 def targetDir = "${ARTIFACTS}/${BUILD_DATE}_${VERSION}"
    //                 sh """
    //                     mkdir -p ${targetDir}
    //                     cp dist/* ${targetDir}/
    //                     echo "Build: ${BUILD_DATE}_${VERSION}
    //                     Commit: \$(git rev-parse HEAD)
    //                     Branch: \$(git branch --show-current)" > ${targetDir}/build_info.txt
    //                 """
    //             }
    //         }
    //     }
     }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo "Build successful! Version: ${VERSION}, Location: ${ARTIFACTS}/${BUILD_DATE}_${VERSION}"
        }
        failure {
            echo "Build failed! Check: ${env.BUILD_URL}"
        }
    }
}
