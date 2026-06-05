# AI-Coding 操作手册

## 一、操作模块

### 0. 任务分级

```text
S 级：文案、样式、小 bug，直接实现。
M 级：单页面、单组件、单接口，轻量 OpenSpec + spec2super + Superpowers。
L 级：完整业务功能，完整 OpenSpec + spec2super + Superpowers。
XL 级：架构、权限、支付、数据模型、核心链路，完整流程并分阶段执行。
```

### 1. 需求进入

```text
确认 change-name。
确认任务级别。
确认是否进入 OpenSpec。
确认不直接写代码。
```

### 2. 用 OpenSpec 做需求落地

快速路径：

```text
/opsx:propose <change-name-or-description>
```

展开路径：

```text
/opsx:new <change-name>
/opsx:ff <change-name>
```

必须生成：

```text
openspec/changes/<change-name>/proposal.md
openspec/changes/<change-name>/design.md
openspec/changes/<change-name>/tasks.md
openspec/changes/<change-name>/specs/**/*.md
```

### 3. 检查 OpenSpec 产物

```text
检查 proposal.md 是否包含目标、范围、非范围。
检查 specs/**/*.md 是否包含 Requirement 和 Scenario。
检查 design.md 是否包含技术方案和关键决策。
检查 tasks.md 是否覆盖 specs 和 design。
检查是否存在阻塞 Superpowers planning 的缺失信息。
```

不通过时：

```text
回到 OpenSpec 修正。
不进入 spec2super。
不写代码。
```

### 4. 用 spec2super 做需求翻译

调用：

```text
Use $spec2super to generate a Superpowers-ready translation for <change-name>.
```

必须生成：

```text
openspec/changes/<change-name>/translation.md
```

必须检查：

```text
translation.md 已读取 proposal.md。
translation.md 已读取 design.md。
translation.md 已读取 tasks.md。
translation.md 已读取 specs/**/*.md。
translation.md 保留 Original OpenSpec Task Input。
translation.md 生成 Engineering-Oriented Task Order。
translation.md 将 tasks.md 从需求/功能模块顺序转换为工程依赖顺序。
translation.md 对无法安全推断的依赖保留原顺序并标注。
translation.md 列出 Planning Gaps。
translation.md 明确下一步使用 superpowers:writing-plans。
```

不通过时：

```text
修正 translation.md。
不进入 Superpowers。
不写代码。
```

### 5. 用 Superpowers 生成工程计划

调用：

```text
Use superpowers:writing-plans with openspec/changes/<change-name>/translation.md as the approved spec input.
Do not reinterpret requirements, change scope, or add design decisions.
Save the plan to docs/superpowers/plans/YYYY-MM-DD-<change-name>.md.
```

必须生成：

```text
docs/superpowers/plans/YYYY-MM-DD-<change-name>.md
```

必须检查：

```text
plan 有标准 header。
plan 有文件结构映射。
plan 有 bite-sized checkbox steps。
plan 有精确文件路径。
plan 有具体代码或命令。
plan 有 TDD 步骤。
plan 有验证方式。
plan 有 commit 步骤。
plan 没有 TODO / TBD / 稍后实现。
```

不通过时：

```text
修正 Superpowers plan。
不进入执行。
```

### 6. 用 Superpowers 做工程落地

优先调用：

```text
Use superpowers:subagent-driven-development to execute docs/superpowers/plans/YYYY-MM-DD-<change-name>.md.
```

无子代理时调用：

```text
Use superpowers:executing-plans to execute docs/superpowers/plans/YYYY-MM-DD-<change-name>.md.
```

执行要求：

```text
按 plan task-by-task 执行。
按 step-by-step 执行。
写测试。
运行失败测试。
写最小实现。
运行通过测试。
重构。
运行验证。
提交或准备提交。
记录失败和修复。
遇到规格冲突时停止。
遇到计划缺口时停止。
遇到重复失败时停止。
```

### 7. 做产品质量保证

Superpowers 侧：

```text
Use superpowers:verification-before-completion.
Use superpowers:requesting-code-review if needed.
Use superpowers:finishing-a-development-branch when ready.
```

OpenSpec 侧：

```text
/opsx:verify <change-name>
```

