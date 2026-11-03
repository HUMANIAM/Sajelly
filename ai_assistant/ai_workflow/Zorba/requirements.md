# Zorba — Living Engineering Team
## System Requirements (Consolidated)

**Version:** 0.4<br>
**Status:** System analysis complete — proposed baseline for team review (not yet approved)<br>
**Scope:** The engineering team as a whole, not individual role specifications<br>
**Source:** Living Engineering Team Manifesto and the team's system-analysis discussions<br>
**Previous draft:** Version 0.3, superseded by this consolidation and not included in this package

## 1. The need

We want a team of human and agent engineers that can take real problems through engineering work, produce trustworthy outcomes, and keep its understanding and experience across projects and sessions.

We already know how to work as engineers. The system should make that collaboration practical for agent engineers too—without turning ordinary work into a complex agent framework. An engineer can initiate work, ask another engineer for help, challenge a decision, submit a PR, review a teammate's work, and improve their own practices.

**Success is not the number of agents or artifacts.** It is whether the team can responsibly own independently assigned work, build understandable software, verify real behavior, resume work, and improve through experience—on Sajelly or another project.

The **Living Engineering Team Manifesto** defines culture and values. This document describes the observable capabilities needed to realize them.

## 2. Boundaries and agreed terms

- **Engineer:** A human or agent teammate. The same standards of contribution, evidence, review, and respectful disagreement apply to both. Real capability and permission limits are made explicit.
- **Role:** A continuing area of engineering responsibility, with an owner. The initial roles are **Client / Intent Clarification, System Analyst, Architect, Designer, Implementer, Tester, and Deployment Engineer**. This is a map of responsibilities, **not a mandatory sequence**.
- **Activity / work item:** A human or agent engineer brings an idea, problem, feature, bug, experiment, test improvement, design change, release, or team improvement. The initiator and collaborators clarify what they want to achieve; the category guides the relevant roles but does not dictate a fixed route.
- **Epic:** A coherent, bounded responsibility or feature that a teammate can own end to end. It may be decomposed into small, reviewable tasks and PRs, and may require help from several roles.
- **Feature workspace:** `ai_assistant/features/<feature>/` holds exploration, discussion, proposals, activity clarification, and phase work. A phase artifact may be one Markdown file or several, or may be code/tests in the main codebase rather than a duplicate document. **This is not canonical project memory.**
- **Project memory:** `docs/` holds the accepted project understanding—requirements, architecture, design, RFCs, ADRs, retrospectives, and related decisions. Source code, configuration, and `data/` are project context and actual system artifacts.
- **Engineering memory:** The reusable, project-agnostic team's identities, roles, skills, tools, templates, manifesto, and playbooks under `ai_assistant/ai_workflow/Zorba/`. It should be portable to another project without carrying Sajelly-specific assumptions.
- **Engineering handoff:** A concise, readable exchange between roles using Markdown and links to relevant artifacts. It communicates intent, accepted facts, decisions, outstanding questions, and the outcome the next engineer is asked to produce. It is **bidirectional**: an engineer can request clarification from any relevant teammate.
- **GitHub:** Git stores accepted artifacts and their history. Pull requests (PRs) are the common way to propose, discuss, test, review, and accept changes. A draft PR is work in progress.
- **Temporary laboratory:** `ai_assistant/tmp/` is a disposable, Git-ignored place for probes and experiments. Important results are preserved elsewhere before the lab is discarded.

Locations are the **agreed starting structure**, not a mandate to build a special runtime or automation framework.

## 3. System requirements

IDs are retained from our discussions so they can be referenced in tests, PRs, and future changes. Short requirements are intentionally separate from instructions about *how* to implement them.

### A. Identity, initiative, and responsibility

