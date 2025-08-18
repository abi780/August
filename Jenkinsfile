pipeline {
    agent any
 
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        DOCKER_IMAGE = "docker.io/abinaya780/flask-demo"
        KUBECONFIG_CREDENTIALS = credentials('kubeconfig-demo')
    }

      stages {
        stage('Clone Code') {
            steps {
                sshagent(['github-ssh']) {
                    sh 'git clone -b main git@github.com:abi780/August.git .'
                }
            }
        }
 
        stage('Build & Push Docker Image') {
            steps {
                script {
                    sh """
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                    docker build -t $DOCKER_IMAGE:${BUILD_NUMBER} .
                    docker push $DOCKER_IMAGE:${BUILD_NUMBER}
                    docker tag $DOCKER_IMAGE:${BUILD_NUMBER} $DOCKER_IMAGE:latest
                    docker push $DOCKER_IMAGE:latest
                    """
                }
            }
        }
       stage('Update Deployment YAML') {
           steps {
                script {
                      sh """
                      sed -i 's|image: ${DOCKER_IMAGE}:.*|image: ${DOCKER_IMAGE}:${BUILD_NUMBER}|' k8s/deployment.yaml
                      """
              }    
            }
          }
        stage('Commit & Push Changes') {
            steps {
                script {
                    sh """
                        git config user.email "ci-bot@myorg.com"
                        git config user.name "CI Bot"
                        git add k8s/deployment.yaml
                        git commit -m "Update image to ${DOCKER_IMAGE}:${BUILD_NUMBER}" || echo "No changes to commit"
                        git push origin main
                    """
                }
            }
        }
 
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh """
                    mkdir -p ~/.kube
                    cp $KUBECONFIG_CREDENTIALS ~/.kube/config
                    kubectl create namespace demo-cicd --dry-run=client -o yaml | kubectl apply -f -
                    sed -i 's|<your-dockerhub-username>|${DOCKERHUB_CREDENTIALS_USR}|g' k8s/deployment.yaml
                    kubectl apply -f k8s/
                    kubectl rollout status deployment/flask-demo -n demo-cicd
                    """
                }
            }
        }
    }
}
