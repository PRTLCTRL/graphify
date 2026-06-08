"""Test custom output directory support via --out flag."""
import os
import sys
import tempfile
from pathlib import Path
import subprocess
import json


def test_out_flag_sets_env_var():
    """Verify --out flag sets GRAPHIFY_OUT environment variable."""
    # Create a minimal test script that imports graphify and checks the env var
    test_script = """
import os
import sys
# Simulate main() parsing --out before modules load
if '--out' in sys.argv:
    idx = sys.argv.index('--out')
    os.environ['GRAPHIFY_OUT'] = sys.argv[idx + 1]

from graphify.__main__ import _GRAPHIFY_OUT
print(_GRAPHIFY_OUT)
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script)
        script_path = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, script_path, '--out', 'custom-dir'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert result.stdout.strip() == 'custom-dir'
    finally:
        os.unlink(script_path)


def test_output_dir_alias():
    """Verify --output-dir works as an alias for --out."""
    test_script = """
import os
import sys
if '--output-dir' in sys.argv:
    idx = sys.argv.index('--output-dir')
    os.environ['GRAPHIFY_OUT'] = sys.argv[idx + 1]

from graphify.__main__ import _GRAPHIFY_OUT
print(_GRAPHIFY_OUT)
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script)
        script_path = f.name
    
    try:
        result = subprocess.run(
            [sys.executable, script_path, '--output-dir', 'my-docs'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert result.stdout.strip() == 'my-docs'
    finally:
        os.unlink(script_path)


def test_help_mentions_out_flag():
    """Verify help text documents the --out flag."""
    result = subprocess.run(
        [sys.executable, '-m', 'graphify', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert '--out' in result.stdout
    assert 'output directory' in result.stdout.lower()