| ID | Requirement |
|---|---|
| TEAM-001 | The team shall allow an engineer to engage a needed role independently, without invoking every other role. |
| TEAM-002 | Agent engineers shall have a durable role identity, mission, responsibility, and working principles that can be restored across sessions and tools. |
| TEAM-003 | Human and agent engineers shall be able to question decisions, raise concerns, explain reasoning, and propose alternatives. |
| TEAM-008 | Engineers shall have access to the context and approved tools needed for their work, with limitations and permissions visible. |
| TEAM-010 | Every engineering responsibility shall have an identified owner. |
| TEAM-029 | Human and agent engineers shall be able to initiate work and propose improvements within their responsibilities without an extra agent-specific permission gate. |

### B. Work begins and ends according to the need

| ID | Requirement |
|---|---|
| TEAM-022 | An engineer initiating work shall describe the need or proposed change and its intended outcome, refining uncertainty with teammates when needed. |
| TEAM-023 | The team shall select the starting role and needed contributions according to the work, without requiring a full linear lifecycle. |
| TEAM-024 | Work shall be allowed to finish at the needed outcome, such as analysis, agreed design, verified fix, or deployed feature. |
| TEAM-025 | When work needs a decision or change owned by another role, the engineer shall request that role's contribution. |
| TEAM-026 | The team shall define completion evidence appropriate to the intended outcome and preserve observed results and limitations. |
| TEAM-027 | Work entering the repository shall be split into understandable, reviewable PRs when practical. |
| TEAM-028 | A meaningful change in agreed scope or intended outcome shall be visible and reviewed by the responsible owner before continuing. |
| TEAM-050 | The team shall let an initiator express an activity in ordinary language, clarify its category, relevant problem or need, and intended outcome without requiring a complete lifecycle plan. |
| TEAM-051 | When clarification matters to later work, the team shall preserve the resulting activity in the feature workspace as a short, revisable Markdown artifact; `activity.md` is a proposed initial filename, not a mandatory system-wide interface. |
| TEAM-053 | The team shall support assigning an epic to one accountable contributor who may take it end to end, request help from teammates, and split delivery into independently reviewable changes. |

### C. Collaboration, handoffs, and disagreement

| ID | Requirement |
|---|---|
| TEAM-007 | Engineers shall use shared, lightweight communication contracts for relevant work, decisions, evidence, and unresolved questions. |
| TEAM-011 | An engineer needing a change outside their responsibility shall send a clear request to the responsible engineer. |
| TEAM-012 | The responsible engineer shall examine the request, discuss it as needed, make the decision or change within their responsibility, and return the outcome with its reasoning. |
| TEAM-013 | Engineers shall not silently take over another role's owned work. |
| TEAM-015 | When a material disagreement remains unresolved after a short direct discussion, either engineer shall be able to propose an RFC; independent reviewers shall be assigned, and the decision and reasoning shall be retained. |
| TEAM-018 | Changes to role-owned artifacts shall involve their responsible engineer in review. |
| TEAM-052 | When one engineer asks another to continue or decide work, the handoff shall communicate the relevant objective, context, existing decisions, requested outcome, and outstanding questions in readable Markdown or linked tracked artifacts. Follow-up questions and challenges remain allowed. |
| TEAM-055 | Work passed from requirement analysis to architectural design shall describe needed behavior, relevant quality constraints, boundaries, and acceptance conditions, with assumptions and unresolved decisions visible; it shall not prescribe architecture without an explicit requirement for it. |

### D. Evidence, review, and releases

| ID | Requirement |
|---|---|
| TEAM-006 | Engineers shall support claims of completion or correctness with evidence of observed behavior, including failures, untested areas, and limitations. |
| TEAM-009 | The team shall distinguish experiment, prototype, and production-ready claims, with evidence appropriate to the stated level. |
| TEAM-017 | Human and agent engineers shall be able to propose code, documentation, data, design, decision, and team-practice changes through PRs. |
| TEAM-030 | Changes to shared, version-controlled project or team artifacts shall enter the accepted codebase through PRs. |
| TEAM-031 | Every PR shall receive review from an engineer other than its author before merging. |
| TEAM-032 | No engineer shall approve and merge their own PR without independent review. |
| TEAM-033 | PR reviews shall examine correctness, impact, evidence, and agreed requirements rather than the author's human or agent status. |
| TEAM-034 | The team shall use GitHub PR states and history to see work in progress and review progress. |
| TEAM-035 | Engineers shall keep unfinished changes as draft PRs; a PR marked ready shall have the relevant verification completed, required CI checks passing, and a useful description. |
| TEAM-036 | PRs shall state the goal, solution, affected areas, review focus, and testing strategy using the team's existing scalable PR template. |
| TEAM-037 | Before approval, the reviewer shall consider the relevant changes, tests, and documentation, and identify any gaps. |
| TEAM-043 | PRs shall make relevant feature artifacts and verification evidence available to reviewers. |

