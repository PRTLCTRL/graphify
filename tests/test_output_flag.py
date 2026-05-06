"""Tests for custom output directory via --output flag."""
import os
import sys
from pathlib import Path
from graphify.__main__ import _process_output_flag


def test_output_flag_sets_env_var(monkeypatch):
    """Test that --output flag sets GRAPHIFY_OUT environment variable."""
    # Clean environment
    monkeypatch.delenv("GRAPHIFY_OUT", raising=False)
    
    # Simulate command line with --output flag
    test_argv = ["graphify", "query", "test", "--output", "custom-dir"]
    monkeypatch.setattr(sys, "argv", test_argv.copy())
    
    _process_output_flag()
    
    assert os.environ.get("GRAPHIFY_OUT") == "custom-dir"
    # Flag should be removed from argv
    assert "--output" not in sys.argv
    assert "custom-dir" not in sys.argv


def test_output_flag_short_form(monkeypatch):
    """Test that -o short form works."""
    monkeypatch.delenv("GRAPHIFY_OUT", raising=False)
    
    test_argv = ["graphify", "query", "test", "-o", "short-dir"]
    monkeypatch.setattr(sys, "argv", test_argv.copy())
    
    _process_output_flag()
    
    assert os.environ.get("GRAPHIFY_OUT") == "short-dir"
    assert "-o" not in sys.argv


def test_output_flag_equals_syntax(monkeypatch):
    """Test that --output=dir syntax works."""
    monkeypatch.delenv("GRAPHIFY_OUT", raising=False)
    
    test_argv = ["graphify", "--output=equals-dir", "query", "test"]
    monkeypatch.setattr(sys, "argv", test_argv.copy())
    
    _process_output_flag()
    
    assert os.environ.get("GRAPHIFY_OUT") == "equals-dir"
    assert "--output=equals-dir" not in sys.argv


def test_output_flag_preserves_existing_env(monkeypatch):
    """Test that CLI flag overrides existing GRAPHIFY_OUT env var."""
    monkeypatch.setenv("GRAPHIFY_OUT", "env-dir")
    
    test_argv = ["graphify", "--output", "cli-dir", "query", "test"]
    monkeypatch.setattr(sys, "argv", test_argv.copy())
    
    _process_output_flag()
    
    # CLI flag should override env var
    assert os.environ.get("GRAPHIFY_OUT") == "cli-dir"


def test_no_output_flag_preserves_env(monkeypatch):
    """Test that GRAPHIFY_OUT env var is preserved when no flag is given."""
    monkeypatch.setenv("GRAPHIFY_OUT", "env-dir")
    
    test_argv = ["graphify", "query", "test"]
    monkeypatch.setattr(sys, "argv", test_argv.copy())
    
    _process_output_flag()
    
    # Env var should be unchanged
    assert os.environ.get("GRAPHIFY_OUT") == "env-dir"


def test_no_output_flag_no_env(monkeypatch):
    """Test that no flag and no env var leaves GRAPHIFY_OUT unset."""
    monkeypatch.delenv("GRAPHIFY_OUT", raising=False)
    
    test_argv = ["graphify", "query", "test"]
    monkeypatch.setattr(sys, "argv", test_argv.copy())
    
    _process_output_flag()
    
    # Should remain unset (module default will be used)
    assert "GRAPHIFY_OUT" not in os.environ


def test_output_flag_absolute_path(monkeypatch):
    """Test that absolute paths work with --output flag."""
    monkeypatch.delenv("GRAPHIFY_OUT", raising=False)
    
    test_argv = ["graphify", "--output", "/absolute/path/to/output", "query", "test"]
    monkeypatch.setattr(sys, "argv", test_argv.copy())
    
    _process_output_flag()
    
    assert os.environ.get("GRAPHIFY_OUT") == "/absolute/path/to/output"
