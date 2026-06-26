# Complexity Guide

Use this guide only when the repository contains mixed signals and you need a default threshold for what to recommend.

## Simple

Typical signals:
- static site, docs site, browser-only app, CLI, or single-process service
- no persistent user data or only disposable data
- one runtime, one deploy target, few environment variables

Usually recommend:
- one run/build/deploy path
- one env example or setup note
- one smoke-check or health-check step
- one rollback or redeploy note if deploys can fail visibly

Usually do not recommend yet:
- full CI/CD pipelines
- paging and on-call workflows
- heavy monitoring stacks
- formal change management

## Moderate

Typical signals:
- database-backed app
- auth, billing, file storage, cron jobs, queues, or third-party webhooks
- multiple deploy steps or multiple environments

Usually recommend:
- migration and rollback path
- backup or export strategy for important data
- deploy checklist with verification steps
- basic logs and at least one production health signal
- one or two release scripts if they remove repeated manual risk

Usually do not recommend yet:
- large platform re-architecture
- team-style incident bureaucracy

## Higher risk

Typical signals:
- revenue-critical flows
- irreversible data writes
- multiple services or workers
- production incidents would be expensive or hard to recover from

Usually recommend:
- tested rollback path
- backup restore confidence, not just backup existence
- migration safety plan
- clear ownership of alerts or failure checks
- automation where manual release risk is already causing mistakes

Still avoid:
- process that exists only to imitate larger teams
- tools that add maintenance burden without improving recovery or visibility