### E. Memory and continuity

| ID | Requirement |
|---|---|
| TEAM-004 | The team shall preserve the current project understanding, important decisions, risks, and unresolved questions across sessions. |
| TEAM-005 | The team shall distinguish reusable engineering knowledge from project-specific knowledge. |
| TEAM-014 | Important decisions shall preserve their reasoning and any material trade-offs or limitations. |
| TEAM-016 | The Git repository shall be the source of truth for accepted project and engineering-team artifacts. |
| TEAM-038 | Git and GitHub history shall preserve enough changes, decisions, discussions, and evidence to understand and resume ongoing work. |
| TEAM-039 | The team shall retain relevant feature exploration and phase artifacts under `ai_assistant/features/<feature>/`. |
| TEAM-040 | Each participating role shall produce or update the agreed artifact needed for its contribution; that artifact may be a document, source code, tests, or another deliverable. |
| TEAM-041 | Engineers shall consult relevant existing feature artifacts instead of starting from an empty understanding of ongoing work. |
| TEAM-042 | Feature artifacts shall evolve under version control alongside related implementation and documentation changes. |
| TEAM-046 | The project's accepted requirements, architecture, designs, RFCs, ADRs, and retrospectives shall be maintained under `docs/` as project memory. |
| TEAM-047 | Exploratory feature artifacts and canonical project memory shall have distinguishable purposes; accepted decisions shall be reflected in `docs/` without requiring both locations to be textually identical. |
| TEAM-048 | The team's reusable identities, roles, skills, tools, templates, manifesto, and playbooks shall remain separate from project-specific knowledge so they can be reused in another project. |
| TEAM-049 | Engineers shall have a disposable, Git-ignored laboratory for experiments; evidence needed for later decisions shall be retained in tracked project or engineering artifacts. |
| TEAM-054 | Relevant activities, epics, issues, artifacts, decisions, PRs, implementation, and test evidence shall be linked sufficiently to follow an engineering change without chat history, including authorship or provenance where useful. This does not require metadata on every source file. |

### F. Learning and self-improvement

| ID | Requirement |
|---|---|
| TEAM-019 | Human and agent engineers shall be able to participate in retrospectives and review real work outcomes together. |
| TEAM-020 | A preserved lesson shall include enough context and evidence to understand when it applies; a local lesson shall not automatically become a universal rule. |
| TEAM-021 | Engineers shall be able to propose changes to their role guidance, skills, tools, templates, and practices through reviewed PRs. |
| TEAM-044 | After initial bootstrap, engineers responsible for roles shall be able to maintain and improve the reusable guidance and capabilities of those roles through peer-reviewed changes. |
| TEAM-045 | Engineers shall be able to initiate such improvements from daily work, experiments, retrospectives, or independent reflection, not only from formally assigned tasks. |

**Important:** These requirements describe capabilities and guardrails. They do **not** require one file, one meeting, or one approval per requirement.

## 4. Communication interfaces — what must survive a handoff

These are **information contracts**, not agent prompts, mandatory forms, or prescribed filenames. Markdown is the first shared language. The owning engineer decides what format best conveys its result; the role contracts provide optional starting templates where a template helps.

