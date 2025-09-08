pipeline {
    agent any

    tools {
        maven 'maven3'
        jdk 'jdk17'
    }

    stages {
        stage('Build') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh 'mvn clean package'
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'target/*.war', fingerprint: true
                }
            }
        }

        stage('Test') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh 'mvn test jacoco:report'
                }
            }
        }

        stage('Code Analysis - Checkstyle') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh 'mvn checkstyle:checkstyle'
                }
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

        stage('Nexus Artifact Upload') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    nexusArtifactUploader artifacts: [[artifactId: 'vprofile', classifier: '', file: 'target/vprofile-v2.war', type: 'war']],
                                          credentialsId: 'nexus',
                                          groupId: 'V3',
                                          nexusUrl: '192.168.184.128:8081',
                                          nexusVersion: 'nexus3',
                                          protocol: 'http',
                                          repository: 'patel-repo-release',
                                          version: "${env.BUILD_ID}-${env.BUILD_TIMESTAMP}"
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    script {
                        def scannerHome = tool 'sonarscanner'   // Ensure this name matches the Global Tool Configuration
                        withSonarQubeEnv('sonarserver') {
                            sh """
                                ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=vprofile \
                                -Dsonar.projectVersion=1.0 \
                                -Dsonar.sources=src \
                                -Dsonar.java.binaries=target/classes \
                                -Dsonar.java.checkstyle.reportPaths=target/checkstyle-result.xml \
                                -Dsonar.coverage.jacoco.reportPaths=target/jacoco.exec \
                                -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
                            """
                        }
                    }
                }
            }
        }


        // Optional stage: Deployment to Kubernetes (commented out)
        stage('Deploy to K8s') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    git branch: 'skelkube', url: env.GIT_URL
                    withCredentials([file(credentialsId: 'k8s', variable: 'KUBECONFIG')]) {
                        dir('kubedefs') {
                            sh 'kubectl delete -f .'
                        }
                    }
                }
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