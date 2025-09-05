pipeline {
    agent any
    
    tools {
        maven 'maven3'
        jdk 'jdk17'
    }
    
    environment {
        SONAR_SERVER = 'sonarserver'
        SONAR_SCANNER = tool 'sonarscanner'
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'target/*.war', fingerprint: true
                }
            }
        }
        
        stage('Test') {
            steps {
                sh 'mvn test jacoco:report'
            }
        }
        
        stage('Code Analysis - Checkstyle') {
            steps {
                sh 'mvn checkstyle:checkstyle'
            }
            post {
                success {
                    echo "Checkstyle analysis completed successfully."
                }
                failure {
                    echo "Checkstyle analysis failed."
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarserver') {
                    sh '''mvn sonar:sonar \
                        -Dsonar.projectKey=vprofile \
                        -Dsonar.projectName=vprofile \
                        -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml \
                        -Dsonar.java.checkstyle.reportPaths=target/checkstyle-result.xml'''
                }
            }
        }
    }
    
    post {
        success {
            echo "✅ Pipeline succeeded: ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
        }
        failure {
            echo "❌ Pipeline failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
        }
    }
}