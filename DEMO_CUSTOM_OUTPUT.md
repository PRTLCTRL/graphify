# Custom Output Directory Demo

This demonstrates the new `--output` flag feature for specifying custom output directories.

## Feature

Graphify now supports custom output directories via the `--output` flag or `GRAPHIFY_OUT` environment variable.

## Usage

### Method 1: Using --output flag (in AI assistant)

```bash
/graphify . --output docs/graph
```

The AI assistant will:
1. Parse the `--output docs/graph` flag
2. Export `GRAPHIFY_OUT=docs/graph`
3. Run the graphify pipeline
4. Output files will be written to `docs/graph/` instead of `graphify-out/`

### Method 2: Using environment variable (direct CLI)

```bash
# For a single command
GRAPHIFY_OUT=my-custom-dir graphify update .

# Or export it for multiple commands
export GRAPHIFY_OUT=docs/graph
graphify update .
graphify query "what connects auth to database?"
```

## Output Files

Instead of the default structure:
```
graphify-out/
├── graph.json
├── graph.html
└── GRAPH_REPORT.md
```

You get:
```
docs/graph/           # or your custom directory
├── graph.json
├── graph.html
└── GRAPH_REPORT.md
```

## Use Cases

1. **Documentation projects**: Keep your graph in `docs/knowledge-graph/`
2. **Multiple projects**: Separate graphs for different codebases
   - `GRAPHIFY_OUT=frontend-graph /graphify ./frontend`
   - `GRAPHIFY_OUT=backend-graph /graphify ./backend`
3. **CI/CD pipelines**: Output to specific artifact directories
4. **Monorepos**: Organize graphs by component

## Examples

```bash
# Generate graph in documentation directory
/graphify . --output docs/architecture

# Use absolute path
GRAPHIFY_OUT=/tmp/my-graph graphify update .

# Relative path
export GRAPHIFY_OUT=.graph
graphify update src/
```

## Technical Details

- The `--output` flag is parsed by the skill and converted to `GRAPHIFY_OUT` env var
- All graphify modules respect this environment variable
- Relative paths are resolved from the current working directory
- Absolute paths are used as-is

## Backward Compatibility

- Default behavior unchanged: outputs to `graphify-out/` when no flag is provided
- Existing scripts and workflows continue to work
- Environment variable takes precedence over default