| Boundary | Information needed by the next engineer | Not required |
|---|---|---|
| Initiator → Intent Clarification / next role | Problem or observation, intended result or question, relevant evidence or context, known uncertainties | A full requirements document |
| Clarified activity → System Analyst (when analysis is needed) | Agreed intent, affected users/system, expected outcome, scope, open decisions, references | A proposed architecture |
| System Analyst → Architect (when design is needed) | Agreed functional behavior, relevant quality and safety constraints, system boundaries or external interactions, acceptance scenarios, assumptions and unresolved questions | Classes, modules, frameworks or implementation details |
| Any engineer → another owner | What needs the owner's decision/change, why, supporting evidence and context, urgency or dependencies | A new workflow engine or meeting |
| Engineer → PR reviewer | Goal, change, relevant artifacts, testing results, known gaps and review focus | Separate Markdown duplicates of code/tests already in the PR |

**Example.** A teammate can take the Sajelly *customers-ledger-and-safety* epic. They should be able to read the accepted product requirements and relevant feature workspace, agree the epic boundary and DoD, then deliver a series of focused PRs. They can request Analyst, Architect, Designer, or Tester contributions when their work crosses ownership boundaries. The epic owner remains accountable for bringing the epic to its agreed outcome, not for personally performing every role.

## 5. Acceptance scenarios (system-wide)

### S1 — A feature stops at analysis

**Given** an engineer has an idea and only wants to understand the need,<br>
**When** they engage the Client / Intent Clarification and/or System Analyst roles,<br>
**Then** the work can produce a clear, reviewed analysis and stop without invoking design, implementation, testing, or deployment.
**Relevant:** TEAM-001, TEAM-022–024, TEAM-026.

### S2 — A bug fix remains small

**Given** a bug is reproducible and no design contract needs changing,<br>
**When** an Implementer fixes it, adds an appropriate regression test, and opens a PR,<br>
**Then** another engineer can inspect the reproduction, fix, test evidence, and known limits without forcing unrelated lifecycle phases.
**Relevant:** TEAM-006, TEAM-023–027, TEAM-031–037.

### S3 — Work crosses ownership boundaries

**Given** an Implementer discovers that an agreed design contract must change,<br>
**When** they ask the responsible Designer or Architect for a change,<br>
**Then** that engineer reviews the request, updates or maintains the contract with reasons, and returns the decision before the affected work proceeds.
**Relevant:** TEAM-010–013, TEAM-018, TEAM-025.

### S4 — Engineers disagree

**Given** two engineers—human or agent—disagree on a material decision,<br>
**When** a direct exchange does not resolve it,<br>
**Then** either may propose an RFC, independent reviewers are assigned, both positions remain available, and the result and reasoning are recorded.
**Relevant:** TEAM-003, TEAM-015.

### S5 — Review is independent of author identity

**Given** an agent or human engineer completes a change,<br>
**When** they mark its PR ready for review,<br>
**Then** the description and test evidence are available, relevant CI checks pass, and another engineer reviews it before merge.
**Relevant:** TEAM-029–037, TEAM-043.

### S6 — Work resumes after months

**Given** the team returns to a feature months later,<br>
**When** an engineer reads its working artifacts, accepted project docs, and Git history,<br>
**Then** they can identify what was decided, what is current, what remains uncertain, and what to do next without relying on a previous chat session.
**Relevant:** TEAM-004, TEAM-014, TEAM-038–042, TEAM-046–047.

### S7 — The team improves itself

**Given** an agent or human engineer identifies a better practice through experience or reflection,<br>
**When** they propose a PR changing their role, skill, template, or tool,<br>
**Then** another engineer can review the reason and evidence, and the accepted improvement remains available for future projects without importing unrelated product assumptions.
**Relevant:** TEAM-005, TEAM-019–021, TEAM-044–045, TEAM-048.

### S8 — A work intent becomes a clear starting point

**Given** a teammate reports a bug but cannot yet explain its cause,<br>
**When** they request Intent Clarification,<br>
**Then** the team can record a small activity describing the observed symptom, desired outcome, known context, category and unresolved questions; the work can then enter the appropriate engineering role without pretending that a diagnosis already exists.
**Relevant:** TEAM-022–024, TEAM-050–052.

### S9 — A teammate owns an epic end to end

