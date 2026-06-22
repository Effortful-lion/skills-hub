# Jenkins Pipeline Reference

Use this reference for `Jenkinsfile`.

## Common Structure

Prefer declarative pipeline unless the project already uses scripted pipeline:

```groovy
pipeline {
  agent { label 'docker' }

  options {
    timestamps()
    disableConcurrentBuilds()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  environment {
    IMAGE = "registry.example.com/team/app:${env.GIT_COMMIT.take(8)}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'registry-creds', usernameVariable: 'REGISTRY_USER', passwordVariable: 'REGISTRY_PASSWORD')]) {
          sh '''
            docker login -u "$REGISTRY_USER" -p "$REGISTRY_PASSWORD" registry.example.com
            docker buildx build --tag "$IMAGE" --push .
          '''
        }
      }
    }

    stage('Deploy Dev') {
      when {
        branch 'main'
      }
      steps {
        input message: 'Deploy to dev?'
        sshagent(credentials: ['deploy-ssh-key']) {
          sh 'ssh deploy@example.com "cd /data/deploy/app && docker compose pull && docker compose up -d"'
        }
      }
    }
  }
}
```

## Credentials

Use Jenkins Credentials, not plaintext environment variables:

- `usernamePassword` for registry.
- `sshUserPrivateKey` or `sshagent` for deploy hosts.
- `string` for tokens.
- Folder credentials when teams/environments need separation.

## Deployment Gates

- Use `input` before staging/prod deploys when the user wants manual approval.
- Use `when { branch 'main' }` or tag conditions for release pipelines.
- Use `disableConcurrentBuilds()` when deployments touch the same environment.

## Docker Notes

Make sure the Jenkins agent can run Docker or talks to a remote builder. If Docker socket access is unavailable, propose Kaniko, BuildKit remote builder, or a platform-specific image builder.

## Pitfalls

- Avoid storing deploy paths or hosts only in shell scripts without documenting them.
- Avoid one global credential for all environments.
- Avoid concurrent deploys to the same compose project.
- Avoid scripted pipeline unless the control flow truly needs it.
