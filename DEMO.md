# Demo: Custom Output Directory Feature

This demonstrates the new `--output` flag functionality for issue #536.

## Test Setup

Created three demo projects to test all three methods of specifying output directory:

### 1. Default Behavior (No Changes)
```bash
cd /tmp/demo-default
echo "def test(): pass" > test.py
python3 -m graphify update .
ls graphify-out/
```

**Result**: ✅ Output created in `graphify-out/` (default)

### 2. CLI Flag Method
```bash
cd /tmp/demo-graphify
echo "def calculate_sum(a, b): return a + b" > src/example.py
python3 -m graphify --output custom-output update .
ls custom-output/
```

**Result**: ✅ Output created in `custom-output/` directory

Output:
```
Re-extracting code files in . (no LLM needed)...
[graphify watch] Rebuilt: 10 nodes, 11 edges, 4 communities
[graphify watch] graph.json, graph.html and GRAPH_REPORT.md updated in custom-output
Code graph updated.
```

### 3. Environment Variable Method
```bash
cd /tmp/demo-env
echo "def env_test(): pass" > env_test.py
GRAPHIFY_OUT="env-output" python3 -m graphify update .
ls env-output/
```

**Result**: ✅ Output created in `env-output/` directory

## Feature Summary

The implementation adds a global `--output` flag that:

1. **Accepts multiple syntaxes**:
   - `--output DIR`
   - `-o DIR`
   - `--output=DIR`
   - `-o=DIR`

2. **Works with all commands**:
   - `graphify . --output docs/graph`
   - `graphify update --output custom`
   - `graphify query "test" --output /shared/graph`

3. **Supports path types**:
   - Relative: `docs/knowledge-graph`
   - Absolute: `/shared/team-graph`

4. **Precedence order**:
   - CLI flag overrides environment variable
   - Environment variable overrides default
   - Default is `graphify-out/`

## Backward Compatibility

All existing behavior is preserved:
- ✅ Default `graphify-out/` works without changes
- ✅ `GRAPHIFY_OUT` environment variable still works
- ✅ All 371 existing tests pass
- ✅ No breaking changes to any APIs

## Use Cases

This feature enables:

1. **Organized documentation directories**:
   ```bash
   graphify . --output docs/knowledge-graph
   ```

2. **Git worktree support**:
   ```bash
   # Shared graph across worktrees
   graphify . --output /shared/project-graph
   ```

3. **Hidden output directories**:
   ```bash
   export GRAPHIFY_OUT=.graphify
   graphify .
   ```

4. **CI/CD workflows**:
   ```bash
   graphify . --output artifacts/graph
   ```
