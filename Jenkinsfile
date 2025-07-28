pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-discriminant:latest'
        APP_CONTAINER_NAME = 'flask_discriminant_app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Vlados752/app_tms.git'
            }
        }
        
        stage('Lint') {
            steps {
                script {
                    docker.image('python:3.10').inside('-u root') {
                        sh 'pip install flake8'
                        sh 'flake8 .'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    sh "docker rm -f ${APP_CONTAINER_NAME} || true"
                    sh "docker run -d --name ${APP_CONTAINER_NAME} -p 5000:5000 ${DOCKER_IMAGE}"
                    // подождать, пока контейнер стартует
                    sleep(time: 5, unit: 'SECONDS')
                }
            }
        }

stage('Test Application') {
    steps {
        script {
            sh """
                docker exec ${APP_CONTAINER_NAME} sh -c '
                    if command -v curl > /dev/null; then
                        echo "curl already installed";
                    else
                        apt-get update && apt-get install -y curl;
                    fi
                '

                docker exec ${APP_CONTAINER_NAME} sh -c '
                    STATUS_CODE=\$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/)
                    echo "Status code: \$STATUS_CODE"
                    if [ "\$STATUS_CODE" -ne 200 ]; then
                        echo "❌ Unexpected response code"
                        exit 1
                    else
                        echo "✅ Application running correctly"
                        exit 0
                    fi
                '
            """
        }
    }
}

        stage('Archive HTML Response') {
            steps {
                script {
                   sh """
                       docker exec ${APP_CONTAINER_NAME} sh -c 'apk add --no-cache curl || apt-get update && apt-get install -y curl'
                       docker exec ${APP_CONTAINER_NAME} sh -c '
                           curl -s http://localhost:5000/ > /response.html
                       '
                       docker cp ${APP_CONTAINER_NAME}:/response.html response.html
                   """
                   archiveArtifacts artifacts: 'response.html', fingerprint: true
                }
            }
        }

        stage('Notify Telegram') {
            steps {
                withCredentials([
                    string(credentialsId: 'TELEGRAM_BOT_TOKEN', variable: 'BOT_TOKEN'),
                    string(credentialsId: 'TELEGRAM_CHAT_ID', variable: 'CHAT_ID')
                ]) {
                    sh """
                        curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendDocument" \
                            -F chat_id=${CHAT_ID} \
                            -F document=@response.html \
                            -F caption="✅ HTML-ответ от Flask-приложения"
                    """
                }
            }
        }        
    }

    post {
          failure {
              withCredentials([
                  string(credentialsId: 'TELEGRAM_BOT_TOKEN', variable: 'BOT_TOKEN'),
                  string(credentialsId: 'TELEGRAM_CHAT_ID', variable: 'CHAT_ID')
              ]) {
                  sh """
                      curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \\
                          -d chat_id=${CHAT_ID} \\
                          -d text="❌ Ошибка: пайплайн *flask-discriminant* завершился неудачей!" \\
                          -d parse_mode=Markdown
                  """
              }
          }
    }
}
