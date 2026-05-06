"""Tests for custom output directory support via GRAPHIFY_OUT env var and --out flag."""
import os
import json
from pathlib import Path
import pytest
import sys


@pytest.fixture(autouse=True)
def reset_modules_after_test():
    """Reset imported modules after each test to avoid cross-test pollution."""
    yield
    # After test runs, reload modules to reset _GRAPHIFY_OUT to default
    import importlib
    if 'graphify.watch' in sys.modules:
        importlib.reload(sys.modules['graphify.watch'])
    if 'graphify.cache' in sys.modules:
        importlib.reload(sys.modules['graphify.cache'])
    if 'graphify.__main__' in sys.modules:
        importlib.reload(sys.modules['graphify.__main__'])


def test_graphify_out_env_var_changes_output_location(tmp_path, monkeypatch):
    """When GRAPHIFY_OUT is set, modules should use that directory instead of graphify-out."""
    custom_out = "my-custom-docs"
    monkeypatch.setenv("GRAPHIFY_OUT", custom_out)
    
    # Import fresh after setting env var
    import importlib
    import graphify.watch
    importlib.reload(graphify.watch)
    
    # The _GRAPHIFY_OUT should now be the custom value
    assert graphify.watch._GRAPHIFY_OUT == custom_out


def test_notify_only_respects_graphify_out_env_var(tmp_path, monkeypatch):
    """_notify_only should create flag in custom output directory when GRAPHIFY_OUT is set."""
    custom_out = "custom-output"
    monkeypatch.setenv("GRAPHIFY_OUT", custom_out)
    
    # Import fresh
    import importlib
    import graphify.watch
    importlib.reload(graphify.watch)
    
    # Run notify
    graphify.watch._notify_only(tmp_path)
    
    # Flag should be in custom directory
    flag = tmp_path / custom_out / "needs_update"
    assert flag.exists()
    assert flag.read_text() == "1"
    
    # Default location should NOT exist
    default_flag = tmp_path / "graphify-out" / "needs_update"
    assert not default_flag.exists()


def test_cache_module_respects_graphify_out(tmp_path, monkeypatch):
    """Cache module should use custom output directory when GRAPHIFY_OUT is set."""
    custom_out = "docs-graphs"
    monkeypatch.setenv("GRAPHIFY_OUT", custom_out)
    
    # Import fresh
    import importlib
    import graphify.cache
    importlib.reload(graphify.cache)
    
    # _GRAPHIFY_OUT should be set correctly
    assert graphify.cache._GRAPHIFY_OUT == custom_out


def test_main_module_respects_graphify_out(tmp_path, monkeypatch):
    """__main__ module should use custom output directory when GRAPHIFY_OUT is set."""
    custom_out = "project-knowledge"
    monkeypatch.setenv("GRAPHIFY_OUT", custom_out)
    
    # Import fresh
    import importlib
    import graphify.__main__
    importlib.reload(graphify.__main__)
    
    # _GRAPHIFY_OUT should be set correctly
    assert graphify.__main__._GRAPHIFY_OUT == custom_out


def test_default_output_dir_when_env_not_set(tmp_path, monkeypatch):
    """When GRAPHIFY_OUT is not set, should default to graphify-out."""
    # Ensure env var is not set
    monkeypatch.delenv("GRAPHIFY_OUT", raising=False)
    
    # Import fresh
    import importlib
    import graphify.watch
    importlib.reload(graphify.watch)
    
    # Should default to graphify-out
    assert graphify.watch._GRAPHIFY_OUT == "graphify-out"


def test_relative_custom_output_dir(tmp_path, monkeypatch):
    """Custom output directory can be a relative path."""
    custom_out = "docs/api-graphs"
    monkeypatch.setenv("GRAPHIFY_OUT", custom_out)
    
    # Import fresh
    import importlib
    import graphify.watch
    importlib.reload(graphify.watch)
    
    graphify.watch._notify_only(tmp_path)
    
    # Should create nested structure
    flag = tmp_path / custom_out / "needs_update"
    assert flag.exists()


def test_absolute_custom_output_dir(tmp_path, monkeypatch):
    """Custom output directory can be an absolute path."""
    custom_out = str(tmp_path / "absolute-output")
    monkeypatch.setenv("GRAPHIFY_OUT", custom_out)
    
    # Import fresh
    import importlib
    import graphify.watch
    importlib.reload(graphify.watch)
    
    # Create a dummy project dir
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    
    graphify.watch._notify_only(project_dir)
    
    # When _GRAPHIFY_OUT is absolute, Path(project_dir) / Path(custom_out) = Path(custom_out)
    # because joining with an absolute path replaces the previous path
    flag = Path(custom_out) / "needs_update"
    assert flag.exists()


def test_help_text_mentions_out_flag(capsys):
    """Help text should mention the --out flag."""
    from graphify.__main__ import main
    import sys
    
    # Capture help output
    old_argv = sys.argv
    sys.argv = ["graphify", "--help"]
    try:
        main()
    except SystemExit:
        pass
    finally:
        sys.argv = old_argv
    
    captured = capsys.readouterr()
    assert "--out" in captured.out
    assert "output directory" in captured.out.lower()
