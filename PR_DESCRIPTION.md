# Pull Request: Add --out flag to specify custom output directory

**Title:** feat: add --out flag to specify custom output directory

**Target:** `safishamsi/graphify` base branch `v6`  
**Branch:** `PRTLCTRL/graphify:cursor/custom-output-dir-c4fe`

**Create PR at:** https://github.com/PRTLCTRL/graphify/pull/new/cursor/custom-output-dir-c4fe

---

## What this fixes

The project always created output in `graphify-out/`, which is a bit like requiring everyone to name their cat "Mittens" — works fine until you already have a cat named "Documentation".

Fixes safishamsi/graphify#536

## Root cause

Every module hardcoded `graphify-out` directly or read from `GRAPHIFY_OUT` env var at import time, before CLI args could influence it. The env var existed but there was no CLI flag to set it, and the timing made it impossible to use effectively.

## What changed

- **Added `--out` / `--output-dir` global flag** that gets parsed before module imports
- **Updated all hardcoded references** to use the dynamic `_GRAPHIFY_OUT` variable
- **Module synchronization helper** ensures already-imported modules pick up the custom path
- **Updated skill docs** so AI assistants know how to use it

## Testing

**Ran the actual thing:**
```bash
# Default behavior still works
graphify update .
# → creates graphify-out/

# Custom path via flag
graphify --out docs/knowledge update .
# → creates docs/knowledge/

# Custom path via env var
GRAPHIFY_OUT=my-docs graphify update .
# → creates my-docs/
```

**Test coverage:**
- Unit tests verify flag parsing and help text
- Integration tests confirm files land in the right directory
- Full test suite passes (464 tests)

## What I couldn't test

I don't have the full semantic extraction pipeline running here (no API keys), so I only validated the AST extraction path. The semantic stuff should work the same way since all modules now respect `_GRAPHIFY_OUT`, but I haven't seen it run end-to-end with docs/papers/images.

## Notes

The implementation updates module-level variables after import, which is a bit cheeky but unavoidable given the CLI arg parsing happens in a module that's already part of the import chain. Works reliably across all test scenarios.

---

I'm trying to get more involved with this project — happy to iterate on this if anything looks off.
