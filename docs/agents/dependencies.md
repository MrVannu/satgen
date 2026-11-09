# Dependencies

- Pin every direct dependency exactly (`==`) in `pyproject.toml`, including the `dev` group. Do not use `>=`, `~=` or other ranges.
- Add dependencies with `uv add <pkg>` (or `uv add --dev <pkg>`). `[tool.uv] add-bounds = "exact"` makes uv write the `==` pin automatically. Never edit versions by hand without running `uv lock` afterwards.
- Commit `uv.lock` together with `pyproject.toml`. It pins transitive dependencies.
- To upgrade a package, run `uv add <pkg>==<new-version>`. Don't run a bare `uv lock --upgrade`.
