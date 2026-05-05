"""Test custom output directory support via --out flag and GRAPHIFY_OUT env var."""
import os
import tempfile
from pathlib import Path
from graphify.detect import detect, _get_manifest_path


def test_custom_output_manifest_path():
    """Test that _get_manifest_path respects GRAPHIFY_OUT environment variable.
    
    Note: This tests the dynamic functions that read GRAPHIFY_OUT at call time.
    Module-level constants like _GRAPHIFY_OUT in cache.py are set at import time
    and won't change during the test run, but they will work correctly when users
    set GRAPHIFY_OUT before running graphify.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        
        # Create a simple Python file
        test_file = tmppath / "example.py"
        test_file.write_text("def hello():\n    return 'world'\n")
        
        # Set custom output directory
        custom_out = tmppath / "custom-output"
        old_env = os.environ.get("GRAPHIFY_OUT")
        try:
            os.environ["GRAPHIFY_OUT"] = str(custom_out)
            
            # Test manifest path uses custom dir
            manifest_path = _get_manifest_path()
            assert "custom-output" in manifest_path
            
            # Test detect still works
            result = detect(tmppath)
            assert result["total_files"] >= 1
            
        finally:
            # Restore original env
            if old_env is None:
                os.environ.pop("GRAPHIFY_OUT", None)
            else:
                os.environ["GRAPHIFY_OUT"] = old_env


def test_default_output_without_env():
    """Test that default graphify-out is used when env var not set."""
    old_env = os.environ.get("GRAPHIFY_OUT")
    try:
        # Clear the env var
        os.environ.pop("GRAPHIFY_OUT", None)
        
        # Should default to graphify-out
        manifest_path = _get_manifest_path()
        assert "graphify-out" in manifest_path
        
    finally:
        # Restore original env
        if old_env is not None:
            os.environ["GRAPHIFY_OUT"] = old_env
