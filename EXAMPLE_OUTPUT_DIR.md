# Custom Output Directory Example

This document demonstrates how to use custom output directories with graphify.

## Default Behavior

By default, graphify writes all output to `graphify-out/`:

```bash
graphify .
# Creates: graphify-out/graph.json, graphify-out/GRAPH_REPORT.md, graphify-out/graph.html
```

## Custom Output Directory

### Relative Paths

Use a relative path to create the output directory in your current location:

```bash
# Write to docs/knowledge-graph/ instead of graphify-out/
GRAPHIFY_OUT=docs/knowledge-graph graphify .

# Feature branch isolation (useful with git worktrees)
GRAPHIFY_OUT=graphify-out-feature-x graphify .

# Per-version graphs
GRAPHIFY_OUT=graphify-v2 graphify .
```

### Absolute Paths

Use an absolute path for shared team outputs or specific locations:

```bash
# Shared team documentation
GRAPHIFY_OUT=/shared/team-docs/graphify-out graphify .

# User-specific location
GRAPHIFY_OUT=$HOME/project-graphs/myproject graphify .
```

## Working with Custom Directories

All graphify commands respect the `GRAPHIFY_OUT` environment variable:

```bash
# Query the graph
GRAPHIFY_OUT=docs/knowledge-graph graphify query "how does auth work?"

# Update the graph
GRAPHIFY_OUT=docs/knowledge-graph graphify update .

# Re-cluster
GRAPHIFY_OUT=docs/knowledge-graph graphify cluster-only .
```

## Use Cases

### 1. Multiple Documentation Directories

Different graphs for different audiences:

```bash
# Developer documentation
GRAPHIFY_OUT=docs/dev graphify ./src

# API documentation  
GRAPHIFY_OUT=docs/api graphify ./api

# Architecture overview
GRAPHIFY_OUT=docs/architecture graphify .
```

### 2. Version Comparison

Track how the codebase evolves:

```bash
# Before refactor
GRAPHIFY_OUT=graphs/before graphify .

# After refactor
GRAPHIFY_OUT=graphs/after graphify .

# Compare the two graph.json files
```

### 3. Git Worktree Isolation

When working on multiple branches simultaneously:

```bash
# Main branch
git worktree add ../myproject-main main
cd ../myproject-main
GRAPHIFY_OUT=graphify-out-main graphify .

# Feature branch
git worktree add ../myproject-feature feature-x
cd ../myproject-feature
GRAPHIFY_OUT=graphify-out-feature-x graphify .
```

### 4. CI/CD Integration

Store graphs as build artifacts:

```bash
# In your CI pipeline
GRAPHIFY_OUT=build/artifacts/graph-$BUILD_NUMBER graphify .
```

## Persistence

The `GRAPHIFY_OUT` environment variable must be set for every command. To make it persistent:

### Shell Session

```bash
# Set once per terminal session
export GRAPHIFY_OUT=docs/knowledge-graph
graphify .
graphify update .
graphify query "..."
```

### Project-Specific (.envrc with direnv)

```bash
# .envrc
export GRAPHIFY_OUT=docs/knowledge-graph
```

Then run `direnv allow` and the variable will be set automatically when you enter the directory.

### Make/Task Runners

```makefile
# Makefile
GRAPHIFY_OUT := docs/knowledge-graph

.PHONY: graph
graph:
	GRAPHIFY_OUT=$(GRAPHIFY_OUT) graphify .

.PHONY: query
query:
	GRAPHIFY_OUT=$(GRAPHIFY_OUT) graphify query "$(Q)"
```

Usage: `make graph` or `make query Q="how does routing work?"`
