pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        DOCKER_IMAGE = "docker.io/abinaya780/flask-demo"
        KUBECONFIG_CREDENTIALS = credentials('kubeconfig-demo')
        GIT_REPO = "https://github.com/abi780/August.git"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: "${GIT_REPO}"
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    IMAGE_TAG = "v${env.BUILD_NUMBER}"
                    IMAGE = "${DOCKER_IMAGE}:${IMAGE_TAG}"

                    sh """
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                    docker build -t ${IMAGE} .
                    docker push ${IMAGE}
                    docker tag ${IMAGE} ${DOCKER_IMAGE}:latest
                    docker push ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Update Deployment YAML') {
            steps {
                script {
                    // update image in deployment.yaml
                    sh """
                        sed -i 's|image: ${DOCKER_IMAGE}:.*|image: ${IMAGE}|' k8s/deployment.yaml
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
                        git commit -m "Update image to ${IMAGE}" || echo "No changes to commit"
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
                    kubectl apply -f k8s/
                    kubectl rollout status deployment/flask-demo -n demo-cicd
                    """
                }
            }
        }
    }
}
