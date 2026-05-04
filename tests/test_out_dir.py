"""Tests for --out-dir CLI argument."""
import os
import pytest
from pathlib import Path
import sys


def test_out_dir_flag_updates_env_var(tmp_path, monkeypatch, capsys):
    """--out-dir flag should update the GRAPHIFY_OUT environment variable."""
    custom_dir = str(tmp_path / "custom-output")
    
    # Mock sys.argv with --out-dir and a command that won't fail
    test_argv = ["graphify", "--out-dir", custom_dir, "hook", "status"]
    monkeypatch.setattr(sys, "argv", test_argv)
    
    # Clear any existing GRAPHIFY_OUT
    monkeypatch.delenv("GRAPHIFY_OUT", raising=False)
    
    # Import and run main
    from graphify.__main__ import main
    main()
    
    # Check that the env var was set
    assert os.environ.get("GRAPHIFY_OUT") == custom_dir


def test_out_dir_flag_equals_syntax(tmp_path, monkeypatch):
    """--out-dir=DIR syntax should also work."""
    custom_dir = str(tmp_path / "my-graphs")
    
    test_argv = ["graphify", f"--out-dir={custom_dir}", "hook", "status"]
    monkeypatch.setattr(sys, "argv", test_argv)
    monkeypatch.delenv("GRAPHIFY_OUT", raising=False)
    
    from graphify.__main__ import main
    main()
    
    assert os.environ.get("GRAPHIFY_OUT") == custom_dir


def test_out_dir_takes_precedence_over_env_var(tmp_path, monkeypatch):
    """CLI --out-dir should override GRAPHIFY_OUT environment variable."""
    env_dir = str(tmp_path / "env-dir")
    cli_dir = str(tmp_path / "cli-dir")
    
    # Set env var first
    monkeypatch.setenv("GRAPHIFY_OUT", env_dir)
    
    # Then use CLI flag
    test_argv = ["graphify", "--out-dir", cli_dir, "hook", "status"]
    monkeypatch.setattr(sys, "argv", test_argv)
    
    from graphify.__main__ import main
    main()
    
    # CLI flag should win
    assert os.environ.get("GRAPHIFY_OUT") == cli_dir


def test_out_dir_with_real_command(tmp_path, monkeypatch):
    """--out-dir should work with actual commands like query."""
    custom_dir = str(tmp_path / "output")
    graph_path = tmp_path / custom_dir / "graph.json"
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create a minimal graph.json
    import json
    graph_data = {
        "nodes": [
            {"id": "node1", "label": "Node1"},
            {"id": "node2", "label": "Node2"}
        ],
        "links": [
            {"source": "node1", "target": "node2", "relation": "uses"}
        ]
    }
    graph_path.write_text(json.dumps(graph_data))
    
    test_argv = ["graphify", "--out-dir", custom_dir, "query", "test question", "--graph", str(graph_path)]
    monkeypatch.setattr(sys, "argv", test_argv)
    monkeypatch.setenv("GRAPHIFY_OUT", custom_dir)
    
    # This should not crash
    from graphify.__main__ import main
    
    # Query command prints output, so this won't raise SystemExit
    # but we're just testing it doesn't crash
    try:
        main()
    except SystemExit:
        pass  # Some commands do exit, that's fine


def test_default_out_dir_without_flag(tmp_path, monkeypatch):
    """Without --out-dir, default should be 'graphify-out'."""
    test_argv = ["graphify", "--help"]
    monkeypatch.setattr(sys, "argv", test_argv)
    monkeypatch.delenv("GRAPHIFY_OUT", raising=False)
    
    # Re-import to get fresh module state
    import importlib
    import graphify.__main__ as main_module
    importlib.reload(main_module)
    
    # The module-level _GRAPHIFY_OUT should be default
    assert main_module._GRAPHIFY_OUT == "graphify-out"