必须检查：

```text
tasks.md 全部完成。
specs/**/*.md 的 Requirement 都有实现。
Scenario 有测试或手动验证证据。
design.md 与实现一致。
没有未说明的 scope creep。
核心路径通过。
失败路径通过。
权限路径通过。
loading 状态通过。
empty 状态通过。
error 状态通过。
移动端验收通过。
lint 通过。
typecheck 通过。
test 通过。
build 通过。
```

不通过时：

```text
回到 Superpowers plan 或执行阶段修复。
修复后重新验证。
```

### 8. 做发布前检查

```text
检查环境变量。
检查数据库 migration。
检查 API 兼容性。
检查权限配置。
检查第三方服务配置。
检查日志和监控。
检查错误上报。
检查性能风险。
检查回滚方案。
检查 release notes。
检查版本号或 build number。
检查部署目标环境。
```

### 9. 做部署

```text
部署到开发环境。
运行 smoke test。
部署到测试环境或 staging。
运行回归测试。
运行核心业务路径测试。
确认日志无异常。
确认监控无异常。
确认错误上报无新增异常。
确认产品负责人或自己验收通过。
部署到生产环境。
运行生产 smoke test。
观察监控。
记录部署结果。
```

### 10. 做归档

```text
/opsx:archive <change-name>
```

必须确认：

```text
OpenSpec delta specs 已同步到 openspec/specs/。
change 已移动到 openspec/changes/archive/。
proposal.md 已保留。
design.md 已保留。
tasks.md 已保留。
specs/**/*.md 已保留。
translation.md 已保留。
Superpowers plan 已保留。
验证结果已保留。
部署结果已记录。
```

### 11. 常用提示词

生成 OpenSpec：

```text
使用 OpenSpec 为这个需求创建 change。
先不要写代码。
请生成 proposal.md、design.md、specs/、tasks.md。
```

生成 translation：

```text
Use $spec2super to generate a Superpowers-ready translation for <change-name>.
只做 OpenSpec 到 Superpowers 的格式转换。
允许将 tasks.md 从需求/功能模块顺序转换为工程依赖顺序。
不要改变 OpenSpec 的内容大意。
如果缺失 Superpowers planning 所需信息，写入 Planning Gaps，不要补猜。
```

生成 Superpowers plan：

```text
Use superpowers:writing-plans with openspec/changes/<change-name>/translation.md as the approved spec input.
Do not reinterpret requirements, change scope, or add design decisions.
```

执行 Superpowers plan：

```text
Use superpowers:subagent-driven-development to execute docs/superpowers/plans/YYYY-MM-DD-<change-name>.md task-by-task.
```

验证和归档：

```text
先执行 Superpowers completion verification，再执行 /opsx:verify <change-name>。
确认 specs、design、tasks、translation、plan 与实现一致后，执行 /opsx:archive <change-name>。
```

### 12. 卡口清单

Spec Gate：

```text
proposal.md 存在。
design.md 存在。
tasks.md 存在。
specs/**/*.md 存在。
scope / out-of-scope 明确。
requirements / scenarios 可验证。
```

Translation Gate：

```text
translation.md 已生成。
所有 specs requirements 已出现。
所有 tasks checkbox 已出现。
工程顺序只重排任务意图，没有新增任务语义。
每个重排原因都有 OpenSpec 依据，或已标注无法安全推断。
design 决策未被改写。
Planning Gaps 已显式列出。
translation 明确要求下一步使用 superpowers:writing-plans。
```

Build Gate：

```text
docs/superpowers/plans/YYYY-MM-DD-<change-name>.md 存在。
plan 有精确文件路径。
plan 有具体测试/验证命令。
plan 是 checkbox task-by-task 格式。
plan 没有 TODO / TBD / 稍后实现。
```

Quality Gate：

```text
lint 通过。
typecheck 通过。
test 通过。
build 通过。
核心路径通过。
失败路径通过。
权限路径通过。
UI 状态通过。
移动端通过。
code review 通过。
OpenSpec verify 通过或已处理 warning。
```

Release Gate：

```text
环境变量确认。
migration 确认。
监控确认。
错误上报确认。
回滚方案确认。
staging 验收确认。
生产 smoke test 确认。
```

