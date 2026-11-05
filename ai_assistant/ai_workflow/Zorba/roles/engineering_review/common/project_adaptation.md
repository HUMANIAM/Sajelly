# Project Adaptation — Inspect Before Enforcing

The two reviewers are portable. Use the
[common workflow](review_protocol.md#common-review-workflow) to adapt only the
checks relevant to the baseline-to-proposed change.

1. Read applicable project instructions and the change goal. Locate affected
   `component_name.meta` files for purpose and dependency navigation.
2. Read the scoped diff and surrounding code. Consult requirements, architecture
   policy or a nearby example only to answer an actual question raised by the change.
3. Follow relevant public interfaces and dependencies to evaluate the affected
   behavior. Do not read a whole stable vertical slice or all project docs by default.
4. Reconcile relevant metadata/docs with code and automated evidence. Record
   consequential drift; missing navigation metadata alone is not a blocking defect.
5. Apply engineering memory as portable lessons and project memory only where
   confirmed for the target project. Do not impose a framework or layout.
6. Use existing mechanical check results for the reviewed revision. Run only
   permitted diagnostics needed for unresolved risks; report material evidence gaps.

## Examples, not universal laws

WebAcademy demonstrated these *conditional* patterns:

- Backend request flow: `route -> service -> repository -> model/database`; lower layers do not import higher layers. Schemas define boundary data, not a required intermediate runtime step. Services own the final transaction boundary when repository helpers compose a workflow. `core` owns process-wide infrastructure; feature-shared packages own named shared responsibilities.
- Frontend flow (React example): `page/container -> hook -> service -> repository -> API`; presentation receives typed props; hooks own lifecycle; services own decisions; repository maps only when there is a real semantic difference; API owns transport.
- Both: feature-oriented grouping, explicit cross-feature public interfaces, mechanically checked import boundaries, no premature ports/adapters or file splitting, consistent naming selected **by the project**.

Do not impose those exact file names or layers on a different framework. A local design can satisfy the same separation principles using different names or boundaries.

## Authority order

Use approved requirements/product decisions and applicable project policies to judge intent; inspect source code, tests, and actual execution evidence to establish implemented behavior. A stale description is not proof of the runtime truth. If governing sources conflict, surface a `question` or `required` finding according to impact rather than inventing a policy.

## Scope and cross-stack interaction

Frontend may read backend API definitions and call-site behavior to assess compatibility. Backend may read frontend clients/consumer contracts to assess compatibility. Both must identify cross-stack gaps, assign the correct owner, and refrain from changing the other stack.
