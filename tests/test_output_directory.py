"""Test custom output directory via GRAPHIFY_OUT environment variable."""
import os
import tempfile
from pathlib import Path
import pytest


def test_graphify_out_env_var_respected():
    """Test that GRAPHIFY_OUT environment variable changes output directory."""
    from graphify import __main__
    
    # The module reads GRAPHIFY_OUT on import
    custom_dir = "custom-output"
    original_value = os.environ.get("GRAPHIFY_OUT")
    
    try:
        os.environ["GRAPHIFY_OUT"] = custom_dir
        # Re-import to pick up the new env var
        import importlib
        importlib.reload(__main__)
        
        # Check that _GRAPHIFY_OUT reflects the custom directory
        assert __main__._GRAPHIFY_OUT == custom_dir
    finally:
        # Restore original value
        if original_value is None:
            os.environ.pop("GRAPHIFY_OUT", None)
        else:
            os.environ["GRAPHIFY_OUT"] = original_value
        importlib.reload(__main__)


def test_graphify_out_default():
    """Test that default output directory is 'graphify-out'."""
    from graphify import __main__
    
    original_value = os.environ.get("GRAPHIFY_OUT")
    
    try:
        # Ensure no custom value is set
        os.environ.pop("GRAPHIFY_OUT", None)
        import importlib
        importlib.reload(__main__)
        
        assert __main__._GRAPHIFY_OUT == "graphify-out"
    finally:
        if original_value is not None:
            os.environ["GRAPHIFY_OUT"] = original_value
        importlib.reload(__main__)


def test_graphify_out_absolute_path():
    """Test that GRAPHIFY_OUT accepts absolute paths."""
    from graphify import __main__
    
    with tempfile.TemporaryDirectory() as tmpdir:
        custom_dir = str(Path(tmpdir) / "absolute-graphify-out")
        original_value = os.environ.get("GRAPHIFY_OUT")
        
        try:
            os.environ["GRAPHIFY_OUT"] = custom_dir
            import importlib
            importlib.reload(__main__)
            
            assert __main__._GRAPHIFY_OUT == custom_dir
        finally:
            if original_value is None:
                os.environ.pop("GRAPHIFY_OUT", None)
            else:
                os.environ["GRAPHIFY_OUT"] = original_value
            importlib.reload(__main__)