Close Gate：

```text
Superpowers 验证通过。
OpenSpec verify 已执行或等价检查已完成。
specs requirements 与实现一致。
design 与实现一致，或已明确处理偏差。
没有未说明的 scope creep。
部署结果已记录。
/opsx:archive 已完成。
```

## 二、理解模块

### 1. 工作流总览

这套工作流把 AI Coding 拆成三个明确职责：

```text
OpenSpec：需求落地
spec2super：需求到工程的翻译
Superpowers：工程落地
```

OpenSpec 负责把用户需求变成稳定的规格产物。spec2super 负责把 OpenSpec 产物整理成 Superpowers 能消费的工程输入。Superpowers 负责把工程输入变成可执行计划，并通过 TDD、审查、验证完成代码交付。

### 2. 为什么要分三层

AI Coding 最大的问题不是 AI 不会写代码，而是 AI 容易在不同阶段混淆职责。

如果直接让 AI 根据需求写代码，它可能会：

- 自己补需求。
- 自己改范围。
- 自己换技术方案。
- 先写 UI，后发现数据和权限没定义。
- 说完成了，但没有验证证据。

三层拆分后，每一层只做自己的事情：

- OpenSpec 让需求先稳定。
- spec2super 让交接格式稳定。
- Superpowers 让工程执行稳定。

### 3. OpenSpec 是什么

OpenSpec 是规格层。它的作用是让 AI 和人先对“做什么”达成一致，再进入工程实现。

一个 OpenSpec change 通常包含：

```text
proposal.md
specs/**/*.md
design.md
tasks.md
```

这些文件一起描述一次变更的原因、范围、行为规格、技术方案和任务清单。

### 4. proposal.md 是什么

`proposal.md` 是变更提案。

它回答：

- 为什么做这个需求。
- 这次做什么。
- 这次不做什么。
- 大致采用什么方向。

它的价值是锁定意图和范围。没有 proposal，AI 很容易扩大需求。

### 5. specs/**/*.md 是什么

`specs/**/*.md` 是行为规格增量。

它通常包含：

```text
ADDED Requirements
MODIFIED Requirements
REMOVED Requirements
Scenario
```

Requirement 描述系统必须具备的行为。Scenario 描述这个行为在具体场景下如何被验证。

它的价值是让功能可验收。没有 specs，AI 写出来的代码可能看似完成，但无法判断是否满足需求。

### 6. design.md 是什么

`design.md` 是技术设计。

它回答：

- 技术方案是什么。
- 架构决策是什么。
- 数据流或状态流是什么。
- 明确提到哪些文件或模块会变化。

它的价值是锁定关键技术决策。没有 design，Superpowers 可能重新设计一套方案。

### 7. tasks.md 是什么

`tasks.md` 是 OpenSpec 视角的任务清单。

它通常按需求、能力、功能模块组织。例如：

```text
1. 用户模块
2. 认证模块
3. UI 模块
4. 测试模块
```

它的作用是确认 OpenSpec 认为这次变更要完成哪些事项。

但它不一定适合作为工程执行顺序。需求视角可能先列功能模块，工程视角却需要先做依赖模块。

### 8. 为什么需要 spec2super

OpenSpec 的输出是需求和规格视角。Superpowers 的输入需要工程计划视角。

两者中间需要一个翻译层，也就是 `spec2super`。

`spec2super` 的目标不是重新设计需求，而是生成：

```text
openspec/changes/<change-name>/translation.md
```

这个文件把 OpenSpec 的 proposal、specs、design、tasks 转成 Superpowers 更容易理解和规划的输入。

### 9. translation.md 是什么

`translation.md` 是 OpenSpec 到 Superpowers 的交接文件。

它包含：

- Source Artifacts。
- Proposal Input。
- Specification Input。
- Design Input。
- Original OpenSpec Task Input。
- Engineering-Oriented Task Order。
- Planning Gaps。
- Instructions For Superpowers Planning。

它不是最终实现计划。最终实现计划由 Superpowers 的 `writing-plans` 生成。

### 10. 为什么 translation.md 要保留 Original OpenSpec Task Input

