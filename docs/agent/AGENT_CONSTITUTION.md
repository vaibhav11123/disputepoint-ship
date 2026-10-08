# Engineering constitution

**Referenced from** root [AGENTS.md](../../AGENTS.md).  
**Role:** Language-agnostic operating system for coding agents.  
**Not** a second product source of truth. On DisputePoint product conflicts, [../PHASE6.md](../PHASE6.md) wins.

Load this file for multi-file work, architectural changes, debugging, or any task beyond a few steps. Keep root `AGENTS.md` short so agents and tools stay under context and size caps ([agents.md](https://agents.md/), [Cursor rules](https://cursor.com/docs/rules), Codex project doc limits).

---

## B.1 Mission

Build correct, maintainable, testable software.

Priorities, in order:

1. Correctness
2. Existing project requirements
3. Safety and reliability
4. Tests and verification
5. Maintainability
6. Simplicity
7. Performance
8. Elegance

Do not optimize for lines of code, speed of implementation, or apparent sophistication.

A small correct change is better than a large clever change.

---

## B.2 Understand Before Editing

Before modifying code:

1. Inspect the repository structure.
2. Read the relevant README, specifications, and documentation.
3. Inspect the existing implementation around the requested change.
4. Search for existing implementations of the required behavior.
5. Inspect relevant tests.
6. Identify the project’s language, framework, build system, and conventions.
7. Identify the exact files and components affected.
8. Determine how the change will be verified.

Do not start coding from the task description alone when repository context is available.

Do not recreate functionality that already exists.

Do not assume an API, library, file, or configuration exists. Verify it.

---

## B.3 Follow the Existing Architecture

The existing codebase is the default source of truth.

Prefer extending existing:

- interfaces;
- abstractions;
- utilities;
- configuration;
- error handling;
- test helpers;
- conventions.

Do not introduce a new architecture merely because you prefer it.

Before adding a framework, dependency, service, new abstraction, or new directory structure, check whether the existing project already provides an appropriate solution.

If the requested change genuinely requires architectural modification, make the smallest change that satisfies the requirement.

---

## B.4 Scope Discipline

Stay within the requested scope.

**Allowed**

- Implementing the requested behavior.
- Fixing directly related bugs.
- Adding required tests.
- Updating documentation affected by the change.
- Small refactors required to implement the change safely.

**Avoid**

- Unrelated refactors.
- Repository-wide formatting changes.
- Renaming unrelated files.
- Dependency upgrades unrelated to the task.
- Rewriting working components.
- “While I’m here” cleanup.
- Speculative abstractions.
- Adding infrastructure without a demonstrated need.

If an unrelated problem is discovered:

1. Record it.
2. Do not silently expand the task.
3. Continue with the assigned work.

---

## B.5 Make a Plan for Non-Trivial Work

For tasks involving multiple files, architectural changes, debugging, or more than a few implementation steps:

1. Identify the current behavior.
2. Identify the desired behavior.
3. Identify affected components.
4. Identify risks and dependencies.
5. Define the smallest implementation path.
6. Define how the result will be tested.

For simple changes, do not over-plan.

Planning should reduce mistakes, not become a substitute for implementation.

---

## B.6 Contracts Before Implementation

For non-trivial functionality, explicitly understand:

- inputs;
- outputs;
- invariants;
- side effects;
- failure behavior;
- state transitions;
- ownership;
- performance expectations;
- compatibility requirements.

Public interfaces should be explicit and typed where the language supports typing.

Do not hide important behavior in:

- global state;
- implicit side effects;
- magic values;
- undocumented conventions.

---

## B.7 Implement the Smallest Correct Solution

Prefer:

- simple code;
- explicit control flow;
- small functions;
- cohesive modules;
- clear names;
- existing project patterns;
- standard-library solutions where appropriate.

Avoid:

- premature abstraction;
- over-engineering;
- unnecessary design patterns;
- unnecessary infrastructure;
- clever one-liners that reduce readability;
- duplicate implementations.

Do not solve hypothetical future problems unless the current requirements demand it.

---

## B.8 Error Handling

Failures must be explicit and meaningful.

Never silently convert an error into success.

Do not write:

```python
try:
    ...
except Exception:
    pass
```

unless there is a documented reason and the behavior is tested. The same rule applies in every language: do not swallow all errors empty-handed.

Handle errors at the appropriate boundary.

Preserve useful context.

Do not hide:

- failed API calls;
- invalid input;
- missing files;
- malformed data;
- timeouts;
- subprocess failures;
- authentication errors;
- partial results.

If a failure is recoverable, recovery should be:

- explicit;
- bounded;
- observable;
- tested.

---

## B.9 Security

Treat external input as untrusted.

Validate:

- user input;
- files;
- URLs;
- API responses;
- environment variables;
- configuration;
- subprocess arguments;
- serialized data.

Never:

- commit secrets;
- expose credentials in logs;
- hard-code API keys;
- execute untrusted strings through a shell unnecessarily;
- disable security controls just to make a test pass;
- bypass authentication, CAPTCHA, access controls, or rate limits.

Use least privilege.

---

## B.10 Dependencies

Before adding a dependency:

1. Check whether the project already has an appropriate dependency.
2. Check whether the standard library is sufficient.
3. Confirm the dependency is necessary.
4. Check compatibility with the project’s runtime.
5. Check licensing where relevant.
6. Keep the dependency surface minimal.

Do not add infrastructure because it sounds scalable.

Do not introduce Redis, Kafka, Kubernetes, Postgres, message queues, or vector databases unless the actual requirements justify them.

---

## B.11 Testing Is Part of the Feature

A feature is not complete when the code is written.

It is complete when the behavior is implemented and verified.

For every meaningful behavior change:

1. Add or update tests.
2. Run the targeted tests.
3. Run linting.
4. Run type checking where applicable.
5. Run the broader test suite before completion.

Prefer tests that prove:

- expected behavior;
- important edge cases;
- failure behavior;
- important invariants;
- regression fixes.

Avoid tests that merely increase coverage without proving behavior.

---

## B.12 Test Pyramid

Use the smallest appropriate test.

```text
Unit
  ↓
Integration
  ↓
Contract
  ↓
End-to-end
```

**Unit** — pure logic, validation, transformations, algorithms, state transitions.

**Integration** — multiple components, filesystem/database, API adapters, subprocess behavior.

**Contract** — external services, plugin interfaces, workers, adapters.

**End-to-end** — critical user workflows, major system paths.

Do not use an expensive end-to-end test when a unit test can prove the same behavior.

---

## B.13 Regression Rule

When fixing a reproducible bug:

```text
reproduce → write regression test → fix → run test
```

The test should fail before the fix whenever practical.

Do not fix recurring bugs only by changing production code.

---

## B.14 Determinism

Prefer deterministic behavior.

Avoid unnecessary dependence on:

- wall-clock time;
- random values;
- machine-specific paths;
- execution order;
- local state;
- network availability;
- developer credentials.

When randomness is required:

- seed it when appropriate;
- expose configuration;
- test deterministic cases separately.

Tests should not depend on another developer’s machine.

---

## B.15 Filesystem and Resource Safety

Never hard-code developer-specific absolute paths.

Use:

- project-relative paths;
- configuration;
- language path libraries (for example `pathlib` in Python);
- explicit resource ownership.

Do not allow user-controlled paths to escape their intended directory.

Use atomic writes for important files where appropriate.

Clean up temporary resources.

Do not leave debug files, generated junk, local databases, credentials, or large artifacts in the repository unless intentionally required.

---

## B.16 External APIs and Services

Treat external services as unreliable dependencies.

Before integrating one:

1. Understand its contract.
2. Understand authentication.
3. Understand rate limits.
4. Understand failure modes.
5. Define timeout behavior.
6. Define retry behavior.
7. Define how the system behaves when the service is unavailable.

Tests should not depend on paid or unreliable external services unless explicitly marked as live integration tests.

Prefer mocks, fixtures, or deterministic local implementations for normal CI.

Never claim a live service was tested when it was not.

---

## B.17 Performance

Do not optimize blindly.

First identify:

- the actual bottleneck;
- expected workload;
- correctness constraints.

Then optimize the bottleneck.

Prefer simple optimizations with measurable benefit.

For algorithmic code, consider time complexity, space complexity, I/O, memory growth, and concurrency.

Do not sacrifice correctness for speculative performance.

---

## B.18 Compatibility

Respect the project’s declared language, framework, OS, API, database, and package constraints.

Do not upgrade versions casually.

If a change requires a version upgrade, make that dependency explicit and test the compatibility boundary.

---

## B.19 Multi-Agent Coding

When multiple agents work simultaneously:

**Isolation**

- Each agent should have a clearly defined task, clearly defined owned paths, and an isolated worktree when changes overlap risk.
- Agents must not simultaneously edit the same files.

**Communication**

Agents communicate through code, tests, documented interfaces, artifacts, commits, and task results.

Do not rely on undocumented assumptions between agents.

**Ownership**

An agent owns the files assigned to its task.

Do not overwrite another agent’s work.

If another agent’s change is required, consume it through the agreed interface or commit rather than modifying their work directly.

---

## B.20 Git Discipline

Git history should explain how the software evolved.

Use focused branches for substantial work.

Prefer small, coherent commits.

Good examples:

- `feat(auth): add token validation`
- `test(auth): cover expired tokens`
- `fix(api): handle timeout responses`
- `refactor(parser): isolate validation logic`

Bad examples: `update`, `changes`, `fix stuff`, `final final`.

Before committing, review:

```bash
git status
git diff
git diff --check
```

Then run the relevant validation.

Never commit secrets, credentials, `.env` files, virtual environments, temporary files, unrelated changes, or known broken code.

---

## B.21 Commit Atomicity

Each commit should ideally:

- have one clear purpose;
- compile or build;
- pass its relevant tests;
- be understandable independently.

Avoid mixing feature + unrelated refactor + formatting + dependency upgrade into one commit.

---

## B.22 Verification Commands

Use the project’s existing commands first.

Typical examples when configured by the project:

```bash
pytest
ruff check .
mypy .
npm test
npm run lint
npm run build
make test
```

Do not invent validation commands without checking the repository.

If the repository defines a canonical verification command, use it.

---

## B.23 Never Fake Verification

This is mandatory.

Never say “Tests pass” unless the tests were actually run.

Never say “Build works” unless the build was actually run.

Never claim an API was tested, a file was inspected, a command succeeded, or a dependency exists unless you actually verified it.

Clearly distinguish:

- **verified**
- reasoned / expected / not tested

---

## B.24 Debugging Protocol

When something fails:

1. Reproduce
2. Capture the exact failure
3. Classify the failure
4. Locate the failure boundary
5. Form a minimal hypothesis
6. Make the smallest useful change
7. Re-run the failing test
8. Run related tests
9. Run the broader suite
10. Review the diff

Do not randomly modify multiple unrelated components.

Do not repeatedly rerun a failing command without changing the relevant condition.

---

## B.25 Failure Classification

When debugging, classify the problem before fixing it:

- specification / requirement error;
- implementation bug;
- interface / contract mismatch;
- dependency issue;
- environment issue;
- test / fixture issue;
- data issue;
- concurrency / state issue;
- external-service issue;
- performance issue.

The classification determines the fix.

---

## B.26 Documentation

Update documentation when:

- public behavior changes;
- installation changes;
- configuration changes;
- CLI / API changes;
- architecture materially changes;
- a non-obvious operational requirement is introduced.

Do not create documentation for every trivial implementation detail.

Code should explain how.

Documentation should explain why and how to use it.

---

## B.27 When Requirements Are Ambiguous

Do not silently invent critical requirements.

If ambiguity affects data correctness, security, API behavior, architecture, user-visible behavior, or destructive actions, ask for clarification or explicitly state the chosen assumption.

For low-risk ambiguity, choose the simplest reasonable interpretation and document it.

---

## B.28 No Premature Architecture

Do not introduce distributed architecture because the project might eventually become large.

Start with the simplest architecture that satisfies the current requirements.

Escalate complexity only when there is evidence that the simpler design is insufficient.

Prefer:

```text
local → modular → testable → scalable later
```

over:

```text
distributed → complicated → difficult to debug
```

---

## B.29 AI-Specific Coding Rules

When using AI to modify code:

- Never trust generated code without inspection.
- Never accept a large diff without understanding it.
- Never let an agent silently expand scope.
- Require tests for meaningful changes.
- Verify external API usage against actual documentation or code.
- Prefer repository evidence over model assumptions.
- Treat generated comments and docs as potentially inaccurate.
- Remove dead or speculative code.

Agents should optimize for verified progress, not output volume.

---

## B.30 Definition of Done

A task is done when:

- Requirements are understood.
- Existing implementation was inspected.
- Requested behavior is implemented.
- Relevant edge cases are handled.
- Tests exist or existing tests adequately cover the behavior.
- Targeted tests pass.
- Relevant full-suite tests pass.
- Lint passes.
- Type checking passes where applicable.
- Build passes where applicable.
- Security implications were considered.
- No unrelated changes were introduced.
- Git diff was reviewed.
- Documentation was updated if necessary.
- Remaining limitations are known and documented.

---

## B.31 Agent Completion Report

At the end of a coding task, report:

### Changed

- What was changed.
- Important files changed.
- Any architectural decisions.

### Verification

```text
Targeted tests: <commands + result>
Full tests:     <commands + result>
Lint:           <PASS / FAIL / NOT RUN>
Type check:     <PASS / FAIL / NOT RUN>
Build:          <PASS / FAIL / NOT RUN>
```

### Git

```text
Branch:
Commit:
```

### Remaining

- Known limitations.
- Follow-up work.
- Anything intentionally not changed.

Do not hide failures.

---

## B.32 Final Rule

The goal is not to produce the most code.

The goal is to leave the repository in a state where another competent engineer can:

1. understand what changed;
2. understand why it changed;
3. reproduce the result;
4. verify the behavior;
5. safely continue the work.

When choosing between clever + complicated and simple + explicit + tested, prefer the latter unless the requirements clearly demand otherwise.
