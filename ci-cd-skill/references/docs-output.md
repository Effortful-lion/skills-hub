# Documentation Output Reference

Use this reference when creating the required Markdown docs.

## Config Explanation: `docs/ci-cd-config.md`

Keep it short and tied to generated files.

Recommended sections:

```markdown
# CI/CD 配置说明

## 文件

- `.gitlab-ci.yml`: ...
- `.github/workflows/ci-cd.yml`: ...
- `Jenkinsfile`: ...

## 流程

1. 构建: ...
2. 推送镜像/产物: ...
3. 部署: ...

## 变量与密钥

| 名称 | 平台位置 | 用途 | 示例/说明 |
| --- | --- | --- | --- |
| SSH_PRIVATE_KEY | CI Secret | SSH 登录部署机 | masked/protected |

## 环境

| 环境 | 触发方式 | 部署目标 | 说明 |
| --- | --- | --- | --- |
| dev | 手动/自动 | ... | ... |

## 注意事项

- ...
```

## Quick Start: `docs/ci-cd-quick-start.md`

Place this after the config explanation work. It should teach the user's operating route, not generic CI theory.

Recommended sections:

```markdown
# CI/CD 快速开始

## 目标路线

代码提交 -> 自动构建 -> 推送镜像/产物 -> 手动或自动部署 -> 验证服务

## 第一次配置

1. 配置 Runner/Agent。
2. 配置 Registry。
3. 添加 Secrets。
4. 确认部署机目录和 compose 文件。
5. 运行一次构建。
6. 运行一次部署。

## 日常操作

### 自动构建

说明触发分支、产物命名、在哪里查看日志。

### 手动部署

说明点击哪个 job/workflow/stage，部署哪个环境，如何确认成功。

### 配置更新

说明只同步配置时走哪条 job。

## 回滚

说明如何选择上一个 commit tag 或镜像 tag 重新部署。

## 排错清单

- Registry 登录失败: ...
- SSH 失败: ...
- 镜像拉取失败: ...
- docker compose 未更新: ...
```

## Writing Rules

- Use Chinese for project docs unless the repo is clearly English-only.
- Mention placeholders clearly, for example `<DEPLOY_HOST>` or `TODO: 替换为实际部署目录`.
- Do not expose real secrets.
- Keep docs actionable: every listed operation should say where to click or which command/job to run.
