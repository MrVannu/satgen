# Tests

Tests are written deliberately by the team, not generated automatically.

- **AI coding agents (Claude Code, Copilot, Codex, etc.) must not create, modify, or delete tests unless explicitly requested.** This applies to all test code: files in `tests/`, `test_*.py`, `*_test.py`, fixtures, and `conftest.py`.
- An explicit request names the test work directly, e.g. "write a test for X" or "update the tests for Y". General instructions such as "implement X", "fix Y", or "make sure it works" are **not** a request to write tests.
- If a change breaks existing tests, agents report the failure instead of changing the tests to make them pass.
- Agents may *run* the existing tests (`uv run pytest`) to check their changes.
