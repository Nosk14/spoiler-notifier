node() {
    def image_name = "spoiler-notifier"
    def image = null
    stage('Checkout') {
        checkout scm
    }

    stage('Build') {
        image = docker.build("${image_name}:${env.BUILD_ID}")
    }

    stage('Deploy'){
        try{
            sh "docker stop ${image_name} && docker rm ${image_name}"
        }catch(Exception e){
            echo e.getMessage()
        }
        withCredentials([string(credentialsId: 'bob-telegram-token', variable: 'token')]) {
            withCredentials([string(credentialsId: 'tutano-telegram-channel', variable: 'telegram_channel')]) {
                def runArgs = '\
-e "BOT_TOKEN=$token" \
-e "TELEGRAM_CHAT=$telegram_channel" \
-v /home/carlos/mtg:/usr/local/etc \
--restart unless-stopped \
--name ' + image_name

                def container = image.run(runArgs)
            }
        }
    }
}