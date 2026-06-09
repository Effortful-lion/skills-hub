---
name: spec2super
description: Use when an OpenSpec change has proposal.md, design.md, specs/, and tasks.md and the user wants to generate a Superpowers-ready translation document without changing the OpenSpec meaning. This skill translates OpenSpec artifacts into translation.md as input for superpowers:writing-plans; it must not implement code, redesign requirements, or replace OpenSpec/Superpowers skills.
metadata:
  short-description: Translate OpenSpec artifacts into Superpowers planning input
---

# OpenSpec → Superpowers Translation

## Purpose

Generate a mechanical translation file from an OpenSpec change so Superpowers can create an implementation plan from stable inputs.

This skill is a translator only:

- OpenSpec owns requirement/spec/design/task generation.
- This skill owns format conversion into `translation.md`.
- Superpowers owns implementation planning, TDD execution, review, and verification.

## Inputs

Read one OpenSpec change directory:

```text
openspec/changes/<change-name>/
├── proposal.md
├── design.md
├── tasks.md
└── specs/**/*.md
```

If `<change-name>` is not provided:

1. List non-archive directories under `openspec/changes/`.
2. If exactly one exists, use it.
3. If multiple exist, ask the user to choose.
4. If none exist, tell the user to create an OpenSpec change first.

## Output

Write:

```text
openspec/changes/<change-name>/translation.md
```

The output is the input document for `superpowers:writing-plans`.

Do not write code. Do not modify OpenSpec artifacts. Do not generate `docs/superpowers/plans/...`; Superpowers does that next.

## Non-Negotiable Translation Contract

The translation must preserve OpenSpec meaning.

Allowed:

- Normalize sections into a Superpowers-readable order.
- Copy or concise-paraphrase OpenSpec content while preserving meaning.
- Extract source references and traceability links.
- Convert OpenSpec `tasks.md` from requirement/module order into engineering dependency order when the dependency is supported by OpenSpec artifacts.
- Group requirements, design facts, and task checklist items.
- Mark missing details as `Not specified in OpenSpec`.
- Add planning instructions that constrain Superpowers to the OpenSpec artifacts.

Forbidden:

- Add requirements, scope, files, APIs, tests, commands, or design decisions not present in OpenSpec.
- Change acceptance criteria or requirement strength (`MUST`, `SHALL`, `SHOULD`, `MAY`).
- Convert open questions into decisions.
- Resolve ambiguity by guessing.
- Reorder or split tasks in a way that changes meaning or implies new work.
- Invent dependencies that are not supported by proposal/design/specs/tasks.
- Treat this translation as the final implementation plan.

If OpenSpec is insufficient for Superpowers planning, write the gap explicitly under `## Planning Gaps` instead of filling it in.

## Generation Procedure

1. **Locate change**
   - Resolve `openspec/changes/<change-name>`.
   - Confirm required files exist: `proposal.md`, `design.md`, `tasks.md`, and at least one `specs/**/*.md`.

2. **Read artifacts exactly once first**
   - Read proposal, design, tasks, and all delta specs.
   - Note file paths used as source references.
   - Do not edit these files.

3. **Extract source facts**
   - Proposal: intent, scope, out-of-scope, approach.
   - Specs: ADDED/MODIFIED/REMOVED requirements and scenarios.
   - Design: technical approach, architecture decisions, data flow, file changes explicitly mentioned.
   - Tasks: checkbox items and grouping exactly as authored.

4. **Create traceability**
   - For each task, list related requirement names when obvious from names/content.
   - If relation is not obvious, write `Not safely inferable from OpenSpec`.
   - Never invent a trace.

5. **Create engineering task order**
   - Preserve the original `tasks.md` checklist under `## Original OpenSpec Task Input`.
   - Add `## Engineering-Oriented Task Order` that reorders the same task intent by implementation dependency.
   - Use only dependencies supported by OpenSpec artifacts, such as explicit file changes, data flow, architecture decisions, prerequisite scenarios, or task wording.
   - If dependency ordering is not safely inferable, preserve the original order and state why.
   - Do not add implementation details that belong to `superpowers:writing-plans`.

6. **Write `translation.md`**
   - Use the template below.
   - Keep wording direct and engineering-facing.
   - Preserve uncertainty as uncertainty.

6. **Self-check before finishing**
   - Confirm every requirement in `specs/` appears in the translation.
   - Confirm every task checkbox in `tasks.md` appears in the translation.
   - Confirm no new scope/design/file/API/test command was invented.
   - Confirm next step says to use `superpowers:writing-plans`, not to implement directly.

## Translation Template

