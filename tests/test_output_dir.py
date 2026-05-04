import os
import subprocess
import tempfile
from pathlib import Path


def test_graphify_out_env_var_help_text():
    """Help text should mention GRAPHIFY_OUT environment variable."""
    import sys
    result = subprocess.run(
        [sys.executable, "-m", "graphify", "--help"],
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert "GRAPHIFY_OUT" in result.stdout
    assert "output directory" in result.stdout


def test_graphify_out_env_var_custom_dir(tmp_path):
    """GRAPHIFY_OUT environment variable should customize output directory."""
    # Create a temporary directory for the test
    test_dir = tmp_path / "test_project"
    test_dir.mkdir()
    
    # Create a simple Python file to analyze
    (test_dir / "example.py").write_text("def hello():\n    return 'world'\n")
    
    # Set custom output directory
    custom_out = test_dir / "custom-graph-dir"
    
    # Import the modules to verify they respect GRAPHIFY_OUT
    old_env = os.environ.get("GRAPHIFY_OUT")
    try:
        os.environ["GRAPHIFY_OUT"] = str(custom_out)
        
        # Re-import to pick up the new environment variable
        import importlib
        import graphify.cache as cache_module
        importlib.reload(cache_module)
        
        # Verify the module picked up the custom directory
        from graphify.cache import _GRAPHIFY_OUT
        assert _GRAPHIFY_OUT == str(custom_out)
        
    finally:
        # Restore original environment
        if old_env is not None:
            os.environ["GRAPHIFY_OUT"] = old_env
        elif "GRAPHIFY_OUT" in os.environ:
            del os.environ["GRAPHIFY_OUT"]


def test_readme_documents_custom_output_dir():
    """README should document how to use custom output directories."""
    readme_path = Path(__file__).parent.parent / "README.md"
    readme_text = readme_path.read_text()
    
    assert "GRAPHIFY_OUT" in readme_text
    assert "output directory" in readme_text.lower()
    assert "Custom output directory" in readme_text or "custom output" in readme_text.lower()
