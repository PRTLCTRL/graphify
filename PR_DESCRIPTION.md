# PR Title
Add support for custom output directories via --out flag

# PR Description

## The Problem

Out of the box, graphify always writes to `graphify-out/` in the current directory. If you've already got a `docs/` folder or some other well-established documentation structure, you're stuck either symlinking, moving files around post-build, or just accepting that your graph lives in a separate directory. Not ideal.

## What Changed

Added a global `--out <dir>` flag that lets you tell graphify where to put its output. It works exactly like the existing `GRAPHIFY_OUT` environment variable (which still works), but now it's easier to use on the command line.

**Usage:**
```bash
graphify . --out docs/knowledge-graph
graphify ./src --out my-project-docs
graphify query "auth flow" --out custom-location
```

**Technical changes:**
- Modified `graphify/__main__.py` to parse `--out` flag before command dispatch and set `GRAPHIFY_OUT` env var
- Refactored `graphify/cache.py` and `graphify/watch.py` to read `GRAPHIFY_OUT` dynamically instead of caching at module load time (so setting it via flag actually works)
- Updated help text and `skill.md` documentation to mention the flag

## What I Tested

**What I actually ran:**
1. Created a test project with Python files, ran extraction with custom output dir via env var — verified cache ends up in the right place
2. Ran `graphify --help` — confirmed new flag shows up in usage
3. Ran existing test suite:
   - `test_cache.py`: 12/12 passed
   - `test_extract.py` + `test_build.py`: 31/31 passed  
   - `test_watch.py` + `test_pipeline.py`: 19/19 passed
   - Full suite: 379/380 passed (one unrelated SQL parsing failure)

**What I couldn't test:**
- Full end-to-end pipeline on a large real-world codebase (no LLM API keys in this environment)
- The skill file integration with actual AI assistants (Claude Code, Cursor, etc.)
- Edge cases with absolute vs relative paths across different filesystems

The core functionality works — output directory is respected by cache, extraction, and watch commands. If there's a scenario I missed or something breaks in production, I'm happy to iterate.

## Why This Approach

I considered making output directory a parameter on every function, but that would've been a huge invasive change touching dozens of files. Using the environment variable as the single source of truth keeps the change localized and backward-compatible — existing code that reads `GRAPHIFY_OUT` continues to work, and the flag is just a convenience wrapper.

Fixes safishamsi/graphify#536

---

I'm trying to get more involved with this project — happy to iterate on this if anything looks off.