```markdown
# Superpowers Translation: <change-name>

> REQUIRED NEXT SKILL: Use `superpowers:writing-plans` to create the implementation plan from this translation. This file is not the implementation plan.

## Translation Contract

This file is the translation from OpenSpec artifacts to Superpowers planning input.

- Do not reinterpret requirements.
- Do not change scope.
- Do not add design decisions.
- Do not implement directly from this file.
- If planning requires missing information, stop and ask instead of guessing.

## Source Artifacts

- Proposal: `openspec/changes/<change-name>/proposal.md`
- Design: `openspec/changes/<change-name>/design.md`
- Tasks: `openspec/changes/<change-name>/tasks.md`
- Specs:
  - `openspec/changes/<change-name>/specs/<domain>/spec.md`

## Proposal Input

### Intent
<Preserved from proposal.md, or `Not specified in OpenSpec`.>

### In Scope
<Preserved from proposal.md.>

### Out of Scope
<Preserved from proposal.md.>

### High-Level Approach
<Preserved from proposal.md.>

## Specification Input

Repeat for each delta spec file.

### Spec File: `openspec/changes/<change-name>/specs/<domain>/spec.md`

#### ADDED Requirements
- Requirement: <name>
  - Statement: <requirement statement preserving MUST/SHALL/SHOULD/MAY>
  - Scenarios:
    - <scenario name>: GIVEN ... WHEN ... THEN ...

#### MODIFIED Requirements
- Requirement: <name>
  - New statement: <preserved statement>
  - Previous behavior: <if stated>
  - Scenarios:
    - <scenario name>: GIVEN ... WHEN ... THEN ...

#### REMOVED Requirements
- Requirement: <name>
  - Removal reason: <if stated>

## Design Input

### Technical Approach
<Preserved from design.md.>

### Architecture Decisions
- Decision: <name>
  - Rationale: <preserved rationale>

### Data Flow / State Flow
<Preserved from design.md, or `Not specified in OpenSpec`.>

### File Changes Mentioned By OpenSpec
- Create: `<path>` — <purpose if specified>
- Modify: `<path>` — <purpose if specified>
- Not specified in OpenSpec

## Original OpenSpec Task Input

Preserve the OpenSpec task grouping and checkbox state before any engineering reordering.

### <OpenSpec task group heading>
- [ ] <task id/title exactly or faithfully preserved>
  - Source: `tasks.md`
  - Requirement refs: <requirement names if safely inferable, otherwise `Not safely inferable from OpenSpec`>
  - Design refs: <design section/decision if safely inferable, otherwise `Not safely inferable from OpenSpec`>

## Engineering-Oriented Task Order

Reorder the same OpenSpec task intent by implementation dependency. This is a dependency-oriented view for Superpowers planning, not a new task list.

Ordering rules:

1. Foundation before consumers: schemas/types/config/data model before APIs/services/state/UI.
2. Backend/API/data access before frontend integration when the UI depends on them.
3. Shared infrastructure before feature modules.
4. Auth/permission/session prerequisites before protected business flows.
5. State management/data flow before components that consume that state.
6. Tests/verification stay attached to the behavior they validate unless OpenSpec states otherwise.
7. If ordering is ambiguous, keep the original OpenSpec order and mark `Dependency not safely inferable from OpenSpec`.

### Engineering Step Group: <dependency-oriented group name>
- OpenSpec task refs: <task ids/titles from tasks.md>
- Why this comes here: <dependency reason from OpenSpec, or `Dependency not safely inferable from OpenSpec`>
- Requirement refs: <requirement names if safely inferable>
- Design refs: <design section/decision if safely inferable>
- Scope preservation note: No new work added; this only reorders OpenSpec task intent.

## Planning Gaps

List only gaps that block Superpowers from writing an exact implementation plan.

- <gap> — Source: Not specified in OpenSpec

If no blocking gaps: `None identified.`

## Instructions For Superpowers Planning

When using `superpowers:writing-plans`:

1. Treat this translation as the approved spec/requirements input.
2. Inspect the codebase to produce exact file paths and code-level steps.
3. Preserve all OpenSpec scope, requirements, design decisions, and task intent.
4. Do not add product scope beyond OpenSpec.
5. If the translation has `Planning Gaps`, ask the user before planning or state assumptions explicitly for approval.
6. Save the implementation plan to `docs/superpowers/plans/YYYY-MM-DD-<change-name>.md`.
7. The generated plan must follow Superpowers requirements: bite-sized checkbox steps, exact files, concrete code/commands, TDD where applicable, and verification steps.

## Translation Self-Check

- [ ] All `specs/**/*.md` requirements are represented.
- [ ] All `tasks.md` checkbox items are represented in the original task input section.
- [ ] Engineering-oriented order uses only existing OpenSpec task intent.
- [ ] Any dependency reordering is justified by OpenSpec artifacts or marked as not safely inferable.
- [ ] Proposal scope and out-of-scope are represented.
- [ ] Design decisions are represented without alteration.
- [ ] No invented requirements, files, APIs, tests, commands, or scope.
- [ ] Next step is `superpowers:writing-plans`, not implementation.
```

## Final Response

After writing the translation, respond with:

- Path to `translation.md`.
- Count of proposal/design/task/spec files read.
- Any `Planning Gaps` found.
- The exact next instruction to give Superpowers.
