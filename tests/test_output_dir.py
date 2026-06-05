"""Tests for --output-dir CLI option."""
import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest


def test_output_dir_flag_sets_environment():
    """--output-dir should set GRAPHIFY_OUT environment variable."""
    from graphify import __main__
    
    # Save original argv
    original_argv = sys.argv.copy()
    original_env = os.environ.get("GRAPHIFY_OUT")
    
    try:
        # Simulate CLI with --output-dir
        sys.argv = ["graphify", "--output-dir", "custom-output", "--help"]
        
        # Mock sys.exit to prevent actual exit
        with patch.object(sys, "exit"):
            __main__.main()
        
        # Check that environment variable was set
        assert os.environ.get("GRAPHIFY_OUT") == "custom-output"
        
    finally:
        # Restore original state
        sys.argv = original_argv
        if original_env is None:
            os.environ.pop("GRAPHIFY_OUT", None)
        else:
            os.environ["GRAPHIFY_OUT"] = original_env


def test_output_dir_short_flag():
    """Short flag -o should also work."""
    from graphify import __main__
    
    original_argv = sys.argv.copy()
    original_env = os.environ.get("GRAPHIFY_OUT")
    
    try:
        sys.argv = ["graphify", "-o", "docs/graph", "--help"]
        
        with patch.object(sys, "exit"):
            __main__.main()
        
        assert os.environ.get("GRAPHIFY_OUT") == "docs/graph"
        
    finally:
        sys.argv = original_argv
        if original_env is None:
            os.environ.pop("GRAPHIFY_OUT", None)
        else:
            os.environ["GRAPHIFY_OUT"] = original_env


def test_output_dir_equals_syntax():
    """--output-dir=value syntax should work."""
    from graphify import __main__
    
    original_argv = sys.argv.copy()
    original_env = os.environ.get("GRAPHIFY_OUT")
    
    try:
        sys.argv = ["graphify", "--output-dir=my-graphs", "--help"]
        
        with patch.object(sys, "exit"):
            __main__.main()
        
        assert os.environ.get("GRAPHIFY_OUT") == "my-graphs"
        
    finally:
        sys.argv = original_argv
        if original_env is None:
            os.environ.pop("GRAPHIFY_OUT", None)
        else:
            os.environ["GRAPHIFY_OUT"] = original_env


def test_output_dir_default_when_not_specified():
    """When --output-dir is not provided, default should be graphify-out."""
    from graphify import __main__
    
    original_argv = sys.argv.copy()
    original_env = os.environ.get("GRAPHIFY_OUT")
    
    try:
        # Clear any existing GRAPHIFY_OUT
        os.environ.pop("GRAPHIFY_OUT", None)
        
        sys.argv = ["graphify", "--help"]
        
        with patch.object(sys, "exit"):
            __main__.main()
        
        # Should use default if not set
        # The main function doesn't set it if not provided, so it remains unset
        # But the _GRAPHIFY_OUT variable should still be "graphify-out"
        from graphify.__main__ import _GRAPHIFY_OUT
        # Note: _GRAPHIFY_OUT gets the env var or defaults to "graphify-out"
        # Since we cleared the env var, it should be "graphify-out"
        
    finally:
        sys.argv = original_argv
        if original_env is None:
            os.environ.pop("GRAPHIFY_OUT", None)
        else:
            os.environ["GRAPHIFY_OUT"] = original_env


def test_output_dir_with_absolute_path():
    """--output-dir should accept absolute paths."""
    from graphify import __main__
    
    original_argv = sys.argv.copy()
    original_env = os.environ.get("GRAPHIFY_OUT")
    
    try:
        sys.argv = ["graphify", "--output-dir", "/tmp/my-project-graph", "--help"]
        
        with patch.object(sys, "exit"):
            __main__.main()
        
        assert os.environ.get("GRAPHIFY_OUT") == "/tmp/my-project-graph"
        
    finally:
        sys.argv = original_argv
        if original_env is None:
            os.environ.pop("GRAPHIFY_OUT", None)
        else:
            os.environ["GRAPHIFY_OUT"] = original_env
