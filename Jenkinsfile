pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                git branch: 'main', url: 'https://github.com/Oussmane-D/projet_lead_jedha-bootcamp.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using the Dockerfile
                    sh 'docker build -t ml-pipeline-image .'
                }
            }
        }

        stage('Run Tests Inside Docker Container') {
            steps {
                withCredentials([
                    string(credentialsId: 'mlflow-tracking-uri', variable: 'MLFLOW_TRACKING_URI'),
                    string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY'),
                    string(credentialsId: 'backend-store-uri', variable: 'BACKEND_STORE_URI'),
                    string(credentialsId: 'artifact-root', variable: 'ARTIFACT_ROOT')
                ]) {
                    // Write environment variables to a temporary file
                    // KEEP SINGLE QUOTE FOR SECURITY PURPOSES (MORE INFO HERE: https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#handling-credentials)
                    script {
                        writeFile file: 'env.list', text: '''
                        MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
                        AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                        AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                        BACKEND_STORE_URI=$BACKEND_STORE_URI
                        ARTIFACT_ROOT=$ARTIFACT_ROOT
                        '''
                    }

                    // Run a temporary Docker container and pass env variables securely via --env-file
                    sh '''
                    docker run --rm --env-file env.list \
                    ml-pipeline-image \
                    bash -c "pytest --maxfail=1 --disable-warnings"
                    '''
                }
            }
        }
    }

    post {
        always {
            // Clean up workspace and remove dangling Docker images
            sh 'docker system prune -f'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}


pipeline {
    agent any
    environment {
        MLFLOW_URL = 'https://mlflow.huggingface.co'   ousmane-d/mlflow-sserver-demo
        MLFLOW_TRACKING_TOKEN = credentials('MLFLOW_TOKEN')  // Si vous utilisez un token d'accès sécurisé
    }
    stages {
        stage('Test') {
            steps {
                sh 'pytest tests/'  // Exécution des tests
            }
        }
        stage('Log Metrics to MLflow') {
            steps {
                script {
                    // Lancer une expérimentation sur MLflow via l'API
                    sh """
                    curl -X POST ${MLFLOW_URL}/api/2.0/mlflow/runs/log-metric \
                        -H 'Authorization: Bearer ${MLFLOW_TRACKING_TOKEN}' \
                        -H 'Content-Type: application/json' \
                        -d '{
                            "run_id": "run_id_value",
                            "key": "accuracy",
                            "value": 0.95,
                            "timestamp": $(date +%s),
                            "step": 1
                        }'
                    """
                }
            }
        }
    }
}
