# Custom Output Directory Support - Implementation Summary

## Issue
Issue #536: Support for Unique Output Directories

## Problem Statement
Graphify hardcodes output to `graphify-out/`, making it difficult to integrate with existing documentation directories. Users want to specify custom output locations like `docs/knowledge-graph/` or other project-specific directories.

## Solution
Added a global `--out <dir>` flag that works alongside the existing `GRAPHIFY_OUT` environment variable.

### Usage Examples
```bash
# Use custom output directory
graphify . --out docs/knowledge-graph

# Works with all commands
graphify ./src --out my-docs
graphify query "auth flow" --out custom-location
graphify --out my-docs update .

# Environment variable still works
export GRAPHIFY_OUT=docs/kg
graphify .
```

## Technical Changes

### 1. CLI Argument Parsing (`graphify/__main__.py`)
- Added global `--out` flag parsing before command dispatch
- Sets `GRAPHIFY_OUT` environment variable when flag is present
- Removes flag from argv to prevent command parsers from seeing it
- Updated help text to document the new flag

### 2. Dynamic Output Directory Resolution
Changed from static module-level import to dynamic function:

**Before:**
```python
_GRAPHIFY_OUT = os.environ.get("GRAPHIFY_OUT", "graphify-out")
```

**After:**
```python
def _get_output_dir() -> str:
    """Get output directory dynamically from env var."""
    return os.environ.get("GRAPHIFY_OUT", "graphify-out")
```

Modified files:
- `graphify/cache.py` - Cache directory resolution
- `graphify/watch.py` - File watching and update detection

### 3. Documentation Updates
- Added `--out` flag to help text
- Updated `skill.md` with usage examples
- Added note about custom output in "What You Must Do When Invoked" section

## Testing

### Automated Tests (All Passing)
- `test_cache.py`: 12/12 ✓
- `test_extract.py` + `test_build.py`: 31/31 ✓
- `test_watch.py` + `test_pipeline.py`: 19/19 ✓
- Full suite: 379/380 ✓ (1 unrelated SQL test failure)

### Manual Testing
1. ✓ Environment variable sets custom output directory
2. ✓ Cache files created in custom location
3. ✓ AST extraction works with custom output
4. ✓ Default behavior (graphify-out/) still works
5. ✓ Help text displays new flag

### What Wasn't Tested
- Full end-to-end pipeline with LLM (no API keys available)
- Skill file integration with AI assistants
- Edge cases with symbolic links, network paths, etc.

## Design Decisions

### Why Environment Variable as Source of Truth?
Alternative considered: Pass output directory as parameter to every function.

**Rejected because:**
- Would require changes to 50+ function signatures
- Breaking change for existing code
- More error-prone (easy to forget to pass through)

**Chosen approach:**
- Environment variable is global and accessible anywhere
- Backward compatible with existing code
- CLI flag is just a convenience wrapper
- Single source of truth reduces bugs

### Why Dynamic Resolution?
Changed from module-level constant to function call because:
- Module-level constants are cached at import time
- Setting env var after import had no effect
- Dynamic resolution ensures changes are respected
- Minimal performance impact (function call is fast)

## Backward Compatibility
✓ Existing code continues to work
✓ GRAPHIFY_OUT environment variable still works
✓ Default behavior unchanged (graphify-out/)
✓ No breaking changes to any APIs

## Files Modified
1. `graphify/__main__.py` - CLI flag parsing, help text
2. `graphify/cache.py` - Dynamic output directory resolution
3. `graphify/watch.py` - Dynamic output directory resolution
4. `graphify/skill.md` - Documentation and usage examples

## Example Use Cases

### Case 1: Existing Documentation Directory
```bash
# Your project has docs/ folder for documentation
my-project/
├── docs/
│   ├── api/
│   └── guides/
├── src/
└── README.md

# Generate graph in docs folder
cd my-project
graphify . --out docs/knowledge-graph

# Result:
my-project/
├── docs/
│   ├── knowledge-graph/
│   │   ├── graph.json
│   │   ├── graph.html
│   │   └── GRAPH_REPORT.md
│   ├── api/
│   └── guides/
```

### Case 2: Multiple Projects
```bash
# Different output for different projects
graphify ./frontend --out docs/frontend-graph
graphify ./backend --out docs/backend-graph
graphify ./shared --out docs/shared-graph
```

### Case 3: CI/CD Integration
```bash
# Set output in build script
export GRAPHIFY_OUT=build/artifacts/graph
graphify .
```

## Notes for Reviewers
- Core functionality is solid and tested
- Change is minimal and localized (4 files)
- No breaking changes
- Ready for feedback and iteration

## Future Enhancements (Out of Scope)
- Validate output directory path before writing
- Add `--out` flag to skill file steps (currently uses env var)
- Support for multiple output directories in single run
- Config file support for persistent settings
