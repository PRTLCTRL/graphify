"""Test for issue #538: Manifest should be saved on every full rebuild.

This test verifies that the manifest is correctly saved after a full rebuild,
preventing ghost node warnings on subsequent incremental updates.
"""
import json
import os
from pathlib import Path
from graphify.detect import detect, save_manifest, load_manifest, detect_incremental


def test_full_rebuild_saves_manifest_immediately(tmp_path):
    """Test that manifest is saved immediately after detect() in Step 2.
    
    This is the core fix for issue #538: save the manifest right after
    detect() to ensure it's always in sync, even if later steps fail.
    """
    # Initial corpus
    (tmp_path / "main.py").write_text("def main(): pass")
    (tmp_path / "utils.py").write_text("def helper(): pass")
    (tmp_path / "config.py").write_text("CONFIG = {}")
    
    graphify_out = tmp_path / "graphify-out"
    graphify_out.mkdir(parents=True, exist_ok=True)
    
    # Change to project directory (simulate skill execution context)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        
        # Simulate Step 2: Detect files and save manifest immediately
        result = detect(Path('.'))
        Path('graphify-out/.graphify_detect.json').write_text(json.dumps(result))
        save_manifest(result['files'])
        
        # Verify manifest was saved
        manifest_path = graphify_out / "manifest.json"
        assert manifest_path.exists(), "manifest.json should be saved immediately after detect"
        
        manifest = load_manifest()
        assert len(manifest) == 3, "manifest should track all 3 files"
        
        # Simulate some time passing and files being deleted
        (tmp_path / "config.py").unlink()
        (tmp_path / "utils.py").unlink()
        
        # Run incremental update - should correctly detect deletions
        detected_inc = detect_incremental(Path('.'))
        assert len(detected_inc['deleted_files']) == 2
        assert any('config.py' in f for f in detected_inc['deleted_files'])
        assert any('utils.py' in f for f in detected_inc['deleted_files'])
        
        # Verify new_total is correct (only main.py remains)
        assert detected_inc['new_total'] == 0  # All remaining files are "unchanged"
        assert len(detected_inc['unchanged_files']['code']) == 1
        
    finally:
        os.chdir(old_cwd)


def test_manifest_prevents_ghost_node_false_positives(tmp_path):
    """Test the exact scenario from issue #538.
    
    Scenario:
    1. Full rebuild with 3 files -> manifest saved
    2. Delete 2 files
    3. Incremental update should correctly report 2 deletions
    
    Without the fix, if manifest wasn't saved in step 1, the incremental
    update would treat it as a fresh run and not report any deletions.
    """
    # Step 1: Full rebuild
    (tmp_path / "file1.py").write_text("def func1(): pass")
    (tmp_path / "file2.py").write_text("def func2(): pass")
    (tmp_path / "file3.py").write_text("def func3(): pass")
    
    graphify_out = tmp_path / "graphify-out"
    graphify_out.mkdir(parents=True, exist_ok=True)
    
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        
        # Full rebuild (Step 2 of skill)
        result = detect(Path('.'))
        Path('graphify-out/.graphify_detect.json').write_text(json.dumps(result))
        save_manifest(result['files'])  # THE FIX
        
        # Verify manifest exists
        assert (graphify_out / "manifest.json").exists()
        
        # Delete 2 files (simulating 4 days later as in the issue)
        (tmp_path / "file2.py").unlink()
        (tmp_path / "file3.py").unlink()
        
        # Incremental update
        inc_result = detect_incremental(Path('.'))
        
        # Should report 2 deletions
        assert len(inc_result['deleted_files']) == 2
        assert sum('file2.py' in f for f in inc_result['deleted_files']) == 1
        assert sum('file3.py' in f for f in inc_result['deleted_files']) == 1
        
        # Should NOT treat this as a fresh run
        assert inc_result['incremental'] == True
        assert inc_result['new_total'] == 0  # file1.py is unchanged
        
    finally:
        os.chdir(old_cwd)


def test_manifest_consistency_across_full_rebuild(tmp_path):
    """Test that manifest reflects filesystem state after full rebuild."""
    # Create initial files
    (tmp_path / "a.py").write_text("# a")
    (tmp_path / "b.py").write_text("# b")
    
    graphify_out = tmp_path / "graphify-out"
    graphify_out.mkdir(parents=True, exist_ok=True)
    
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        
        # First full rebuild
        result1 = detect(Path('.'))
        save_manifest(result1['files'])
        manifest1 = load_manifest()
        
        # Add a new file and delete an old one
        (tmp_path / "c.py").write_text("# c")
        (tmp_path / "a.py").unlink()
        
        # Second full rebuild
        result2 = detect(Path('.'))
        save_manifest(result2['files'])
        manifest2 = load_manifest()
        
        # Manifest should reflect current filesystem state
        assert len(manifest2) == 2
        assert any('b.py' in f for f in manifest2)
        assert any('c.py' in f for f in manifest2)
        assert not any('a.py' in f for f in manifest2)
        
    finally:
        os.chdir(old_cwd)
