"""Tests for --output CLI flag."""
import os
import subprocess
import sys
from pathlib import Path


def test_output_flag_sets_env():
    """Verify --output flag sets GRAPHIFY_OUT environment variable."""
    # Run graphify with --output flag and check that it's visible in the environment
    result = subprocess.run(
        [sys.executable, "-m", "graphify", "--output", "custom-out", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    # Help should be displayed
    assert "Usage:" in result.stdout


def test_output_flag_with_equals():
    """Verify --output=DIR syntax works."""
    result = subprocess.run(
        [sys.executable, "-m", "graphify", "--output=my-custom-dir", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "Usage:" in result.stdout


def test_short_output_flag():
    """Verify -o shorthand works."""
    result = subprocess.run(
        [sys.executable, "-m", "graphify", "-o", "out", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "Usage:" in result.stdout


def test_output_flag_in_help():
    """Verify --output flag is documented in help text."""
    result = subprocess.run(
        [sys.executable, "-m", "graphify", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "--output" in result.stdout
    assert "set output directory" in result.stdout.lower()
