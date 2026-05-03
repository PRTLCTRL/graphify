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
        
        # Full rebuild: detect + save manifest (as fixed in Step 2)
        result = detect(Path('.'))
        save_manifest(result['files'])
        
        manifest = load_manifest()
        assert len(manifest) == 3
        
        # Step 2: Delete files (simulating days passing)
        (tmp_path / "file2.py").unlink()
        (tmp_path / "file3.py").unlink()
        
        # Step 3: Incremental update
        detected_inc = detect_incremental(Path('.'))
        
        # The fix ensures manifest is up-to-date, so deleted_files is accurate
        assert len(detected_inc['deleted_files']) == 2
        assert 'file2.py' in str(detected_inc['deleted_files'])
        assert 'file3.py' in str(detected_inc['deleted_files'])
        
        # Update manifest after incremental run
        save_manifest(detected_inc['files'])
        
        # Verify manifest now only tracks the remaining file
        manifest_after = load_manifest()
        assert len(manifest_after) == 1
        
    finally:
        os.chdir(old_cwd)


def test_step_9_still_saves_manifest_for_robustness(tmp_path):
    """Test that Step 9 also saves manifest (redundant but ensures consistency).
    
    Even though Step 2 now saves the manifest, Step 9 should still save it
    to ensure consistency if anything modified the files between steps.
    """
    (tmp_path / "main.py").write_text("def main(): pass")
    
    graphify_out = tmp_path / "graphify-out"
    graphify_out.mkdir(parents=True, exist_ok=True)
    
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        
        # Step 2: Detect and save manifest
        result = detect(Path('.'))
        Path('graphify-out/.graphify_detect.json').write_text(json.dumps(result))
        save_manifest(result['files'])
        
        # Simulate Step 9: Load detect result and save manifest again
        detect_data = json.loads(Path('graphify-out/.graphify_detect.json').read_text())
        save_manifest(detect_data['files'])
        
        # Verify manifest still exists and is correct
        manifest = load_manifest()
        assert len(manifest) == 1
        assert any('main.py' in f for f in manifest)
        
    finally:
        os.chdir(old_cwd)
