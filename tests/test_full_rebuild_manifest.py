"""Test the full rebuild manifest save scenario from issue #538."""
import json
from pathlib import Path
from graphify.detect import detect, save_manifest, load_manifest, detect_incremental


def test_full_rebuild_then_incremental_with_deletes(tmp_path):
    """Reproduce the issue: full rebuild doesn't save manifest, incremental sees ghosts.
    
    Scenario from issue #538:
    1. Run /graphify . (full rebuild) - produces graph.json with 5,812 nodes
    2. Several deletes + new files happen
    3. Run /graphify --update (incremental)
    4. Observe: "Pruned 0 ghost nodes from 13 deleted file(s)" - incorrect!
    
    The deleted files were already absent from graph.json because the rebuild excluded them,
    but the manifest hadn't caught up because Step 9 didn't save it.
    """
    # Initial corpus
    (tmp_path / "main.py").write_text("def main(): pass")
    (tmp_path / "utils.py").write_text("def helper(): pass")
    (tmp_path / "config.py").write_text("CONFIG = {}")
    
    detect_path = tmp_path / "graphify-out" / ".graphify_detect.json"
    manifest_path = tmp_path / "graphify-out" / "manifest.json"
    detect_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Full rebuild (simulate what the skill does)
    detected = detect(tmp_path)
    detect_path.write_text(json.dumps(detected))
    
    # This is the bug: if Step 9 doesn't save the manifest, it remains stale
    # For this test, let's simulate the bug by NOT saving the manifest here
    # (In reality, Step 9 should save it, but if skipped/errors, this happens)
    
    # Step 2: Time passes, files are deleted
    (tmp_path / "config.py").unlink()
    (tmp_path / "utils.py").unlink()
    
    # Step 3: Run incremental update
    # If manifest wasn't saved after the full rebuild, it will be missing or stale
    manifest = load_manifest(str(manifest_path))
    assert len(manifest) == 0, "Manifest should be empty if Step 9 didn't save it"
    
    # Incremental detect will now see deleted_files, but...
    detected_inc = detect_incremental(tmp_path, str(manifest_path))
    
    # ...because the manifest was never saved, detect_incremental treats this as a first run
    assert detected_inc['incremental'] is True
    assert detected_inc['new_total'] == 1  # only main.py remains
    # The deleted files won't be in deleted_files if manifest was never saved
    # (they'll be in new_files or unchanged depending on the logic)
    
    # The FIX: Step 9 must ALWAYS save the manifest after a full rebuild
    # Simulate the fix: save manifest after detect
    detected_fixed = detect(tmp_path)
    save_manifest(detected_fixed['files'], str(manifest_path))
    
    # Now add and then delete a file to verify manifest tracking works
    (tmp_path / "test.py").write_text("def test(): pass")
    detected_with_test = detect(tmp_path)
    save_manifest(detected_with_test['files'], str(manifest_path))  # Update manifest
    
    # Verify test.py is in manifest
    manifest_with_test = load_manifest(str(manifest_path))
    assert any('test.py' in f for f in manifest_with_test.keys())
    
    # Delete test.py
    (tmp_path / "test.py").unlink()
    
    # Run incremental again - now it should correctly detect the deletion
    detected_inc2 = detect_incremental(tmp_path, str(manifest_path))
    assert len(detected_inc2['deleted_files']) == 1
    assert 'test.py' in ' '.join(detected_inc2['deleted_files'])


def test_skill_step_9_saves_manifest_correctly(tmp_path):
    """Verify that the skill's Step 9 code pattern works correctly."""
    import os
    
    (tmp_path / "main.py").write_text("def main(): pass")
    (tmp_path / "utils.py").write_text("def helper(): pass")
    
    graphify_out = tmp_path / "graphify-out"
    graphify_out.mkdir(parents=True, exist_ok=True)
    
    # Simulate Step 2: Detect files
    detected = detect(tmp_path)
    detect_path = graphify_out / ".graphify_detect.json"
    detect_path.write_text(json.dumps(detected))
    
    # Change to the project directory (as the skill would be run from)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        
        # Simulate Step 9: Load detect result and save manifest
        # This is the exact code from skill.md Step 9 (lines 807-811)
        detect_data = json.loads(Path('graphify-out/.graphify_detect.json').read_text())
        save_manifest(detect_data['files'])
        
        # Verify manifest was saved
        manifest_path = graphify_out / "manifest.json"
        assert manifest_path.exists(), "Step 9 should save manifest.json"
        
        manifest = load_manifest()
        assert len(manifest) == 2, "Manifest should track both files"
    finally:
        os.chdir(old_cwd)
