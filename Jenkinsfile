stage('Clone Code') {
    steps {
        checkout([$class: 'GitSCM', 
                  branches: [[name: '*/main']], 
                  userRemoteConfigs: [[
                      url: 'git@github.com:abi780/ci-cd-demo-flask.git',
                      credentialsId: 'github-ssh'
                  ]]
        ])
    }
}
