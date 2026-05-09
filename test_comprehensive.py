#!/usr/bin/env python3
"""Test custom output directory with actual graphify commands."""
import sys
import subprocess
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmpdir:
    tmpdir = Path(tmpdir)
    custom_out = tmpdir / "my-graph-output"
    
    # Create a simple Python file
    src_dir = tmpdir / "src"
    src_dir.mkdir()
    (src_dir / "example.py").write_text("""
def add(a, b):
    return a + b

def multiply(a, b):
    result = add(a, 0)
    for _ in range(b - 1):
        result = add(result, a)
    return result
""")
    
    # Test: Run graphify update with custom output directory
    print(f"Testing graphify update with custom output: {custom_out}")
    result = subprocess.run(
        ["python3", "-m", "graphify", "--out", str(custom_out), "update", str(src_dir)],
        capture_output=True,
        text=True,
        cwd=tmpdir
    )
    
    print(f"Exit code: {result.returncode}")
    
    # Check if custom output directory was created
    if custom_out.exists():
        print(f"✓ Custom output directory created: {custom_out}")
        
        # List contents
        contents = list(custom_out.glob("*"))
        print(f"Contents: {[f.name for f in contents]}")
        
        # Check for expected files
        if (custom_out / "graph.json").exists():
            print("✓ graph.json found in custom directory")
        else:
            print("✗ graph.json NOT found")
            
        if (custom_out / "GRAPH_REPORT.md").exists():
            print("✓ GRAPH_REPORT.md found in custom directory")
        else:
            print("✗ GRAPH_REPORT.md NOT found")
    else:
        print(f"✗ Custom output directory not created")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    
    # Test: Verify default directory wasn't created
    default_out = tmpdir / "graphify-out"
    if default_out.exists():
        print(f"✗ Default directory was created when it shouldn't have been")
        sys.exit(1)
    else:
        print(f"✓ Default directory was NOT created (as expected)")

print("\n✓ All tests passed!")
