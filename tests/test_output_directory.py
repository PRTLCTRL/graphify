"""Test GRAPHIFY_OUT environment variable support for custom output directories."""
import os
import tempfile
from pathlib import Path
import pytest


def test_graphify_out_default():
    """_GRAPHIFY_OUT defaults to 'graphify-out' when environment variable is not set."""
    import graphify.__main__ as main_module
    
    original = os.environ.get("GRAPHIFY_OUT")
    try:
        if "GRAPHIFY_OUT" in os.environ:
            del os.environ["GRAPHIFY_OUT"]
        
        import importlib
        importlib.reload(main_module)
        
        assert main_module._GRAPHIFY_OUT == "graphify-out"
    finally:
        if original is not None:
            os.environ["GRAPHIFY_OUT"] = original
        importlib.reload(main_module)


def test_graphify_out_custom_relative():
    """_GRAPHIFY_OUT respects GRAPHIFY_OUT environment variable with relative path."""
    import graphify.__main__ as main_module
    
    original = os.environ.get("GRAPHIFY_OUT")
    try:
        os.environ["GRAPHIFY_OUT"] = "custom-output"
        
        import importlib
        importlib.reload(main_module)
        
        assert main_module._GRAPHIFY_OUT == "custom-output"
    finally:
        if original is not None:
            os.environ["GRAPHIFY_OUT"] = original
        else:
            del os.environ["GRAPHIFY_OUT"]
        importlib.reload(main_module)


def test_graphify_out_custom_absolute():
    """_GRAPHIFY_OUT respects GRAPHIFY_OUT environment variable with absolute path."""
    import graphify.__main__ as main_module
    
    original = os.environ.get("GRAPHIFY_OUT")
    try:
        test_path = "/tmp/graphify-test-output"
        os.environ["GRAPHIFY_OUT"] = test_path
        
        import importlib
        importlib.reload(main_module)
        
        assert main_module._GRAPHIFY_OUT == test_path
    finally:
        if original is not None:
            os.environ["GRAPHIFY_OUT"] = original
        else:
            del os.environ["GRAPHIFY_OUT"]
        importlib.reload(main_module)


def test_watch_module_respects_graphify_out():
    """watch.py module respects GRAPHIFY_OUT environment variable."""
    import graphify.watch as watch_module
    
    original = os.environ.get("GRAPHIFY_OUT")
    try:
        os.environ["GRAPHIFY_OUT"] = "custom-watch-dir"
        
        import importlib
        importlib.reload(watch_module)
        
        assert watch_module._GRAPHIFY_OUT == "custom-watch-dir"
    finally:
        if original is not None:
            os.environ["GRAPHIFY_OUT"] = original
        else:
            del os.environ["GRAPHIFY_OUT"]
        importlib.reload(watch_module)


def test_cache_module_respects_graphify_out():
    """cache.py module respects GRAPHIFY_OUT environment variable."""
    import graphify.cache as cache_module
    
    original = os.environ.get("GRAPHIFY_OUT")
    try:
        os.environ["GRAPHIFY_OUT"] = "custom-cache-dir"
        
        import importlib
        importlib.reload(cache_module)
        
        assert cache_module._GRAPHIFY_OUT == "custom-cache-dir"
    finally:
        if original is not None:
            os.environ["GRAPHIFY_OUT"] = original
        else:
            del os.environ["GRAPHIFY_OUT"]
        importlib.reload(cache_module)


def test_cache_directory_uses_graphify_out(tmp_path):
    """Cache directory is created under GRAPHIFY_OUT, not hardcoded graphify-out."""
    import graphify.cache as cache_module
    
    original = os.environ.get("GRAPHIFY_OUT")
    try:
        custom_out = "test-output"
        os.environ["GRAPHIFY_OUT"] = custom_out
        
        import importlib
        importlib.reload(cache_module)
        
        test_project = tmp_path / "test_project"
        test_project.mkdir()
        
        from graphify.cache import cache_dir
        cache_path = cache_dir(test_project)
        
        # cache_dir returns the subdirectory path (ast/ or semantic/)
        expected_parent = test_project / custom_out / "cache"
        assert cache_path.parent == expected_parent
        assert str(custom_out) in str(cache_path)
    finally:
        if original is not None:
            os.environ["GRAPHIFY_OUT"] = original
        else:
            del os.environ["GRAPHIFY_OUT"]
        importlib.reload(cache_module)


def test_update_command_respects_graphify_out(tmp_path):
    """graphify update command uses GRAPHIFY_OUT for reading saved root."""
    import graphify.__main__ as main_module
    
    original = os.environ.get("GRAPHIFY_OUT")
    try:
        custom_out = "my-graph-dir"
        os.environ["GRAPHIFY_OUT"] = custom_out
        
        import importlib
        importlib.reload(main_module)
        
        assert main_module._GRAPHIFY_OUT == custom_out
        
        test_dir = tmp_path / "project"
        test_dir.mkdir()
        output_dir = test_dir / custom_out
        output_dir.mkdir()
        
        root_file = output_dir / ".graphify_root"
        root_file.write_text(str(test_dir))
        
        assert root_file.exists()
        assert root_file.read_text() == str(test_dir)
    finally:
        if original is not None:
            os.environ["GRAPHIFY_OUT"] = original
        else:
            del os.environ["GRAPHIFY_OUT"]
        importlib.reload(main_module)
