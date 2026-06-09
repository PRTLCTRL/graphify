"""Tests for custom output directory via GRAPHIFY_OUT environment variable."""
import os
import pytest
from pathlib import Path
from graphify.cache import cache_dir


def test_default_output_directory():
    """Without GRAPHIFY_OUT set, default is 'graphify-out'."""
    # Save and restore original env var
    original = os.environ.get("GRAPHIFY_OUT")
    try:
        if "GRAPHIFY_OUT" in os.environ:
            del os.environ["GRAPHIFY_OUT"]
        
        # Import after clearing env var
        import importlib
        import graphify.cache
        importlib.reload(graphify.cache)
        
        # Should default to graphify-out
        expected = Path("graphify-out")
        assert graphify.cache._GRAPHIFY_OUT == "graphify-out"
    finally:
        if original:
            os.environ["GRAPHIFY_OUT"] = original


def test_custom_output_directory_relative(tmp_path):
    """GRAPHIFY_OUT can be set to a relative path."""
    original = os.environ.get("GRAPHIFY_OUT")
    try:
        os.environ["GRAPHIFY_OUT"] = "custom-output"
        
        # Reload module to pick up env var
        import importlib
        import graphify.cache
        importlib.reload(graphify.cache)
        
        assert graphify.cache._GRAPHIFY_OUT == "custom-output"
        
        # Verify cache_dir uses the custom path
        custom_cache = cache_dir(root=tmp_path, kind="ast")
        assert "custom-output" in str(custom_cache)
        assert custom_cache.exists()
    finally:
        if original:
            os.environ["GRAPHIFY_OUT"] = original
        else:
            if "GRAPHIFY_OUT" in os.environ:
                del os.environ["GRAPHIFY_OUT"]
        # Reload to restore original
        import importlib
        import graphify.cache
        importlib.reload(graphify.cache)


def test_custom_output_directory_absolute(tmp_path):
    """GRAPHIFY_OUT can be set to an absolute path."""
    original = os.environ.get("GRAPHIFY_OUT")
    custom_dir = tmp_path / "my-custom-graphify"
    
    try:
        os.environ["GRAPHIFY_OUT"] = str(custom_dir)
        
        # Reload module to pick up env var
        import importlib
        import graphify.cache
        importlib.reload(graphify.cache)
        
        assert graphify.cache._GRAPHIFY_OUT == str(custom_dir)
        
        # Verify cache_dir uses the custom path
        custom_cache = cache_dir(root=tmp_path, kind="semantic")
        assert str(custom_dir) in str(custom_cache)
        assert custom_cache.exists()
    finally:
        if original:
            os.environ["GRAPHIFY_OUT"] = original
        else:
            if "GRAPHIFY_OUT" in os.environ:
                del os.environ["GRAPHIFY_OUT"]
        # Reload to restore original
        import importlib
        import graphify.cache
        importlib.reload(graphify.cache)


def test_custom_output_prevents_collision(tmp_path):
    """Different GRAPHIFY_OUT values create separate cache directories."""
    original = os.environ.get("GRAPHIFY_OUT")
    
    try:
        # First output directory
        os.environ["GRAPHIFY_OUT"] = "output-a"
        import importlib
        import graphify.cache
        importlib.reload(graphify.cache)
        
        cache_a = cache_dir(root=tmp_path, kind="ast")
        test_file_a = cache_a / "test.json"
        test_file_a.write_text('{"test": "a"}')
        
        # Second output directory
        os.environ["GRAPHIFY_OUT"] = "output-b"
        importlib.reload(graphify.cache)
        
        cache_b = cache_dir(root=tmp_path, kind="ast")
        test_file_b = cache_b / "test.json"
        test_file_b.write_text('{"test": "b"}')
        
        # Verify they're in different locations
        assert cache_a != cache_b
        assert test_file_a.read_text() == '{"test": "a"}'
        assert test_file_b.read_text() == '{"test": "b"}'
        assert "output-a" in str(cache_a)
        assert "output-b" in str(cache_b)
    finally:
        if original:
            os.environ["GRAPHIFY_OUT"] = original
        else:
            if "GRAPHIFY_OUT" in os.environ:
                del os.environ["GRAPHIFY_OUT"]
        # Reload to restore original
        import importlib
        import graphify.cache
        importlib.reload(graphify.cache)
