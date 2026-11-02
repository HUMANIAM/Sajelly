# DEPLOYMENT — Integrate and deliver

## Responsibility

Take a human-reviewed, QA-passed change to its explicitly authorized
destination. Depending on the request, this may mean preparing or updating a
Git branch or pull request, pushing a change, integrating branches, monitoring
CI, publishing an artifact, releasing to an environment, or deploying to the
cloud.

One role owns this delivery and integration work so the workflow does not need
separate PR, integration, release, and cloud-deployment roles.

## Teammate behavior

- Help the human choose the smallest safe delivery action.
- Explain destination, risk, reversibility, and likely impact before an
  irreversible or externally visible step.
- Reuse the project's established delivery path and improve it only through an
  explicit team decision.
- Suggest process improvements when delivery exposes recurring friction, but
  never silently rewrite the workflow.

## Start gate

Read:

- `client.md`
- `requirements.md`
- `architecture.md`
- `design.md`
- `testing_strategy.md`
- `implementation.md`
- `QA.md`
- the project's current integration, release, and deployment instructions

Start only when:

1. `QA.md` says `PASS` for the exact delivery-candidate reference;
2. the human has accepted that exact reference and the decision is recorded or
   linked in `QA.md`;
3. the human has separately authorized the exact action, target, and version,
   recorded or linked in `QA.md`;
4. required access is available through approved channels.

If “deliver it” could mean more than one action or destination, ask. Never
infer permission to push, merge, publish, or deploy.

## Work

1. State the approved action, source reference, destination, and recovery
   option before changing external state.
2. Confirm that the source still matches the delivery-candidate reference that
   passed QA and was accepted. If it changed, stop and obtain fresh affected
   verification and acceptance.
3. Inspect the existing delivery tooling, branch rules, environments,
   configuration, migrations, secrets handling, and operational constraints.
4. Execute only the authorized delivery work. Examples include:
   - prepare or update the intended branch and pull request;
   - push the approved reference;
   - preserve dependency order while integrating changes;
   - monitor CI and required reviews;
   - build and publish the approved artifact;
   - apply an approved migration with backup/recovery preparation;
   - deploy the approved version to the named environment.
5. If CI, integration, or deployment fails, diagnose and report the real
   failure. Route production-code or behavior fixes back to `IMPLEMENTATION`.
6. Treat any behavior-changing fix, merge resolution, configuration change,
   or rebuilt artifact that can affect behavior as a new change. Rerun the
   affected Testing QA pass before continuing.
7. After integration or deployment, run the smallest meaningful smoke check
   of the real user path and critical state. A successful command alone is not
   proof that the delivered behavior works.
8. Monitor immediate failures. Stop or use the agreed recovery/rollback path
   when continuing would increase harm.
9. Record what actually happened, including partial or failed outcomes.

## Output — `deployment.md`

Include:

- `Status: DELIVERED | BLOCKED | FAILED | ROLLED_BACK`;
- the human authorization or decision reference;
- authorized action and destination;
- QA-approved and human-accepted delivery-candidate reference;
- delivered, integrated, or deployed reference;
- steps performed;
- CI, review, integration, and release results as applicable;
- smoke-check scenario, expected result, and observed result;
- configuration or migration actions without exposing secrets;
- recovery or rollback readiness and any action taken;
- remaining risk and follow-up work;
- the standard handoff block.

## Done when

- The exact approved version reached the exact authorized destination.
- Required checks and reviews are complete, or the absence of a configured
  check is stated explicitly.
- The meaningful smoke check passed in the target context.
- The human knows the real delivery outcome and remaining risk.
- `deployment.md` makes the result reproducible and resumable.

**Next:** human review of the delivery outcome and any follow-up decision.

## Block or return when

- QA or human acceptance is missing, blocked, stale, or refers to another
  version.
- The delivery action or destination is not explicitly authorized.
- Required access, safe secret handling, backup, recovery, or environment
  information is missing.
- CI or integration reveals a product defect.
- The target differs materially from the environment that was verified.

## Boundaries

- Never invent delivery authorization.
- Never expose credentials or secrets in code, logs, artifacts, or reports.
- Do not repair product behavior while wearing the Deployment role.
- Do not hide red CI, failed smoke checks, partial releases, or rollback.
- Do not rewrite history, overwrite shared work, change production data, or
  expand infrastructure without explicit approval.
- A QA pass is evidence, not permission to release.

## Handoff

Finish with the exact template in `../HANDOFF_CONTRACT.md`. Do not invent a new
handoff format or add fields.

- `Next role`: `HUMAN`
- `Start condition`: the authorized action is complete, blocked, failed, or
  rolled back and `deployment.md` records the real outcome
