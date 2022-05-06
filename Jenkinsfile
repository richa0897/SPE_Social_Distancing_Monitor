pipeline {
  agent any
   environment {
        imageName = ""
  }
  stages {
    
    stage('GIT CLONE') {
      steps {
        git url: 'https://github.com/AnkD21-me/SPE_Social_Distancing_Monitor.git', branch: 'master'
      }
    }
     
     stage('Build') {
        steps {
          echo 'building'
        }
    }

    stage('Build Docker_Image'){
        steps {
            script {
                imageName = docker.build "richavarma/mlops_repo:latest"
                }
            }
    }
    
    stage('Push Docker Image')
    {
        steps {
            script{
                docker.withRegistry('','credentials-Id') {
                imageName.push()
                }
            }
        }
    }
    
    stage('Deploy using Ansible'){
            steps{
                ansiblePlaybook becomeUser: yes, ansiblePlaybook becomePassword: infear, colorized: true, disableHostKeyChecking: true, installation: 'Ansible', inventory: 'inventory', playbook: 'p2.yml', sudoUser: null
            }
        }
      
  }
}
