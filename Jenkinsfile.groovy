pipeline {
    agent any

    environment {
        // ───────────────────────────────────────────────
        // Kubernetes
        KUBECONFIG_CRED_ID  = 'kubeconfig-my-cluster'     // Jenkins credential ID
        NAMESPACE           = 'demo-app'

        // ───────────────────────────────────────────────
        // Artifactory / Helm
        ARTIFACTORY_CRED_ID = 'artifactory-deploy-user'
        ARTIFACTORY_URL     = 'https://artifactory.company.local'
        HELM_REPO_NAME      = 'helm-charts'
        HELM_CHART_NAME     = 'simple-webapp'
        HELM_CHART_VERSION  = '0.3.2'                     // or use 'latest'

        // ───────────────────────────────────────────────
        // Maven component
        MAVEN_COMPONENT_DIR = 'backend'

        // ───────────────────────────────────────────────
        // Git repo for updating README.md
        GIT_REPO_URL        = 'https://github.com/pradipt/demo-project.git'
        GIT_CRED_ID         = 'github-token-jenkins'
        README_PATH         = 'README.md'
    }

    stages {
        stage('Pre-Deployment Checks') {
            steps {
                echo 'Running pre-deployment checks...'
                checkout scm

                sh 'mvn --version'
                sh 'helm version'
                sh 'kubectl version --client'
                sh 'git --version'

                echo 'Pre-checks completed.'
            }
        }

        stage('Build Component') {
            steps {
                echo 'Building the backend component...'
                dir(MAVEN_COMPONENT_DIR) {
                    sh 'mvn clean install -DskipTests'
                }
                echo 'Build finished.'
            }
        }

        stage('Fetch and Deploy Helm Chart') {
            steps {
                echo 'Deploying Helm chart from Artifactory...'

                withCredentials([usernamePassword(
                    credentialsId: ARTIFACTORY_CRED_ID,
                    usernameVariable: 'ART_USER',
                    passwordVariable: 'ART_PASS'
                )]) {
                    sh """
                        helm repo add ${HELM_REPO_NAME} ${ARTIFACTORY_URL}/api/helm/${HELM_REPO_NAME} \
                            --username ${ART_USER} \
                            --password ${ART_PASS} \
                            --force-update
                    """

                    sh 'helm repo update'

                    sh """
                        helm pull ${HELM_REPO_NAME}/${HELM_CHART_NAME} \
                            --version ${HELM_CHART_VERSION} \
                            --untar=false
                    """
                }

                withCredentials([file(credentialsId: KUBECONFIG_CRED_ID, variable: 'KUBECONFIG')]) {
                    sh """
                        helm upgrade --install simple-webapp \
                            ${HELM_CHART_NAME}-${HELM_CHART_VERSION}.tgz \
                            --namespace ${NAMESPACE} \
                            --create-namespace \
                            --kubeconfig ${KUBECONFIG} \
                            --wait --timeout 5m
                    """

                    sh """
                        kubectl rollout status deployment/simple-webapp \
                            --namespace ${NAMESPACE} \
                            --kubeconfig ${KUBECONFIG} \
                            --timeout=300s
                    """
                }

                echo 'Deployment done.'
            }
        }

        stage('Post-Deployment Checks') {
            steps {
                echo 'Verifying deployment...'
                withCredentials([file(credentialsId: KUBECONFIG_CRED_ID, variable: 'KUBECONFIG')]) {
                    sh "kubectl get pods -n ${NAMESPACE} --kubeconfig ${KUBECONFIG}"
                    sh "kubectl get svc -n ${NAMESPACE} --kubeconfig ${KUBECONFIG}"
                }
                echo 'Post-checks passed (basic verification).'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
            sh 'rm -f *.tgz || true'
        }

        success {
            echo 'Deployment successful — updating README.md'

            withCredentials([usernamePassword(
                credentialsId: GIT_CRED_ID,
                usernameVariable: 'GIT_USER',
                passwordVariable: 'GIT_TOKEN'
            )]) {
                sh """
                    git config --global user.email "jenkins@company.local"
                    git config --global user.name "Jenkins CI"

                    rm -rf temp-repo || true
                    git clone ${GIT_REPO_URL} temp-repo
                    cd temp-repo

                    echo "" >> ${README_PATH}
                    echo "## Last successful deployment" >> ${README_PATH}
                    echo "- Date: \$(date '+%Y-%m-%d %H:%M:%S %Z')" >> ${README_PATH}
                    echo "- Build: #\${BUILD_NUMBER}" >> ${README_PATH}
                    echo "- Chart version: ${HELM_CHART_VERSION}" >> ${README_PATH}

                    git add ${README_PATH}
                    git commit -m "docs: record successful deployment #\${BUILD_NUMBER}" || echo "Nothing to commit"
                    git push https://${GIT_USER}:${GIT_TOKEN}@${GIT_REPO_URL#https://} HEAD:main
                """
            }
        }

        failure {
            echo 'Pipeline failed :('
        }
    }
}