"""Test custom output directory via GRAPHIFY_OUT env var."""
import os
import json
from pathlib import Path
from graphify.detect import detect, _is_noise_dir


def test_graphify_out_env_var_default(tmp_path):
    """Test that GRAPHIFY_OUT defaults to 'graphify-out'."""
    # Ensure env var is not set
    old_val = os.environ.pop("GRAPHIFY_OUT", None)
    try:
        # Re-import to pick up the default
        import importlib
        import graphify.detect
        importlib.reload(graphify.detect)
        
        from graphify.detect import _GRAPHIFY_OUT
        assert _GRAPHIFY_OUT == "graphify-out"
    finally:
        if old_val is not None:
            os.environ["GRAPHIFY_OUT"] = old_val


def test_graphify_out_env_var_custom(tmp_path):
    """Test that GRAPHIFY_OUT can be customized via env var."""
    custom_dir = "docs/knowledge-graph"
    os.environ["GRAPHIFY_OUT"] = custom_dir
    
    try:
        # Re-import to pick up the custom value
        import importlib
        import graphify.detect
        importlib.reload(graphify.detect)
        
        from graphify.detect import _GRAPHIFY_OUT
        assert _GRAPHIFY_OUT == custom_dir
    finally:
        os.environ.pop("GRAPHIFY_OUT", None)


def test_is_noise_dir_respects_custom_output(tmp_path):
    """Test that _is_noise_dir skips the custom output directory."""
    custom_dir = "my-custom-output"
    os.environ["GRAPHIFY_OUT"] = custom_dir
    
    try:
        # Re-import to pick up the custom value
        import importlib
        import graphify.detect
        importlib.reload(graphify.detect)
        
        from graphify.detect import _is_noise_dir
        
        # Should skip the custom output dir
        assert _is_noise_dir(custom_dir) is True
        
        # Should not skip random dirs
        assert _is_noise_dir("src") is False
    finally:
        os.environ.pop("GRAPHIFY_OUT", None)


def test_detect_ignores_custom_output_dir(tmp_path):
    """Test that detect() ignores files in the custom output directory."""
    custom_out = "custom-graphify-out"
    os.environ["GRAPHIFY_OUT"] = custom_out
    
    try:
        # Re-import modules to pick up env var
        import importlib
        import graphify.detect
        importlib.reload(graphify.detect)
        
        # Create test structure
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "main.py").write_text("print('hello')")
        
        out_dir = tmp_path / custom_out
        out_dir.mkdir()
        (out_dir / "graph.json").write_text('{"nodes": []}')
        
        # Run detect
        result = detect(tmp_path)
        
        # Should find the source file
        code_files = result["files"].get("code", [])
        assert any("main.py" in str(f) for f in code_files)
        
        # Should NOT find the output file
        all_files = [f for files in result["files"].values() for f in files]
        assert not any(custom_out in str(f) for f in all_files)
    finally:
        os.environ.pop("GRAPHIFY_OUT", None)
