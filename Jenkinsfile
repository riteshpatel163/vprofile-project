pipeline {
    agent any
    tools {
        maven "maven3"
        jdk "jdk21"
    }
    parameters {
        string(name: 'ENVIRONMENT', defaultValue: 'dev', description: 'Deployment environment')
    }
    environment {
        
        SNAP_REPO = 'vprofile-snapshot'
        NEXUS_USER = 'admin'
        NEXUS_PASS = 'redhat'
        RELEASE_REPO = 'patel-repo-release'
        CENTRAL_REPO = 'patel-maven-central'
        NEXUSIP = '192.168.184.128'
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
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=vprofile \
                            -Dsonar.projectName=vprofile \
                            -Dsonar.projectVersion=1.0 \
                            -Dsonar.sources=src/ \
                            -Dsonar.java.binaries=target/test-classes/com/visualpathit/account/controllerTest/ \
                            -Dsonar.junit.reportsPath=target/surefire-reports/ \
                            -Dsonar.jacoco.reportsPath=target/jacoco.exec \
                            -Dsonar.java.checkstyle.reportPaths=target/checkstyle-result.xml
                        """
                    }
                }
            }
            post {
                success {
                    echo "Sonar Analysis completed ssssuccessfully."
                    echo "now archiving"
                    archiveArtifacts artifacts: '**/*.war'
                }
                failure {
                    echo "Sonar Analysises failed."
                }
            }
        }
        stage('deploy to tomcat server'){
            
            steps {
                script {
                    if (params.ENVIRONMENT == 'dev') {
                       
                        echo "Deploying to dev environment."
                        sh ''' rm -rf /opt/tomcat9/webapps/vprofile-v2.war
                            cp -rv target/vprofile-v2.war /opt/tomcat9/webapps/
                            chown -R tomcat:tomcat-deploy /opt/tomcat9/webapps/
                        '''

                }else {
                    echo "Deployment skipped. Not in dev environment."
                }
            
                }
            }
        }
        stage('nexus artifact upload') {
            steps {
                nexusArtifactUploader(
                    nexusVersion: 'nexus3',
                    protocol: 'http',
                    nexusUrl: "${NEXUSIP}:${NEXUSPORT}",
                    groupId: 'QA',
                    version: "${env.BUILD_ID}-${env.BUILD_TIMESTAMP}",
                    repository: "${RELEASE_REPO}",
                    credentialsId: "${NEXUS_LOGIN}",
                    artifacts: [
                        [artifactId: 'vprofile',
                        classifier: '',
                        file: 'target/vprofile-v2.war',
                        type: 'war']
                    ]
                )
            }
            
        }
    }
}
