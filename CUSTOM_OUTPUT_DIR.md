# Custom Output Directory Support

As of this PR, graphify supports specifying a custom output directory for all generated files (graph.json, GRAPH_REPORT.md, graph.html, etc.).

## Usage

### Method 1: Environment Variable

Set the `GRAPHIFY_OUT` environment variable before running any graphify commands:

```bash
export GRAPHIFY_OUT=docs/knowledge-graph
/graphify .
```

All outputs will now go to `docs/knowledge-graph/` instead of the default `graphify-out/`.

### Method 2: In AI Assistant Skills

When using graphify through AI assistants (Claude Code, Cursor, etc.), set the environment variable in the `/graphify` command:

```bash
export GRAPHIFY_OUT=my-custom-dir
/graphify ./src
```

The skill will automatically use this directory for all operations.

## Examples

### Organize by project component

```bash
# Backend graph
GRAPHIFY_OUT=docs/backend-graph /graphify ./backend

# Frontend graph  
GRAPHIFY_OUT=docs/frontend-graph /graphify ./frontend
```

### Integrate with existing docs

```bash
# Place graph in your team's existing documentation folder
export GRAPHIFY_OUT=team-docs/architecture
/graphify .
```

### CI/CD artifacts

```bash
# Output to build artifacts directory
export GRAPHIFY_OUT=build/artifacts/knowledge-graph
graphify ./src
```

## Directory Behavior

- **Relative paths**: Created relative to the project root
  - `GRAPHIFY_OUT=docs/graphs` → creates `./docs/graphs/`
  
- **Absolute paths**: Used as-is, but Path behavior means they replace the base
  - `GRAPHIFY_OUT=/shared/graphs` → creates `/shared/graphs/`
  - Note: In most cases, relative paths are recommended for portability

- **Default**: If `GRAPHIFY_OUT` is not set, defaults to `graphify-out`

## What's Affected

The custom output directory affects:

- Core outputs:
  - `graph.json` - the knowledge graph
  - `GRAPH_REPORT.md` - analysis report
  - `graph.html` - interactive visualization
  
- Cache and metadata:
  - `cache/` - extraction cache directory
  - `.graphify_python` - Python interpreter path
  - `.graphify_root` - scan root for updates
  - `manifest.json` - file modification tracking
  
- Temporary files during build:
  - `.graphify_detect.json`
  - `.graphify_ast.json`
  - `.graphify_semantic.json`
  - `.graphify_extract.json`
  
- Optional outputs (if enabled):
  - `wiki/` - agent-crawlable wiki
  - `graph.svg` - static visualization
  - `graph.graphml` - Gephi/yEd export
  - `cypher.txt` - Neo4j import script

## Technical Details

### Module Support

All graphify modules read the `GRAPHIFY_OUT` environment variable:

- `graphify.__main__` - CLI entry point
- `graphify.watch` - file watching and update detection
- `graphify.cache` - extraction cache management
- `graphify.detect` - file discovery (via manifest path)
- `graphify.transcribe` - video/audio transcript storage

### Python API

When using graphify as a library:

```python
import os
os.environ["GRAPHIFY_OUT"] = "my-output-dir"

# Now import and use graphify modules
from graphify.detect import detect
from graphify.watch import _notify_only

# They will all use "my-output-dir" instead of "graphify-out"
```

## Migration

Existing projects continue to work without changes - the default behavior is unchanged. To migrate:

1. Decide on your new output directory structure
2. Set `GRAPHIFY_OUT` in your environment or CI config
3. Run `/graphify .` to regenerate the graph in the new location
4. Update any references to `graphify-out/` in your docs or scripts
5. (Optional) Add the old `graphify-out/` to `.gitignore` if not already there

## Why This Feature?

Many projects already have established documentation directories where graphify outputs should live. Examples:

- **Monorepos**: Separate graphs for different modules (e.g., `packages/api/docs/graph`, `packages/web/docs/graph`)
- **Team conventions**: Organization-wide docs structure (e.g., `docs/architecture/knowledge-graph`)
- **CI/CD**: Build artifacts go to specific directories (e.g., `build/reports/graphify`)
- **Versioned docs**: Multiple graphs for different branches or releases

This PR resolves issue #536 by making the output directory configurable via environment variable, which works seamlessly with all existing graphify commands and AI assistant skills.
