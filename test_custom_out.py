#!/usr/bin/env python3
"""Quick test script for custom output directory feature."""
import tempfile
import shutil
from pathlib import Path
import subprocess
import sys

def test_custom_output_dir():
    """Test that --out flag creates output in the specified directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        
        # Create a simple Python file to analyze
        code_dir = test_dir / "src"
        code_dir.mkdir()
        (code_dir / "hello.py").write_text("""
def greet(name):
    '''Say hello to someone.'''
    return f"Hello, {name}!"

def main():
    print(greet("World"))

if __name__ == "__main__":
    main()
""")
        
        # Test 1: Default output directory
        print("Test 1: Default output directory (graphify-out)")
        result = subprocess.run(
            [sys.executable, "-m", "graphify", "update", str(code_dir)],
            cwd=test_dir,
            capture_output=True,
            text=True
        )
        default_out = test_dir / "graphify-out"
        if default_out.exists():
            print(f"✓ Default directory created: {default_out}")
        else:
            print(f"✗ Default directory NOT created")
            return False
        
        # Clean up for next test
        shutil.rmtree(default_out)
        
        # Test 2: Custom output directory
        print("\nTest 2: Custom output directory (custom-graph)")
        custom_out = test_dir / "custom-graph"
        result = subprocess.run(
            [sys.executable, "-m", "graphify", "--out", str(custom_out), "update", str(code_dir)],
            cwd=test_dir,
            capture_output=True,
            text=True
        )
        if custom_out.exists():
            print(f"✓ Custom directory created: {custom_out}")
        else:
            print(f"✗ Custom directory NOT created")
            print(f"stdout: {result.stdout}")
            print(f"stderr: {result.stderr}")
            return False
        
        # Test 3: Verify graph.json exists in custom directory
        graph_json = custom_out / "graph.json"
        if graph_json.exists():
            print(f"✓ graph.json found in custom directory")
        else:
            print(f"✗ graph.json NOT found in custom directory")
            return False
        
        return True

if __name__ == "__main__":
    success = test_custom_output_dir()
    sys.exit(0 if success else 1)
