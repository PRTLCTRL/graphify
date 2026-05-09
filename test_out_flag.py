#!/usr/bin/env python3
"""Simple test to verify --out flag parsing."""
import sys
import subprocess
import tempfile
from pathlib import Path

# Test that --out flag is recognized
print("Test 1: Check --out flag is in help text")
result = subprocess.run(
    [sys.executable, "-m", "graphify", "--help"],
    capture_output=True,
    text=True
)
if "--out DIR" in result.stdout:
    print("✓ --out flag documented in help")
else:
    print("✗ --out flag NOT in help")
    sys.exit(1)

# Test that graphify command parsing works with --out
print("\nTest 2: Test --out flag with a simple command")
with tempfile.TemporaryDirectory() as tmpdir:
    custom_out = Path(tmpdir) / "my-custom-output"
    
    # Create a minimal test directory with one Python file
    src_dir = Path(tmpdir) / "src"
    src_dir.mkdir()
    (src_dir / "test.py").write_text("def hello(): pass\n")
    
    # Try to run graphify update with custom output dir
    # This will likely fail because we haven't built a graph yet,
    # but it should at least parse the --out flag without error
    result = subprocess.run(
        [sys.executable, "-m", "graphify", "--out", str(custom_out), "update", str(src_dir)],
        capture_output=True,
        text=True,
        cwd=tmpdir
    )
    
    print(f"Command exited with code: {result.returncode}")
    print(f"Stderr: {result.stderr[:200] if result.stderr else '(empty)'}")
    
    # Check if the custom output directory was attempted to be used
    # (it should have created the directory or at least tried to access it)
    if custom_out.exists():
        print(f"✓ Custom output directory created: {custom_out}")
    else:
        # It's OK if it doesn't exist, as long as the error isn't about command parsing
        if "unrecognized" not in result.stderr.lower() and "usage:" not in result.stderr.lower():
            print(f"✓ --out flag parsed correctly (directory not created, but no parsing error)")
        else:
            print(f"✗ Command parsing error detected")
            sys.exit(1)

print("\n✓ All tests passed!")