保留原始任务输入，是为了让后续审查能看到 OpenSpec 原本的任务表达。

这样可以判断工程重排有没有改变原意。

### 11. 为什么 translation.md 要生成 Engineering-Oriented Task Order

OpenSpec 的 `tasks.md` 可能按需求模块排列，但工程开发通常要按依赖顺序排列。

例如：

```text
先做 schema / type / config / data model
再做 API / service / state
再做 UI / page / interaction
最后做测试、验收、部署检查
```

这样做可以减少返工，避免先写上层功能后发现底层依赖不存在。

### 12. 工程依赖顺序是什么意思

工程依赖顺序是指先实现被依赖的部分，再实现依赖它的部分。

常见顺序：

```text
数据结构 → 数据访问 → 服务逻辑 → 状态管理 → UI 组件 → 页面集成 → 测试 → 验收
```

对于登录、权限、支付、数据写入等场景，还要优先处理：

```text
认证 → 权限 → 数据契约 → 业务逻辑 → 用户界面
```

### 13. spec2super 可以改什么

spec2super 可以做这些转换：

- 改变文档结构。
- 提取 OpenSpec 事实。
- 保留来源路径。
- 标注需求和任务的对应关系。
- 把需求任务转换成工程依赖顺序。
- 标出 Planning Gaps。

### 14. spec2super 不能改什么

spec2super 不能做这些事情：

- 新增需求。
- 删除需求。
- 改变需求强度。
- 新增技术决策。
- 发明 API。
- 发明文件路径。
- 发明测试命令。
- 代替 Superpowers 写最终 plan。

如果 OpenSpec 没有足够信息，spec2super 应该写 `Planning Gaps`，而不是补猜。

### 15. Planning Gaps 是什么

`Planning Gaps` 是阻塞 Superpowers 写出准确工程计划的缺失信息。

例如：

- OpenSpec 没有说明 API 返回字段。
- OpenSpec 没有说明权限规则。
- OpenSpec 没有说明错误状态。
- OpenSpec 没有说明目标平台。
- OpenSpec 没有说明是否需要 migration。

它的作用是把不确定性显性化。

### 16. Superpowers 是什么

Superpowers 是工程执行层。

它负责：

- 生成工程计划。
- 拆成小步骤。
- 使用 TDD。
- 执行实现。
- 做代码审查。
- 做完成前验证。
- 收尾开发分支。

它关注的是“怎么把代码写稳”。

### 17. writing-plans 是什么

`superpowers:writing-plans` 是 Superpowers 里负责生成工程实现计划的 skill。

它会把 `translation.md` 转成：

```text
docs/superpowers/plans/YYYY-MM-DD-<change-name>.md
```

这个 plan 应该包含精确文件路径、具体代码步骤、测试命令、验证方式和提交步骤。

### 18. 为什么不直接让 Superpowers 读 tasks.md

因为 `tasks.md` 是需求视角，不一定是工程执行视角。

如果直接把 `tasks.md` 交给 Superpowers，它可能会重新理解需求，并自行生成一套计划。

`translation.md` 的作用是把输入先整理好，减少 Superpowers 重新解释需求的空间。

### 19. 为什么要做验证和归档

验证保证代码真的满足规格。归档保证这次变更成为项目长期上下文。

如果不验证，AI 可能只完成了部分需求。  
如果不归档，下次 AI 还要重新理解同样的背景。

### 20. 为什么要加入部署检查

产品落地不等于代码合并。

真正的交付包括：

- 环境正确。
- 数据正确。
- 权限正确。
- 监控正确。
- 错误可见。
- 可以回滚。
- 生产可用。

所以 AI-Coding 工程师不仅要完成代码，还要保证功能能安全上线。

### 21. 这套流程的好处

这套流程的好处：

- 减少需求漂移。
- 减少 AI 自作主张。
- 减少工程返工。
- 提高验收质量。
- 保留完整变更上下文。
- 让复杂功能可以分阶段落地。
- 让后续功能开发更快。

### 22. 最终原则

```text
OpenSpec 不写代码。
spec2super 不改需求。
Superpowers 不重新定义产品范围。
验证不看口头完成，只看证据。
归档不只是收尾，而是沉淀长期上下文。
```