**Given** another engineer volunteers for Sajelly's *conversation-and-agent* epic,<br>
**When** they inspect its accepted docs, dependencies and feature workspace,<br>
**Then** they can define a clear DoD, plan reviewable PRs, seek specialist contributions, and deliver the epic's agreed outcome with traceable evidence and independent review.
**Relevant:** TEAM-010–013, TEAM-027, TEAM-040, TEAM-053–054.

### S10 — The Architect receives a usable requirements contract

**Given** an initiative has reached agreement about expected behavior and constraints,<br>
**When** the System Analyst hands it to the Architect,<br>
**Then** the Architect can identify the required behaviors, acceptance outcomes, quality constraints, and open questions without treating an unexamined implementation suggestion as a binding requirement; the Architect may ask the Analyst or initiator for clarification.
**Relevant:** TEAM-003, TEAM-007, TEAM-025, TEAM-052, TEAM-055.

## 6. Explicit non-goals for this version

- No mandatory end-to-end sequence for every work item.
- No orchestration engine, multi-agent hierarchy, or automatic specialist invocation.
- No separate work-tracking service or memory database replacing Git/GitHub.
- No mandatory full set of phase files for every feature. Code and tests can be sufficient phase artifacts.
- No forced conversion of every idea into an epic or every chat into a permanent document.
- No requirement to define executable agent skills, prompts, or automated handoff machinery in this baseline.
- No duplication of individual role contracts inside these system-level requirements.
- No requirement for agents to have personal emails, GitHub accounts, names, or other decorative identities at bootstrap.

## 7. Open questions — only those that can change system behavior

1. **Unavailable owner:** What should happen when the responsible engineer is unavailable and a change cannot reasonably wait?
2. **RFC outcome:** Who records and has authority to settle an RFC after assigned peer reviewers consider it? How does that fit the responsible role's ownership?
3. **Protected operations:** Which actions, if any, need additional safeguards beyond normal peer review (for example, deployment credentials, destructive actions, or access to private data)?
4. **Repository adoption:** Which accepted Sajelly project docs should link to this proposed baseline if it is adopted?

These questions remain visible for team governance and architectural risk assessment. They do **not** require answers before the role contracts can be exercised in a small manual pilot; any behavior that depends on one must be explicit in the relevant change.

## 8. Requirements vs. role design

System requirements end here. Role-specific responsibilities and input/output contracts live in [`roles/`](roles/). They are engineering-memory artifacts governed by this baseline, but they can evolve independently through peer-reviewed changes.

The initial role set is Intent Clarification, System Analysis, Architecture, Design, Implementation, Testing, and Deployment. The [`README`](README.md#meet-the-engineers) introduces the team and links to each role contract.

**`intent_clarification/`** is the preferred folder name for the Client role. This is a naming convention, not an additional role.

## 9. Definition of Done for system analysis

This draft can be approved when:

- The team agrees that it describes **system-wide capabilities**, not a particular agent architecture.
- A new feature, a small bug fix, an ownership handoff, an independently owned epic, an RFC, and an engineer-led self-improvement can each be traced to observable requirements.
- Project memory, feature workspace, and engineering memory are distinguishable.
- Any remaining questions are explicit rather than silently answered through implementation.

The candidate baseline is **ready for human team review**. Approval would establish the system-level baseline against which the role contracts and future architecture are reviewed; it would **not** assert that the workflow is already implemented or proven.

---

### Changes since v0.3

- Integrated the handwritten notes: engineer-initiated activities, category-based starts, and an optional tracked `activity.md` before analysis.
- Aligned RFC peer review with the same human/agent review principle as other PRs.
- Defined **logical Markdown handoffs** between initiator, intent clarification, System Analyst, Architect and PR reviewer, without specifying agent prompts or an orchestration engine.
- Made **end-to-end epic ownership**, reviewable work slices, and traceability explicit (`TEAM-050`–`TEAM-055`).
- Added observable examples for intent intake, independently owned Sajelly epics, and the architecture handoff.
- Kept the original `TEAM-001`–`TEAM-049` IDs and Architect role requirements separate.
