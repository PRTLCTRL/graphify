#!/usr/bin/env python3
"""
Demonstration of the --out flag feature for custom output directories.
This script shows how the new feature works in practice.
"""
import tempfile
import subprocess
import sys
from pathlib import Path


def demo():
    """Demonstrate the --out flag with a simple example."""
    
    print("=" * 70)
    print("DEMO: Custom Output Directory Support (Issue #536)")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create a simple project
        print("\n📁 Creating demo project...")
        (tmpdir / "main.py").write_text("""
def authenticate_user(username, password):
    '''Validate user credentials.'''
    return username and password

def process_request(request):
    '''Handle incoming request.'''
    return authenticate_user(request.user, request.password)
""")
        
        (tmpdir / "utils.py").write_text("""
def validate_email(email):
    '''Check if email format is valid.'''
    return '@' in email

def sanitize_input(data):
    '''Clean user input.'''
    return data.strip()
""")
        
        print(f"   Created demo project in {tmpdir}")
        print(f"   - main.py (auth functions)")
        print(f"   - utils.py (helper functions)")
        
        # Test 1: Default behavior (graphify-out/)
        print("\n📊 Test 1: Default output directory")
        print("   Running graphify without --out flag...")
        
        import os
        from graphify.extract import extract
        from graphify.cache import cache_dir
        
        # Clear any custom env var
        if 'GRAPHIFY_OUT' in os.environ:
            del os.environ['GRAPHIFY_OUT']
        
        default_cache = cache_dir(tmpdir, 'ast')
        print(f"   ✓ Default cache location: {default_cache.relative_to(tmpdir)}")
        assert 'graphify-out' in str(default_cache)
        
        # Test 2: Custom output via env var
        print("\n📊 Test 2: Custom directory via GRAPHIFY_OUT env var")
        os.environ['GRAPHIFY_OUT'] = 'my-docs'
        
        custom_cache = cache_dir(tmpdir, 'ast')
        print(f"   ✓ Custom cache location: {custom_cache.relative_to(tmpdir)}")
        assert 'my-docs' in str(custom_cache)
        
        # Test 3: Extraction with custom output
        print("\n📊 Test 3: Running extraction with custom output")
        code_files = list(tmpdir.glob("*.py"))
        result = extract(code_files, cache_root=tmpdir)
        
        print(f"   ✓ Extracted {len(result['nodes'])} nodes, {len(result['edges'])} edges")
        print(f"   ✓ Cache created in: {custom_cache.relative_to(tmpdir)}")
        
        cache_files = list(custom_cache.glob("*.json"))
        print(f"   ✓ Generated {len(cache_files)} cache files")
        
        # Clean up
        del os.environ['GRAPHIFY_OUT']
        
        # Test 4: Show how --out flag would work
        print("\n📊 Test 4: How to use the --out flag")
        print("   Command line examples:")
        print("   $ graphify . --out docs/knowledge-graph")
        print("   $ graphify ./src --out my-project-docs  ")
        print("   $ graphify query 'auth flow' --out custom-location")
        
        print("\n✅ All demos completed successfully!")
        print("\n" + "=" * 70)
        print("Summary:")
        print("  • Default output: graphify-out/")
        print("  • Custom output: Set via --out flag or GRAPHIFY_OUT env var")
        print("  • Use case: Place graphs in existing docs/ directories")
        print("=" * 70)


if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"\n❌ Demo failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
