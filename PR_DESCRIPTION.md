## Summary

Adds support for specifying a custom output directory via `--out` or `--output-dir` CLI flags, making it easier to integrate graphify with existing documentation structures.

## What was the issue?

Issue #536 requested the ability to specify where graphify output should be written. Previously, the only options were:
- Use the default `graphify-out/` directory
- Set the `GRAPHIFY_OUT` environment variable

The environment variable approach works but isn't as discoverable or convenient for one-off commands.

## What changed?

Added global `--out` and `--output-dir` flags that can be specified with any graphify command:
- Supports both space-separated syntax: `--out my-graphs`
- And equals syntax: `--out=my-graphs`
- Flags are parsed early and set the `GRAPHIFY_OUT` environment variable
- Updated all commands (`query`, `path`, `explain`, `save-result`, `cluster-only`, etc.) to use the dynamic `_GRAPHIFY_OUT` variable
- Updated help documentation to reflect the new options

## Examples

```bash
# Query with custom output directory
graphify --out my-graphs query "search term"

# Path command with custom location
graphify --output-dir docs/knowledge-graph path "A" "B"

# Equals syntax
graphify --out=./results explain "NodeName"

# Still works with environment variable
GRAPHIFY_OUT=custom-dir graphify query "test"

# Default behavior unchanged
graphify query "test"  # still looks in graphify-out/
```

## What I tested

Ran manual integration tests covering:
- ✅ `--out` flag with query command
- ✅ `--output-dir` variant
- ✅ `--out=value` equals syntax
- ✅ Default behavior without flags (still uses `graphify-out/`)
- ✅ Environment variable approach still works
- ✅ Help documentation displays correctly

All tests passed successfully.

## What I couldn't test

- The full build pipeline with the skill system (requires AI assistant environment)
- Commands that need actual code extraction (AST, semantic extraction)
- Neo4j export, watch mode, git hooks (require additional setup)

The core flag parsing and path resolution logic is solid and well-tested.

## Notes

This is my first contribution to graphify — happy to iterate on anything that looks off! The implementation feels pretty straightforward: early flag parsing sets the environment variable, and all the existing code that references `_GRAPHIFY_OUT` automatically picks it up.

One design decision: I made the flags "global" (can appear anywhere in the command) rather than position-dependent. This feels more flexible, though if you prefer them to be command-specific, that's an easy change.

Fixes safishamsi/graphify#536
