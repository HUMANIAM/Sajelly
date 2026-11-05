# External Dependency Policy

## Default Rule

Install only what the project needs for a current, approved requirement.

- Prefer the Python standard library, browser platform, Node.js built-ins, and
  dependencies already present in the project.
- Do not add an external dependency when the standard platform provides a
  clear, safe, and maintainable solution.
- Do not add a second package that substantially duplicates an existing
  dependency.
- Do not install a package for a small helper that can be implemented clearly
  and safely with a few project-owned lines.
- Do not add a dependency for speculative future use.

## When an External Dependency Is Justified

A new dependency may be proposed when the standard platform or existing
dependencies are materially insufficient because of correctness, security,
interoperability, performance, or maintenance cost.

Choose a package that is:

- well known and meaningfully used by the development community
- actively maintained with recent, stable releases
- documented and compatible with the project's supported runtimes
- appropriately licensed for the project
- reasonably small in direct and transitive dependency cost
- supported by a credible security and issue-response history

Do not implement security-sensitive standards such as cryptography,
authentication protocols, or complex parsers merely to avoid a dependency.
The standard-library preference applies only when it provides an adequate and
safe solution.

## Required Proposal

Every new package or tool must be visible in the change and include a concise
rationale:

```markdown
Dependency:
Current requirement:
Why the standard platform is insufficient:
Existing dependencies considered:
Alternatives considered:
Runtime, development, or test-only:
Maintenance, license, security, and transitive-dependency notes:
Version and lockfile impact:
```

The engineering reviewer must be able to connect the dependency directly to
the implemented requirement.

## Installation and Lifecycle

- Use the project's existing package manager and dependency group.
- Keep runtime dependencies separate from development and test tooling.
- Commit the corresponding lockfile or resolved dependency artifact when the
  project uses one.
- Pin or constrain versions according to the project's update strategy.
- Review unexpected transitive dependencies and install scripts.
- Import the package only from the layer that owns the responsibility.
- Remove unused dependencies when the code that requires them is removed.
- Treat major upgrades and package replacements as reviewed dependency changes.

## Reviewer Decision

The reviewer should reject a dependency when:

- the standard platform or an existing dependency adequately solves the need
- the requirement is speculative or convenience-only
- the package duplicates an installed capability
- maintenance, security, license, compatibility, or transitive cost is unclear
- the change does not include the required rationale and lockfile impact

Approval means the dependency is necessary, appropriately scoped, and a better
long-term choice than owning the equivalent implementation in the project.
