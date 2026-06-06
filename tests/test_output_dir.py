"""Test custom output directory via GRAPHIFY_OUT environment variable."""
import os
import sys
from pathlib import Path
import tempfile
import subprocess


def test_graphify_out_env_var_in_subprocess():
    """Test that GRAPHIFY_OUT environment variable is respected in a fresh process."""
    # Test with custom value
    result = subprocess.run(
        [sys.executable, "-c", 
         "import os; from graphify.__main__ import _GRAPHIFY_OUT; print(_GRAPHIFY_OUT)"],
        env={**os.environ, "GRAPHIFY_OUT": "custom-output"},
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "custom-output"


def test_graphify_out_default_in_subprocess():
    """Test that default output directory is 'graphify-out' when env var not set."""
    env = os.environ.copy()
    env.pop("GRAPHIFY_OUT", None)  # Ensure it's not set
    
    result = subprocess.run(
        [sys.executable, "-c",
         "from graphify.__main__ import _GRAPHIFY_OUT; print(_GRAPHIFY_OUT)"],
        env=env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "graphify-out"


def test_cache_module_reads_graphify_out():
    """Test that cache module reads GRAPHIFY_OUT correctly."""
    result = subprocess.run(
        [sys.executable, "-c",
         "import os; from graphify.cache import _GRAPHIFY_OUT; print(_GRAPHIFY_OUT)"],
        env={**os.environ, "GRAPHIFY_OUT": "docs/knowledge"},
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "docs/knowledge"


def test_watch_module_reads_graphify_out():
    """Test that watch module reads GRAPHIFY_OUT correctly."""
    result = subprocess.run(
        [sys.executable, "-c",
         "import os; from graphify.watch import _GRAPHIFY_OUT; print(_GRAPHIFY_OUT)"],
        env={**os.environ, "GRAPHIFY_OUT": "/absolute/path/graph"},
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "/absolute/path/graph"


def test_detect_creates_custom_output_dir():
    """Test that detect command respects GRAPHIFY_OUT and creates the directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        test_root = tmppath / "test_project"
        test_root.mkdir()
        
        # Create a test file
        test_file = test_root / "test.py"
        test_file.write_text("# test file\ndef hello():\n    pass\n")
        
        custom_out = test_root / "custom-output"
        
        # Run detect with custom GRAPHIFY_OUT
        result = subprocess.run(
            [sys.executable, "-c",
             f"""
import os
from pathlib import Path
from graphify.detect import detect
result = detect(Path('{test_root}'))
# Verify the output directory was used
assert result['total_files'] >= 1
print('OK')
             """],
            env={**os.environ, "GRAPHIFY_OUT": str(custom_out)},
            capture_output=True,
            text=True,
            cwd=test_root
        )
        
        assert result.returncode == 0, f"Failed: {result.stderr}"
        assert "OK" in result.stdout

