pipeline {
    agent any
    
    tools {
        maven 'maven3'
        jdk 'jdk17'
    }
    
    environment {
        SONAR_SERVER = 'sonarserver'
        SONAR_SCANNER = 'sonarscanner'
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
                script {
                    def scannerHome = tool "${SONAR_SCANNER}"
                    withSonarQubeEnv("${SONAR_SERVER}") {
                        sh '''
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=vprofile \
                            -Dsonar.projectVersion=1.0 \
                            -Dsonar.sources=src \
                            -Dsonar.java.binaries=target/classes \
                            -Dsonar.java.checkstyle.reportPaths=target/checkstyle-result.xml \
                            -Dsonar.coverage.jacoco.reportPaths=target/jacoco.exec \
                            -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
                        '''
                    }
                }
            }
        }
        stage('nexus artifact upload') {

            steps {
                nexusArtifactUploader artifacts: [[artifactId: 'vprofile-new', classifier: '', file: 'target/vprofile-v2.war', type: 'war']], credentialsId: 'nexus', groupId: 'V2', nexusUrl: 'http://rhel.local:8081', nexusVersion: 'nexus2', protocol: 'http', repository: 'patel-repo-release', version: '1.0'
            }
        }
        
        stage('Always Run Stage') {
            steps {
                echo "This stage runs regardless of previous stage success or failure"
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