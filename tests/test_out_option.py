"""Tests for --out command-line option."""
import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest


def test_out_option_in_help():
    """Test that --out appears in help text."""
    from graphify.__main__ import main
    
    with patch.object(sys, 'argv', ['graphify', '--help']):
        with patch('sys.stdout') as mock_stdout:
            try:
                main()
            except SystemExit:
                pass
            
            # Check that help was printed
            calls = [str(call) for call in mock_stdout.write.call_args_list]
            help_text = ''.join([call[0][0] if call[0] else '' for call in mock_stdout.write.call_args_list])
            
            assert '--out' in help_text or any('--out' in str(call) for call in calls), \
                "Help text should mention --out option"


def test_set_output_directory():
    """Test _set_output_directory function."""
    from graphify.__main__ import _set_output_directory, _GRAPHIFY_OUT
    
    # Save original value
    original = os.environ.get("GRAPHIFY_OUT")
    
    try:
        # Test setting a custom directory
        _set_output_directory("my-custom-output")
        assert os.environ.get("GRAPHIFY_OUT") == "my-custom-output"
        
        # Test setting None (should not change anything)
        _set_output_directory(None)
        assert os.environ.get("GRAPHIFY_OUT") == "my-custom-output"
        
    finally:
        # Restore original value
        if original:
            os.environ["GRAPHIFY_OUT"] = original
        elif "GRAPHIFY_OUT" in os.environ:
            del os.environ["GRAPHIFY_OUT"]


def test_out_option_parsing():
    """Test that --out option is parsed correctly."""
    from graphify.__main__ import main
    
    # Save original value
    original = os.environ.get("GRAPHIFY_OUT")
    
    try:
        # Test with --out before command
        with patch.object(sys, 'argv', ['graphify', '--out', 'custom-dir', 'hook', 'status']):
            with patch('graphify.hooks.status', return_value="No hooks installed") as mock_status:
                with patch('builtins.print'):
                    main()
                
                # Verify the environment variable was set
                assert os.environ.get("GRAPHIFY_OUT") == "custom-dir"
                
                # Verify the command was executed
                mock_status.assert_called_once()
    finally:
        # Restore original value
        if original:
            os.environ["GRAPHIFY_OUT"] = original
        elif "GRAPHIFY_OUT" in os.environ:
            del os.environ["GRAPHIFY_OUT"]


def test_out_option_equals_syntax():
    """Test that --out=value syntax works."""
    from graphify.__main__ import main
    
    # Save original value
    original = os.environ.get("GRAPHIFY_OUT")
    
    try:
        # Test with --out=value
        with patch.object(sys, 'argv', ['graphify', '--out=another-dir', 'hook', 'status']):
            with patch('graphify.hooks.status', return_value="No hooks installed") as mock_status:
                with patch('builtins.print'):
                    main()
                
                # Verify the environment variable was set
                assert os.environ.get("GRAPHIFY_OUT") == "another-dir"
                
                # Verify the command was executed
                mock_status.assert_called_once()
    finally:
        # Restore original value
        if original:
            os.environ["GRAPHIFY_OUT"] = original
        elif "GRAPHIFY_OUT" in os.environ:
            del os.environ["GRAPHIFY_OUT"]


def test_out_option_propagates_to_modules():
    """Test that --out option affects module-level constants."""
    from graphify.__main__ import _set_output_directory
    
    # Save original value
    original = os.environ.get("GRAPHIFY_OUT")
    
    try:
        # Set a custom directory
        _set_output_directory("test-output")
        
        # Import modules after setting the env var
        # Note: This may not work for already-imported modules,
        # but new imports should pick up the env var
        import importlib
        import graphify.cache
        importlib.reload(graphify.cache)
        
        assert graphify.cache._GRAPHIFY_OUT == "test-output"
        
        import graphify.watch
        importlib.reload(graphify.watch)
        
        assert graphify.watch._GRAPHIFY_OUT == "test-output"
        
    finally:
        # Restore original value
        if original:
            os.environ["GRAPHIFY_OUT"] = original
        elif "GRAPHIFY_OUT" in os.environ:
            del os.environ["GRAPHIFY_OUT"]
        
        # Reload modules to restore original state
        import importlib
        import graphify.cache
        import graphify.watch
        importlib.reload(graphify.cache)
        importlib.reload(graphify.watch)
