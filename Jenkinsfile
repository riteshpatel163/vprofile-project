pipeline {
    agent any
    
    tools {
        maven 'maven3'
        jdk 'jdk17'
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
            post {
                always {
                    script {
                        def surefireReports = findFiles(glob: 'target/surefire-reports/*.xml')
                        if (surefireReports.length > 0) {
                            junit 'target/surefire-reports/*.xml'
                        } else {
                            echo 'No test reports found - tests may have failed or not run'
                        }
                    }
                }
            }
        }
        
        stage('Code Analysis - Checkstyle') {
            steps {
                sh 'mvn checkstyle:checkstyle'
            }
            post {
                always {
                    publishCheckstyle pattern: 'target/checkstyle-result.xml'
                    script {
                        if (fileExists('target/checkstyle-result.xml')) {
                            def checkstyleResult = readFile('target/checkstyle-result.xml')
                            if (checkstyleResult.contains('error')) {
                                echo "⚠️ Checkstyle found issues in ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
                            }
                        }
                    }
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