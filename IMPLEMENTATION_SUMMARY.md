# Implementation Summary: Custom Output Directory Support

## Issue #536: Support for Unique Output Directories

**Branch:** `cursor/output-dir-flag-42f3`  
**Commit:** `2329fd0`  
**Status:** Ready for PR

## What Was Implemented

Added `--out` and `--output-dir` global CLI flags to specify where graphify should write its output, addressing the issue where users with existing documentation directories want control over output location.

## Changes Made

### 1. CLI Flag Parsing (`graphify/__main__.py`)
- Added early parsing of `--out` / `--output-dir` flags in `main()` function
- Supports three syntaxes:
  - `--out DIR`
  - `--output-dir DIR`
  - `--out=DIR` (equals syntax)
- Sets `GRAPHIFY_OUT` environment variable when flag is provided
- Removes flags from `sys.argv` after parsing to avoid conflicts with subsequent argument processing

### 2. Updated Commands
Modified all commands to use `_GRAPHIFY_OUT` variable instead of hardcoded `"graphify-out"`:
- `query` command: Uses custom directory for graph.json lookup
- `path` command: Uses custom directory for graph.json lookup
- `explain` command: Uses custom directory for graph.json lookup
- `save-result` command: Uses custom directory for memory/ subdirectory
- `cluster-only` command: Uses custom directory for graph.json and output
- `tree` command: Already used `_GRAPHIFY_OUT`, updated help text
- `merge-graphs` command: Already used `_GRAPHIFY_OUT`, updated help text

### 3. Updated Help Documentation
- Added "Global options" section to help output
- Updated all command-specific help text to show dynamic default paths
- Uses f-strings to display current `_GRAPHIFY_OUT` value in help

## Design Decisions

1. **Global flag:** Made `--out` a global flag that can appear anywhere in the command line, not position-dependent
2. **Environment variable compatibility:** Maintains full backward compatibility with existing `GRAPHIFY_OUT` environment variable
3. **Early parsing:** Parses flags before any command execution to ensure consistent behavior
4. **No breaking changes:** Default behavior (`graphify-out/`) unchanged when flag not specified

## Testing

Created and ran manual integration tests (`test_simpler.sh`) covering:
- Basic `--out` flag functionality
- `--output-dir` variant
- `--out=value` equals syntax
- Default behavior verification
- Environment variable compatibility

**All tests passed ✓**

## Example Usage

```bash
# Use custom output directory
graphify --out my-graphs query "search term"

# Alternative flag name
graphify --output-dir docs/knowledge-graph path "A" "B"

# Equals syntax
graphify --out=./results explain "NodeName"

# Environment variable still works
GRAPHIFY_OUT=custom-dir graphify query "test"

# Default unchanged
graphify query "test"  # uses graphify-out/
```

## Limitations / Future Work

1. The skill system (skill.md) still references hardcoded `graphify-out/` paths in its embedded shell commands
   - This is intentional as skills are read by AI assistants, not executed directly by the CLI
   - A follow-up could update the skill templates to reference the environment variable

2. Some error messages and documentation strings in other modules may still mention "graphify-out"
   - These are non-critical and can be updated in follow-up PRs

## Files Changed

- `graphify/__main__.py`: +51 lines, -17 lines
  - Added flag parsing logic
  - Updated command defaults
  - Updated help documentation

## Pull Request

PR should be created from:
- **Source:** PRTLCTRL/graphify:cursor/output-dir-flag-42f3
- **Target:** safishamsi/graphify:v6

PR Description is available in: `PR_DESCRIPTION.md`

---

## For Reviewers

The implementation is minimal and focused:
1. Parse flags early → set environment variable
2. Use existing `_GRAPHIFY_OUT` variable everywhere
3. Update help text to be dynamic

No complex logic, no risk to existing functionality. The environment variable mechanism was already there; this just makes it CLI-friendly.
