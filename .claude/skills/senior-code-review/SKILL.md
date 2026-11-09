---
name: senior-code-review
description: Perform a thorough code review focusing on performance, security, architecture, best practices, codebase consistency, scalability, and reusability. Use when the user asks for a code review, requests PR feedback, says "review this", "check my code", or when examining code changes before merge.
---

# Senior Code Review

Review code with the rigor of a principal engineer. Prioritize issues that cause real damage in production over stylistic preferences.

## Review Process

1. *Understand scope*: Read all changed files. Identify the intent of the change.
2. *Check surrounding code*: Read neighboring functions, imports, and callers to understand existing patterns.
3. *Analyze each focus area* (below) against every changed file.
4. *Produce the output* in the exact format specified.

## Focus Areas

### Performance

- Unnecessary allocations, copies, or re-renders in hot paths
- N+1 queries, missing indexes, unbounded result sets
- Missing caching opportunities or cache invalidation bugs
- Blocking the event loop (sync I/O, CPU-heavy work without offloading)
- Quadratic or worse algorithmic complexity where linear is possible
- Memory leaks (unclosed streams, dangling listeners, growing maps)

### Security

- Injection risks (SQL, NoSQL, command, template)
- Improper input validation or sanitization
- Secrets, tokens, or credentials in code or logs
- Missing authentication or authorization checks
- Unsafe deserialization, prototype pollution, path traversal
- Overly permissive CORS, CSP, or header configuration
- Sensitive data in error messages or stack traces

### Architecture

- Violations of existing module boundaries or layering
- Circular dependencies or tight coupling between unrelated modules
- Business logic leaking into transport/presentation layers
- God objects or functions doing too many things
- Missing abstractions that would simplify the code
- Inconsistent use of established project patterns

### Best Practices & Principles

- Violated single responsibility, open-closed, or dependency inversion
- Missing or misleading error handling (swallowed errors, empty catches)
- Race conditions in concurrent or async code
- Mutable shared state without synchronization
- Dead code, unreachable branches, or redundant checks
- Insufficient or brittle test coverage for the change

### Codebase Consistency

- Naming that deviates from existing conventions (casing, terminology)
- Different patterns for the same problem already solved elsewhere
- Import style or module structure inconsistencies
- Duplicated logic that already exists as a utility

### Scalability & Reusability

- Hard-coded values that should be configurable
- Tightly coupled to a specific use case when a general solution is straightforward
- Data structures that won't scale with growth
- Missing pagination, rate limiting, or backpressure

## Output Format

Present findings as a flat bullet list grouped by file. Each issue must include the full file path, exact line number(s), and a suggested fix.

Use two severity levels:

- *Must Fix* -- Bugs, security holes, data loss risks, performance regressions, or architectural violations that will cause real problems.
- *Nice to Have* -- Improvements to clarity, consistency, or maintainability that are not urgent.

## Must Fix

- `server/users/repository.py:42` -- SQL injection: `user_id` is interpolated into a raw query string.
 **Fix**: Use a parameterized query and pass `user_id` as a bound parameter instead of string formatting.

- `server/orders/handlers.py:118-125` -- The list endpoint loads every row without a limit and can exhaust memory as the table grows.
 **Fix**: Accept bounded `limit` / `offset` parameters (with a sane maximum) and apply them to the query.

## Nice to Have

- `client/utils/format.ts:7` -- `formatDate` duplicates date formatting already implemented in `client/utils/time.ts:23`.
 **Fix**: Reuse the existing `formatTimestamp()` helper from `time.ts`.

### Rules

- Always include the full relative file path and line number(s).
- Write the suggested fix as a concrete description, not vague advice. Include a code snippet when it makes the fix unambiguous.
- If no issues are found in a severity tier, omit that section entirely.
- Keep the list focused -- flag real issues, not style nitpicks the linter already catches.
- When the fix requires broader refactoring, note the scope and trade-offs briefly.
