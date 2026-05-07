"""Test custom output directory support via GRAPHIFY_OUT environment variable."""
import os
import pytest
from pathlib import Path
import sys


def test_graphify_out_env_var_respected_in_main():
    """Verify that __main__.py respects GRAPHIFY_OUT environment variable."""
    # Save original value
    orig = os.environ.get("GRAPHIFY_OUT")
    
    try:
        # Set custom output directory
        os.environ["GRAPHIFY_OUT"] = "custom-out"
        
        # Force reload to pick up the new environment variable
        if "graphify.__main__" in sys.modules:
            del sys.modules["graphify.__main__"]
        
        from graphify.__main__ import _GRAPHIFY_OUT
        assert _GRAPHIFY_OUT == "custom-out"
    finally:
        # Restore original value
        if orig is None:
            os.environ.pop("GRAPHIFY_OUT", None)
        else:
            os.environ["GRAPHIFY_OUT"] = orig
        
        # Force reload with original value
        if "graphify.__main__" in sys.modules:
            del sys.modules["graphify.__main__"]


def test_graphify_out_defaults_to_graphify_out():
    """Verify that _GRAPHIFY_OUT defaults to 'graphify-out' when not set."""
    # Save original value
    orig = os.environ.get("GRAPHIFY_OUT")
    
    try:
        # Remove environment variable if set
        os.environ.pop("GRAPHIFY_OUT", None)
        
        # Force reload
        if "graphify.__main__" in sys.modules:
            del sys.modules["graphify.__main__"]
        
        from graphify.__main__ import _GRAPHIFY_OUT
        assert _GRAPHIFY_OUT == "graphify-out"
    finally:
        # Restore original value
        if orig is not None:
            os.environ["GRAPHIFY_OUT"] = orig
        
        # Force reload with original value
        if "graphify.__main__" in sys.modules:
            del sys.modules["graphify.__main__"]


def test_graphify_out_supports_absolute_paths():
    """Verify that GRAPHIFY_OUT accepts absolute paths."""
    orig = os.environ.get("GRAPHIFY_OUT")
    
    try:
        # Set absolute path
        os.environ["GRAPHIFY_OUT"] = "/tmp/graphify-test-output"
        
        # Force reload
        if "graphify.__main__" in sys.modules:
            del sys.modules["graphify.__main__"]
        
        from graphify.__main__ import _GRAPHIFY_OUT
        assert _GRAPHIFY_OUT == "/tmp/graphify-test-output"
    finally:
        # Restore original value
        if orig is None:
            os.environ.pop("GRAPHIFY_OUT", None)
        else:
            os.environ["GRAPHIFY_OUT"] = orig
        
        # Force reload
        if "graphify.__main__" in sys.modules:
            del sys.modules["graphify.__main__"]


def test_watch_module_respects_graphify_out():
    """Verify that watch.py module respects GRAPHIFY_OUT environment variable."""
    orig = os.environ.get("GRAPHIFY_OUT")
    
    try:
        os.environ["GRAPHIFY_OUT"] = "watch-custom-out"
        
        # Force reload
        if "graphify.watch" in sys.modules:
            del sys.modules["graphify.watch"]
        
        from graphify.watch import _GRAPHIFY_OUT
        assert _GRAPHIFY_OUT == "watch-custom-out"
    finally:
        if orig is None:
            os.environ.pop("GRAPHIFY_OUT", None)
        else:
            os.environ["GRAPHIFY_OUT"] = orig
        
        if "graphify.watch" in sys.modules:
            del sys.modules["graphify.watch"]


def test_cache_module_respects_graphify_out():
    """Verify that cache.py module respects GRAPHIFY_OUT environment variable."""
    orig = os.environ.get("GRAPHIFY_OUT")
    
    try:
        os.environ["GRAPHIFY_OUT"] = "cache-custom-out"
        
        # Force reload
        if "graphify.cache" in sys.modules:
            del sys.modules["graphify.cache"]
        
        from graphify.cache import _GRAPHIFY_OUT
        assert _GRAPHIFY_OUT == "cache-custom-out"
    finally:
        if orig is None:
            os.environ.pop("GRAPHIFY_OUT", None)
        else:
            os.environ["GRAPHIFY_OUT"] = orig
        
        if "graphify.cache" in sys.modules:
            del sys.modules["graphify.cache"]
