pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                checkout([$class: 'GitSCM', 
                          branches: [[name: '*/main']], 
                          userRemoteConfigs: [[
                              url: 'git@github.com:abi780/August.git',
                              credentialsId: 'github-ssh'
                          ]]
                ])
            }
        }
    }
}
