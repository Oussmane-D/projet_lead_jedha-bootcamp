pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out the code..."
                git branch: 'main', url: 'https://github.com/Oussmane-D/projet_lead_jedha-bootcamp.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building the Docker image..."
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
                    script {
                        // Log the content of env.list to check for issues
                        echo "Creating the env.list file with environment variables..."
                        writeFile file: 'env.list', text: """
                        MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
                        AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                        AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                        BACKEND_STORE_URI=$BACKEND_STORE_URI
                        ARTIFACT_ROOT=$ARTIFACT_ROOT
                        """
                        sh 'cat env.list'  // Display the content of the env.list file

                        echo "Running tests inside Docker..."
                        sh '''
                        docker run --rm --env-file env.list \
                        ml-pipeline-image \
                        bash -c "pytest --maxfail=1 --disable-warnings"
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up Docker system..."
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
