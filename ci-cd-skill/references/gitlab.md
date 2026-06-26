# GitLab CI Reference

Use this reference for `.gitlab-ci.yml`.

## Common Structure

Prefer:

```yaml
stages:
  - build
  - deploy

variables:
  DOCKER_BUILDKIT: "1"

build_image:
  stage: build
  tags:
    - shell
  rules:
    - if: '$CI_COMMIT_BRANCH'
  before_script:
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"
  script:
    - docker buildx build --tag "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA" --push .

deploy_dev:
  stage: deploy
  tags:
    - shell
  when: manual
  needs:
    - build_image
  script:
    - ssh "$DEPLOY_USER@$DEPLOY_HOST" "cd '$DEPLOY_PATH' && docker compose pull && docker compose up -d"
```

Adapt to the project's runner. Shell runners can use host Docker; Docker runners often need Docker-in-Docker or a remote builder.

## Docker Buildx Pattern

When the project builds images and pushes to GitLab Registry:

- Use `docker login` with `CI_REGISTRY_USER`, `CI_REGISTRY_PASSWORD`, `CI_REGISTRY`.
- Tag every image with `$CI_COMMIT_SHORT_SHA`.
- Add service-specific tags when multiple Dockerfiles exist, for example `photos-$CI_COMMIT_SHORT_SHA` and `ops-$CI_COMMIT_SHORT_SHA`.
- Use `latest` or `ops-latest` only as a convenience tag, not as the only deploy reference.
- Use `--ssh=default` only when Dockerfile build steps need private Git or private package access.

Example adapted from a two-image project:

```yaml
build_photos_image:
  stage: build
  tags:
    - shell
  when: manual
  before_script:
    - eval "$(ssh-agent -s)"
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"
  script:
    - docker buildx build --tag "$CI_REGISTRY_IMAGE:photos-$CI_COMMIT_SHORT_SHA" --tag "$CI_REGISTRY_IMAGE:photos-latest" --ssh=default -f Dockerfile . --push

build_ops_image:
  stage: build
  tags:
    - shell
  when: manual
  before_script:
    - eval "$(ssh-agent -s)"
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"
  script:
    - docker buildx build --tag "$CI_REGISTRY_IMAGE:ops-$CI_COMMIT_SHORT_SHA" --tag "$CI_REGISTRY_IMAGE:ops-latest" --ssh=default -f Dockerfile_ops . --push
```

## Deploy Pattern

Use `needs`, not `dependencies`, for modern job ordering unless artifacts are required.

For SSH plus docker compose:

```yaml
deploy_dev:
  stage: deploy
  environment:
    name: dev
  tags:
    - shell
  when: manual
  needs:
    - build_photos_image
  before_script:
    - eval "$(ssh-agent -s)"
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh
    - echo "$SSH_KNOWN_HOSTS" > ~/.ssh/known_hosts
  script:
    - |
      ssh "$DEPLOY_USER@$DEPLOY_HOST" "sed -i.bak 's/^PHOTOS_VERSION=.*/PHOTOS_VERSION=${CI_COMMIT_SHORT_SHA}/' '$DEPLOY_PATH/.env'"
      ssh "$DEPLOY_USER@$DEPLOY_HOST" "cd '$DEPLOY_PATH' && docker compose up -d"
```

For config sync:

```yaml
deploy_dev_config:
  stage: deploy
  environment:
    name: dev
  tags:
    - shell
  when: manual
  before_script:
    - eval "$(ssh-agent -s)"
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh
    - echo "$SSH_KNOWN_HOSTS" > ~/.ssh/known_hosts
  script:
    - rsync -az --delete ./conf/app/dev/ "$DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH/conf/app/"
    - ssh "$DEPLOY_USER@$DEPLOY_HOST" "cd '$DEPLOY_PATH' && docker compose restart app"
```

## Variables To Document

List these in `deploy/ci-cd-config.md` when used:

- `SSH_PRIVATE_KEY`: deploy key or build key, protected/masked.
- `SSH_KNOWN_HOSTS`: output of `ssh-keyscan <host>`.
- `DEPLOY_USER`, `DEPLOY_HOST`, `DEPLOY_PATH`.
- `CI_REGISTRY_*`: built-in GitLab registry variables.
- Service-specific variables such as `PHOTOS_VERSION` or `OPS_VERSION`.

## Pitfalls

- Avoid `docker login -p $PASSWORD` without quotes.
- Avoid unverified SSH hosts; use `SSH_KNOWN_HOSTS`.
- Avoid deploying `latest` to production when a commit tag exists.
- Avoid sharing one deploy job across unrelated services unless rollback behavior is identical.
