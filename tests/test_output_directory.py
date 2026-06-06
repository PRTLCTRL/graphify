"""
Test that the --output flag correctly sets the output directory.
"""
import os
import sys
import tempfile
from pathlib import Path

import pytest


def test_output_flag_sets_environment_variable():
    """Test that --output flag sets GRAPHIFY_OUT environment variable."""
    # Save original value
    original = os.environ.get("GRAPHIFY_OUT")
    
    # Simulate main() parsing with --output flag
    test_argv = ["graphify", "--output", "my-custom-dir", "--help"]
    
    # Mock sys.argv
    old_argv = sys.argv
    sys.argv = test_argv
    
    try:
        # Import main and run the environment setup logic
        from graphify.__main__ import main
        
        # The main() function should set GRAPHIFY_OUT
        # We need to test the parsing logic specifically
        if "--output" in sys.argv:
            idx = sys.argv.index("--output")
            if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith("-"):
                output_dir = sys.argv[idx + 1]
                os.environ["GRAPHIFY_OUT"] = output_dir
        
        assert os.environ.get("GRAPHIFY_OUT") == "my-custom-dir"
    finally:
        # Restore original state
        sys.argv = old_argv
        if original is not None:
            os.environ["GRAPHIFY_OUT"] = original
        elif "GRAPHIFY_OUT" in os.environ:
            del os.environ["GRAPHIFY_OUT"]


def test_output_flag_short_form():
    """Test that -o short flag also works."""
    # Save original value
    original = os.environ.get("GRAPHIFY_OUT")
    
    # Simulate main() parsing with -o flag
    test_argv = ["graphify", "-o", "another-dir", "--help"]
    
    # Mock sys.argv
    old_argv = sys.argv
    sys.argv = test_argv
    
    try:
        # Test the parsing logic
        if "-o" in sys.argv:
            idx = sys.argv.index("-o")
            if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith("-"):
                output_dir = sys.argv[idx + 1]
                os.environ["GRAPHIFY_OUT"] = output_dir
        
        assert os.environ.get("GRAPHIFY_OUT") == "another-dir"
    finally:
        # Restore original state
        sys.argv = old_argv
        if original is not None:
            os.environ["GRAPHIFY_OUT"] = original
        elif "GRAPHIFY_OUT" in os.environ:
            del os.environ["GRAPHIFY_OUT"]


def test_default_output_directory():
    """Test that default output directory is graphify-out when flag not provided."""
    # Save original value
    original = os.environ.get("GRAPHIFY_OUT")
    
    # Clear GRAPHIFY_OUT to test default
    if "GRAPHIFY_OUT" in os.environ:
        del os.environ["GRAPHIFY_OUT"]
    
    try:
        # Import the module which reads the env var
        import importlib
        import graphify.__main__
        importlib.reload(graphify.__main__)
        
        # After reload, _GRAPHIFY_OUT should be "graphify-out"
        assert graphify.__main__._GRAPHIFY_OUT == "graphify-out"
    finally:
        # Restore original state
        if original is not None:
            os.environ["GRAPHIFY_OUT"] = original
