---
name: ci-cd-skill
description: Use when creating, reviewing, or explaining CI/CD configuration for GitLab CI, GitHub Actions, Jenkins, Docker image build/push, environment deploys, secrets, pipeline docs, or quick-start automation routes for a project.
---

# 项目CI/CD配置

## Overview

Use this skill to produce project-specific CI/CD configuration and the two documents that make it usable: a short config explanation and a final quick-start guide for the whole build/deploy route.

Prefer the project's existing conventions. Do not replace working pipelines wholesale unless the user asks for a redesign. Keep standard CI/CD config files in their native locations, and always place generated Markdown docs under the project-root `deploy/` directory. Create `deploy/` first if it does not exist.

## Workflow

1. Inspect the project before writing files: language/framework, package manager, Dockerfiles, compose files, deployment scripts, existing `.gitlab-ci.yml`, `.github/workflows/*`, `Jenkinsfile`, docs, env examples, and README.
2. Identify the user's platform and runner model: GitLab CI, GitHub Actions, Jenkins, or mixed. If unspecified, infer from existing files; otherwise ask one concise question only when the choice changes output filenames.
3. Select and read the relevant references:
   - GitLab CI: `references/gitlab.md`
   - GitHub Actions: `references/github-actions.md`
   - Jenkins Pipeline: `references/jenkins.md`
   - Docker image build, registry, SSH deploy, compose deploy: `references/docker-image-and-deploy.md`
   - Required docs and quick-start structure: `references/docs-output.md`
4. Generate or update the CI/CD config file with conservative defaults:
   - Build and deploy are separate jobs/stages.
   - Production deploys are manual unless the user explicitly wants fully automatic release.
   - Secrets come from platform variables/secrets/credentials, never plaintext repo files.
   - Images use immutable tags such as commit SHA plus optional environment/latest tags.
   - Repeated shell blocks are factored only when the platform supports it clearly.
   - Do not relocate standard platform config files just to unify output paths.
   - If the repository already has working CI/CD config, preserve its behavior and change only the minimum needed scope.
5. Create or update a short config explanation document at `deploy/ci-cd-config.md`.
6. Create or update a final learning-oriented quick-start document at `deploy/ci-cd-quick-start.md`, with a clear route for automated build and deployment.
   - Write both docs in concise, newcomer-friendly Chinese unless the repo is clearly English-only.
   - Keep the modules logically ordered so a new maintainer can follow setup, trigger, deploy, rollback, and troubleshooting without extra background reading.
7. Validate syntax where tools are available, and at minimum run formatting/lint-safe checks such as YAML parse, `git diff --check`, or platform CLI validation if configured.

## Required Discovery

Gather these facts and reflect them in generated docs:

- Platform: GitLab, GitHub Actions, Jenkins, or mixed.
- Runner/agent: shell runner, Docker runner, GitHub hosted runner, self-hosted runner, Jenkins agent label.
- Build artifact: Docker image, binary, static files, package, or multiple services.
- Registry: GitLab registry, GHCR, Docker Hub, private registry, or internal Harbor.
- Environments: dev/test/staging/prod and which should be manual.
- Deployment method: SSH plus docker compose, Kubernetes, rsync, cloud CLI, or custom script.
- Required secrets: registry credentials, SSH key, known hosts, deploy host/user/path, cloud credentials, environment variables.

If a fact is unknown, choose a safe placeholder and mark it clearly in the generated docs. Prefer placeholders that are easy for a new owner to search and replace.

## Output Contract

For each user request, produce only files that fit the selected platform:

- GitLab: `.gitlab-ci.yml`
- GitHub Actions: `.github/workflows/ci-cd.yml`
- Jenkins: `Jenkinsfile`
- Docs: `deploy/ci-cd-config.md` and `deploy/ci-cd-quick-start.md`

When editing an existing repo, keep unrelated pipeline behavior intact. Do not move or rename existing standard CI/CD config files unless the user explicitly requests that restructuring. Add comments only where future maintainers need to replace placeholders or understand a non-obvious deploy step.

## Review Checklist

Before finishing, verify:

- No secret value is committed.
- Build can run without deploy permissions.
- Deploy job uses the image or artifact created by the build job.
- Manual gates exist for risky environments.
- Cache does not hide dependency lockfile changes.
- Image tags are traceable to a commit.
- Docs explain required variables/secrets and the normal operating path.
