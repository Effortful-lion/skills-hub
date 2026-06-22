# Docker Image And Deploy Reference

Use this reference when CI/CD builds container images or deploys through SSH, rsync, docker compose, or similar scripts.

## Image Tagging

Use at least one immutable tag:

- GitLab: `$CI_COMMIT_SHORT_SHA`
- GitHub: `${{ github.sha }}`
- Jenkins: `env.GIT_COMMIT.take(8)`

Optional mutable tags:

- `latest` for default service image.
- `<service>-latest` for multi-service repos.
- `<branch>` or `<env>` tags for development convenience.

Production deploys should prefer immutable commit tags so rollback is explicit.

## SSH Build Secrets

Use SSH forwarding only when Docker build needs private dependencies:

```bash
eval "$(ssh-agent -s)"
echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
docker buildx build --ssh=default ...
```

Do not copy private keys into Docker build context. Make sure `.dockerignore` excludes `.git`, local env files, credentials, and build outputs that are not needed.

## Compose Deploy Route

The common deploy route is:

1. Build and push image.
2. SSH to deploy host.
3. Update `.env` or compose override with the new image tag.
4. Run `docker compose pull` when compose references remote images.
5. Run `docker compose up -d`.
6. Optionally run a health check and show rollback command.

Example:

```bash
ssh "$DEPLOY_USER@$DEPLOY_HOST" "sed -i.bak 's/^APP_VERSION=.*/APP_VERSION=${IMAGE_TAG}/' '$DEPLOY_PATH/.env'"
ssh "$DEPLOY_USER@$DEPLOY_HOST" "cd '$DEPLOY_PATH' && docker compose pull && docker compose up -d"
```

## Config Sync Route

Use `rsync` when config files live in repo and should be copied to the host:

```bash
rsync -az --delete ./conf/app/dev/ "$DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH/conf/app/"
ssh "$DEPLOY_USER@$DEPLOY_HOST" "cd '$DEPLOY_PATH' && docker compose restart app"
```

Be careful with `--delete`; use it only when the source directory fully owns the destination.

## Safety Defaults

- Add `set -euo pipefail` in multi-line shell scripts when the platform shell supports it.
- Quote variables.
- Keep build secrets separate from deploy secrets.
- Use `known_hosts`; do not disable host checking for long-lived pipelines.
- Document rollback as redeploying a previous commit tag.
