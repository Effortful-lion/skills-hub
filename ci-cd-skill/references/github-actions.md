# GitHub Actions Reference

Use this reference for `.github/workflows/ci-cd.yml`.

## Common Structure

Prefer separate jobs for build and deploy:

```yaml
name: CI/CD

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  packages: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.sha }}
            ghcr.io/${{ github.repository }}:latest

  deploy-dev:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: dev
    steps:
      - name: Deploy
        run: ssh "$DEPLOY_USER@$DEPLOY_HOST" "cd '$DEPLOY_PATH' && docker compose pull && docker compose up -d"
        env:
          DEPLOY_USER: ${{ secrets.DEPLOY_USER }}
          DEPLOY_HOST: ${{ secrets.DEPLOY_HOST }}
          DEPLOY_PATH: ${{ secrets.DEPLOY_PATH }}
```

## Secrets And Environments

- Use repository or environment secrets for credentials.
- Use GitHub Environments for deploy approvals, especially staging/prod.
- Set `permissions` explicitly; do not rely on broad defaults.
- Use `workflow_dispatch` when the user wants manual build/deploy buttons.

For SSH deploys, add an SSH agent step:

```yaml
- uses: webfactory/ssh-agent@v0.9.0
  with:
    ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
- name: Trust deploy host
  run: |
    mkdir -p ~/.ssh
    echo "${{ secrets.SSH_KNOWN_HOSTS }}" > ~/.ssh/known_hosts
```

## Docker And Registry

Use GHCR by default for GitHub-hosted repos unless the user names another registry.

For multiple images, use `docker/build-push-action` once per Dockerfile or a matrix when the build arguments are similar:

```yaml
strategy:
  matrix:
    service:
      - name: photos
        dockerfile: Dockerfile
      - name: ops
        dockerfile: Dockerfile_ops
```

Tag images with `${{ github.sha }}` and optionally `service-latest`. For human readability, also add branch or release tags when useful.

## Pitfalls

- Do not put deployment secrets in normal `env` at workflow top level.
- Do not grant `packages: write` to deploy-only jobs.
- Do not auto-deploy pull requests from forks.
- Avoid unpinned third-party actions for sensitive deploy pipelines unless the repo already accepts that tradeoff.
