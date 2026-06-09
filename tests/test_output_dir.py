"""Test --output-dir flag and GRAPHIFY_OUT environment variable support."""
import json
import os
import subprocess
import tempfile
from pathlib import Path


def test_output_dir_flag_creates_custom_directory():
    """Test that --output-dir flag creates output in specified directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        test_file = tmpdir / "test.py"
        test_file.write_text("def hello(): pass\n")
        
        custom_dir = "my-custom-output"
        result = subprocess.run(
            ["python3", "-m", "graphify", "update", str(tmpdir), "--output-dir", custom_dir],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )
        
        assert result.returncode == 0, f"Command failed: {result.stderr}"
        
        # Check custom directory was created
        output_dir = tmpdir / custom_dir
        assert output_dir.exists(), f"Custom output directory {custom_dir} not created"
        
        # Check key files exist in custom directory
        assert (output_dir / "graph.json").exists(), "graph.json not in custom directory"
        assert (output_dir / "GRAPH_REPORT.md").exists(), "GRAPH_REPORT.md not in custom directory"
        assert (output_dir / "manifest.json").exists(), "manifest.json not in custom directory"
        
        # Verify default directory was NOT created
        default_dir = tmpdir / "graphify-out"
        assert not default_dir.exists() or not (default_dir / "graph.json").exists(), \
            "Output should not be in default graphify-out directory"


def test_output_dir_env_var():
    """Test that GRAPHIFY_OUT environment variable works."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        test_file = tmpdir / "test.py"
        test_file.write_text("def world(): pass\n")
        
        custom_dir = "env-var-output"
        env = os.environ.copy()
        env["GRAPHIFY_OUT"] = custom_dir
        
        result = subprocess.run(
            ["python3", "-m", "graphify", "update", str(tmpdir)],
            capture_output=True,
            text=True,
            cwd=tmpdir,
            env=env,
        )
        
        assert result.returncode == 0, f"Command failed: {result.stderr}"
        
        # Check custom directory was created
        output_dir = tmpdir / custom_dir
        assert output_dir.exists(), f"Custom output directory {custom_dir} not created"
        assert (output_dir / "graph.json").exists(), "graph.json not in custom directory"


def test_output_dir_flag_overrides_env_var():
    """Test that --output-dir flag takes precedence over GRAPHIFY_OUT env var."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        test_file = tmpdir / "test.py"
        test_file.write_text("def override(): pass\n")
        
        env_dir = "env-output"
        flag_dir = "flag-output"
        
        env = os.environ.copy()
        env["GRAPHIFY_OUT"] = env_dir
        
        result = subprocess.run(
            ["python3", "-m", "graphify", "update", str(tmpdir), "--output-dir", flag_dir],
            capture_output=True,
            text=True,
            cwd=tmpdir,
            env=env,
        )
        
        assert result.returncode == 0, f"Command failed: {result.stderr}"
        
        # Check flag directory was used
        flag_output = tmpdir / flag_dir
        assert flag_output.exists(), "Flag directory should be created"
        assert (flag_output / "graph.json").exists(), "graph.json should be in flag directory"
        
        # Check env directory was NOT used
        env_output = tmpdir / env_dir
        assert not env_output.exists() or not (env_output / "graph.json").exists(), \
            "Output should not be in env var directory when flag is provided"


def test_output_dir_absolute_path():
    """Test that --output-dir works with absolute paths."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        test_file = tmpdir / "test.py"
        test_file.write_text("def absolute(): pass\n")
        
        # Use a different temp directory for output
        with tempfile.TemporaryDirectory() as output_tmpdir:
            output_dir = Path(output_tmpdir) / "absolute-output"
            
            result = subprocess.run(
                ["python3", "-m", "graphify", "update", str(tmpdir), "--output-dir", str(output_dir)],
                capture_output=True,
                text=True,
            )
            
            assert result.returncode == 0, f"Command failed: {result.stderr}"
            
            # Check absolute path directory was created
            assert output_dir.exists(), f"Absolute output directory {output_dir} not created"
            assert (output_dir / "graph.json").exists(), "graph.json not in absolute path directory"
