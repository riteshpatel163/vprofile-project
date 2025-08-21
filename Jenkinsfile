pipeline {
    agent any
    tools {
        maven "maven3"
        jdk "jdk21"
    }
    
    environment {
        
        SNAP_REPO = 'vprofile-snapshot'
        NEXUS_USER = 'admin'
        NEXUS_PASS = 'redhat'
        RELEASE_REPO = 'patel-repo-release'
        CENTRAL_REPO = 'patel-maven-central'
        NEXUSIP = '192.168.181.128'
        NEXUSPORT = '8081'
        NEXUS_GRP_REPO = 'patel-maven-group'
        NEXUS_LOGIN = 'nexus'
        SONARSERVER='sonarserver'
        SONARSCANNER='sonarscanner'
    }

    stages {
        stage('fetching from git'){
            steps{
              git branch: 'jenkins-ci', url: 'https://github.com/hkhcoder/vprofile-project.git'
            }
            
        }
        stage('Build') {
            steps {
                sh 'mvn -s settings.xml -DskipTests install'
            }
            post {
                success {
                    echo "Now Archiving."
                    archiveArtifacts artifacts: '**/*.war'
                }
            }
        }

        stage('Test') {
            steps {
                sh 'mvn -s settings.xml test'
            }
        }

        stage('Checkstyle Analysis') {
            steps {
                sh 'mvn -s settings.xml checkstyle:checkstyle'
            }
        }

        stage('Sonar Analysis') {
            steps {
                script {
                    def scannerHome = tool "${SONARSCANNER}"
                    

                    withSonarQubeEnv("${SONARSERVER}") {
                        sh "${scannerHome}/bin/sonar-scanner " +
                           "-Dsonar.projectKey=vprofile " +
                           "-Dsonar.projectName=vprofile " +
                           "-Dsonar.projectVersion=1.0 " +
                           "-Dsonar.sources=src/ " +
                           "-Dsonar.java.binaries=target/test-classes/com/visualpathit/account/controllerTest/ " +
                           "-Dsonar.junit.reportsPath=target/surefire-reports/ " +
                           "-Dsonar.jacoco.reportsPath=target/jacoco.exec "
                           // You may re-enable the lines below if needed:
                           // + "-Dsonar.java.checkstyle.reportPaths=target/checkstyle-result.xml "
                           // + "-Dsonar.nodejs.executable=${nodePath}"
                    }
                }
            }
            post {
                success {
                    echo "Sonar Analysis completed successfully."
                }
                failure {
                    echo "Sonar Analysis failed."
                }
            }
        }
    }
}
