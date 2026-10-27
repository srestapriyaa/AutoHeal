pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'AutoHeal source code is ready!'
            }
        }

        stage('Check Project Files') {
            steps {
                sh 'ls -la'
                sh 'test -f app.py'
                sh 'test -f monitor.py'
                sh 'test -f Dockerfile'
                echo 'All required project files are present!'
            }
        }

        stage('Validate Python Syntax') {
            steps {
                sh 'python3 -m py_compile app.py monitor.py'
                echo 'Python syntax validation passed!'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t autoheal:latest .'
            }
        }
    }

    post {
        success {
            echo 'AutoHeal pipeline completed successfully!'
        }
        failure {
            echo 'AutoHeal pipeline failed. Check the build logs.'
        }
    }
}
