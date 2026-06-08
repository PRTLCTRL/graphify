"""Integration test for custom output directory."""
import os
import subprocess
import tempfile
import shutil
from pathlib import Path


def test_custom_output_dir_integration():
    """Test that --out flag creates files in the specified directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / "test-project"
        test_dir.mkdir()
        
        # Create a simple Python file
        (test_dir / "sample.py").write_text('def hello(): return "world"')
        
        # Run graphify update with custom output dir
        custom_out = test_dir / "my-docs"
        result = subprocess.run(
            ["graphify", "--out", str(custom_out), "update", str(test_dir)],
            capture_output=True,
            text=True,
            cwd=test_dir,
            env={**os.environ, "PATH": "/home/ubuntu/.local/bin:" + os.environ.get("PATH", "")}
        )
        
        # Check if custom directory was created
        assert custom_out.exists(), f"Custom output directory {custom_out} was not created"
        
        # Check if graph.json was created in custom directory
        graph_json = custom_out / "graph.json"
        assert graph_json.exists(), f"graph.json not found in {custom_out}"
        
        # Verify default directory was NOT created
        default_out = test_dir / "graphify-out"
        assert not default_out.exists(), f"Default directory {default_out} should not exist"


def test_env_var_output_dir():
    """Test that GRAPHIFY_OUT env var works."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / "test-project"
        test_dir.mkdir()
        
        # Create a simple Python file
        (test_dir / "sample.py").write_text('def foo(): pass')
        
        # Run graphify update with GRAPHIFY_OUT env var
        custom_out = test_dir / "env-custom-dir"
        env = os.environ.copy()
        env["GRAPHIFY_OUT"] = str(custom_out)
        env["PATH"] = "/home/ubuntu/.local/bin:" + env.get("PATH", "")
        
        result = subprocess.run(
            ["graphify", "update", str(test_dir)],
            capture_output=True,
            text=True,
            cwd=test_dir,
            env=env
        )
        
        # Check if custom directory was created
        assert custom_out.exists(), f"Custom output directory {custom_out} was not created"
        
        # Verify default directory was NOT created
        default_out = test_dir / "graphify-out"
        assert not default_out.exists(), f"Default directory {default_out} should not exist"
