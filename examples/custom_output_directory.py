#!/usr/bin/env python3
"""
Example: Using a custom output directory with graphify

This demonstrates how to use the GRAPHIFY_OUT environment variable
to specify a custom output directory for graphify's knowledge graph outputs.
"""

import os
import subprocess
import tempfile
from pathlib import Path


def demo_default_output():
    """Default behavior - outputs to graphify-out/"""
    print("=== Demo 1: Default Output Directory ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a sample Python file
        sample_file = Path(tmpdir) / "hello.py"
        sample_file.write_text('def greet(name):\n    return f"Hello, {name}!"')
        
        # Run graphify detect (lightweight, no LLM needed)
        result = subprocess.run(
            ["python3", "-m", "graphify.detect", tmpdir],
            capture_output=True,
            text=True
        )
        
        # Check default output location
        default_out = Path(tmpdir) / "graphify-out"
        print(f"Default output would be at: {default_out}")
        print(f"(Simulated - actual graphify commands would create this)")


def demo_custom_output_with_env():
    """Using GRAPHIFY_OUT environment variable"""
    print("\n=== Demo 2: Custom Output Directory via Environment Variable ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Set custom output directory
        custom_dir = "my-project-docs"
        os.environ["GRAPHIFY_OUT"] = custom_dir
        
        # Create a sample file
        sample_file = Path(tmpdir) / "example.py"
        sample_file.write_text('class Calculator:\n    def add(self, a, b):\n        return a + b')
        
        print(f"GRAPHIFY_OUT is set to: {custom_dir}")
        print(f"Outputs will go to: {Path(tmpdir) / custom_dir}")
        
        # Import after setting env var to see the effect
        from graphify import watch
        import importlib
        importlib.reload(watch)
        
        print(f"Module _GRAPHIFY_OUT: {watch._GRAPHIFY_OUT}")
        
        # Clean up
        del os.environ["GRAPHIFY_OUT"]


def demo_nested_output_dir():
    """Using a nested path for organized outputs"""
    print("\n=== Demo 3: Nested Output Directory ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Set nested output directory
        custom_dir = "docs/knowledge-graphs"
        os.environ["GRAPHIFY_OUT"] = custom_dir
        
        print(f"GRAPHIFY_OUT is set to: {custom_dir}")
        print(f"This is useful for integrating with existing documentation structures")
        print(f"Outputs will go to: {Path(tmpdir) / custom_dir}")
        
        # The directory structure would look like:
        print("\nDirectory structure:")
        print("project/")
        print("├── docs/")
        print("│   └── knowledge-graphs/")
        print("│       ├── graph.json")
        print("│       ├── graph.html")
        print("│       └── GRAPH_REPORT.md")
        print("└── src/")
        
        # Clean up
        del os.environ["GRAPHIFY_OUT"]


def demo_cli_usage():
    """Example CLI commands with --out flag"""
    print("\n=== Demo 4: CLI Usage Examples ===")
    
    examples = [
        "graphify . --out docs/api-graph",
        "GRAPHIFY_OUT=knowledge graphify ./src",
        "graphify ./project --out team-docs --mode deep",
        "graphify query 'how does auth work?' --graph team-docs/graph.json",
    ]
    
    print("Command examples:")
    for cmd in examples:
        print(f"  $ {cmd}")
    
    print("\nUse cases:")
    print("  - Multiple projects: each with its own graph directory")
    print("  - Team docs: output to a shared documentation folder")
    print("  - CI/CD: output to a specific artifacts directory")
    print("  - Monorepos: separate graphs for different modules")


if __name__ == "__main__":
    demo_default_output()
    demo_custom_output_with_env()
    demo_nested_output_dir()
    demo_cli_usage()
    
    print("\n=== Summary ===")
    print("✓ Set GRAPHIFY_OUT environment variable before running graphify commands")
    print("✓ Use relative paths like 'docs/graphs' or 'knowledge-out'")
    print("✓ Absolute paths work too (they replace the base path)")
    print("✓ All graphify modules respect this environment variable")
    print("✓ Default is 'graphify-out' if GRAPHIFY_OUT is not set")
