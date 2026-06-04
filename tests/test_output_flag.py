"""Tests for custom output directory flag (--output, --out, -o)."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


def test_output_flag_long_form():
    """Test --output flag sets custom output directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        test_file = test_dir / "test.py"
        test_file.write_text("def hello(): return 'world'", encoding="utf-8")
        
        custom_out = test_dir / "custom-output"
        result = subprocess.run(
            [sys.executable, "-m", "graphify", "--output", str(custom_out), "update", str(test_dir)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        assert result.returncode == 0, f"Command failed: {result.stderr}"
        assert custom_out.exists(), "Custom output directory was not created"
        assert (custom_out / "graph.json").exists(), "graph.json not in custom directory"
        assert (custom_out / "GRAPH_REPORT.md").exists(), "GRAPH_REPORT.md not in custom directory"
        # Default output dir should not be created
        assert not (test_dir / "graphify-out").exists(), "Default output dir should not exist"


def test_output_flag_short_form():
    """Test -o flag (short form) sets custom output directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        test_file = test_dir / "test.py"
        test_file.write_text("class Test: pass", encoding="utf-8")
        
        custom_out = test_dir / "my-graphs"
        result = subprocess.run(
            [sys.executable, "-m", "graphify", "-o", str(custom_out), "update", str(test_dir)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        assert result.returncode == 0, f"Command failed: {result.stderr}"
        assert custom_out.exists(), "Custom output directory was not created"
        assert (custom_out / "graph.json").exists(), "graph.json not in custom directory"


def test_output_flag_equals_syntax():
    """Test --output=path syntax."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        test_file = test_dir / "test.py"
        test_file.write_text("x = 1", encoding="utf-8")
        
        custom_out = test_dir / "equals-syntax"
        result = subprocess.run(
            [sys.executable, "-m", "graphify", f"--output={custom_out}", "update", str(test_dir)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        assert result.returncode == 0, f"Command failed: {result.stderr}"
        assert custom_out.exists(), "Custom output directory was not created"
        assert (custom_out / "graph.json").exists(), "graph.json not in custom directory"


def test_output_flag_nested_path():
    """Test --output with nested directory path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        test_file = test_dir / "test.py"
        test_file.write_text("def nested(): pass", encoding="utf-8")
        
        custom_out = test_dir / "docs" / "graphs" / "v1"
        result = subprocess.run(
            [sys.executable, "-m", "graphify", "--output", str(custom_out), "update", str(test_dir)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        assert result.returncode == 0, f"Command failed: {result.stderr}"
        assert custom_out.exists(), "Nested output directory was not created"
        assert (custom_out / "graph.json").exists(), "graph.json not in nested directory"


def test_output_flag_absolute_path():
    """Test --output with absolute path."""
    with tempfile.TemporaryDirectory() as tmpdir1:
        with tempfile.TemporaryDirectory() as tmpdir2:
            test_dir = Path(tmpdir1)
            test_file = test_dir / "test.py"
            test_file.write_text("def absolute(): pass", encoding="utf-8")
            
            custom_out = Path(tmpdir2) / "absolute-out"
            result = subprocess.run(
                [sys.executable, "-m", "graphify", "--output", str(custom_out), "update", str(test_dir)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            assert result.returncode == 0, f"Command failed: {result.stderr}"
            assert custom_out.exists(), "Absolute path output directory was not created"
            assert (custom_out / "graph.json").exists(), "graph.json not in absolute path directory"


def test_output_flag_without_value_fails():
    """Test that --output without a value shows an error."""
    result = subprocess.run(
        [sys.executable, "-m", "graphify", "--output"],
        capture_output=True,
        text=True,
        timeout=5,
    )
    
    assert result.returncode != 0, "Command should fail without value"
    assert "requires a directory path" in result.stderr, "Error message should mention missing path"


def test_output_flag_help_text():
    """Test that --output flag is documented in help text."""
    result = subprocess.run(
        [sys.executable, "-m", "graphify", "--help"],
        capture_output=True,
        text=True,
        timeout=5,
    )
    
    assert result.returncode == 0, "Help should succeed"
    assert "--output" in result.stdout, "--output flag should be in help"
    assert "--out" in result.stdout, "--out alias should be in help"
    assert "-o" in result.stdout, "-o short form should be in help"
    assert "GRAPHIFY_OUT" in result.stdout, "Environment variable should be mentioned"
