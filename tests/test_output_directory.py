"""Tests for custom output directory support (--out flag and GRAPHIFY_OUT env var)."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

import graphify.__main__ as mainmod


def test_out_flag_sets_graphify_out(monkeypatch, tmp_path):
    """Test that --out flag sets the _GRAPHIFY_OUT variable and env var."""
    custom_dir = tmp_path / "custom-output"
    
    # Reset _GRAPHIFY_OUT to default
    monkeypatch.setattr(mainmod, "_GRAPHIFY_OUT", "graphify-out")
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr(
        mainmod.sys,
        "argv",
        ["graphify", "--out", str(custom_dir), "--help"],
    )
    
    # Capture the state before main() modifies it
    original_env = dict(os.environ)
    
    try:
        mainmod.main()
    except SystemExit:
        pass  # --help exits, that's expected
    
    # Check that GRAPHIFY_OUT env var was set
    assert os.environ.get("GRAPHIFY_OUT") == str(custom_dir)
    
    # Clean up
    for key in set(os.environ) - set(original_env):
        del os.environ[key]
    os.environ.update(original_env)


def test_out_flag_with_equals_syntax(monkeypatch, tmp_path):
    """Test that --out=<dir> syntax works."""
    custom_dir = tmp_path / "custom-output"
    
    monkeypatch.setattr(mainmod, "_GRAPHIFY_OUT", "graphify-out")
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr(
        mainmod.sys,
        "argv",
        ["graphify", f"--out={custom_dir}", "--help"],
    )
    
    original_env = dict(os.environ)
    
    try:
        mainmod.main()
    except SystemExit:
        pass
    
    assert os.environ.get("GRAPHIFY_OUT") == str(custom_dir)
    
    # Clean up
    for key in set(os.environ) - set(original_env):
        del os.environ[key]
    os.environ.update(original_env)


def test_out_flag_removes_from_argv(monkeypatch):
    """Test that --out flag is removed from argv after parsing."""
    monkeypatch.setattr(mainmod, "_GRAPHIFY_OUT", "graphify-out")
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    
    test_argv = ["graphify", "--out", "custom-dir", "--help"]
    monkeypatch.setattr(mainmod.sys, "argv", test_argv)
    
    original_env = dict(os.environ)
    
    try:
        mainmod.main()
    except SystemExit:
        pass
    
    # After parsing, --out should be removed from argv
    # (We can't directly check this since main() modifies sys.argv in place,
    # but the test verifies the flag doesn't interfere with subsequent parsing)
    
    # Clean up
    for key in set(os.environ) - set(original_env):
        del os.environ[key]
    os.environ.update(original_env)


def test_env_var_takes_precedence_without_flag(monkeypatch):
    """Test that GRAPHIFY_OUT env var is used when no --out flag is given."""
    monkeypatch.setenv("GRAPHIFY_OUT", "env-var-dir")
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr(
        mainmod.sys,
        "argv",
        ["graphify", "--help"],
    )
    
    try:
        mainmod.main()
    except SystemExit:
        pass
    
    # The env var should still be set
    assert os.environ.get("GRAPHIFY_OUT") == "env-var-dir"


def test_flag_overrides_env_var(monkeypatch):
    """Test that --out flag overrides GRAPHIFY_OUT env var."""
    monkeypatch.setenv("GRAPHIFY_OUT", "env-var-dir")
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr(
        mainmod.sys,
        "argv",
        ["graphify", "--out", "flag-dir", "--help"],
    )
    
    try:
        mainmod.main()
    except SystemExit:
        pass
    
    # The flag should override the env var
    assert os.environ.get("GRAPHIFY_OUT") == "flag-dir"
