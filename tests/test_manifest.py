"""Test manifest save/load functionality for full rebuild and incremental update."""
from pathlib import Path
from graphify.detect import detect, save_manifest, load_manifest, detect_incremental


def test_full_rebuild_saves_manifest(tmp_path):
    """Full rebuild should save manifest.json after detect()."""
    (tmp_path / "main.py").write_text("def hello(): pass")
    (tmp_path / "test.py").write_text("def test(): pass")
    
    manifest_path = tmp_path / "graphify-out" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Simulate full rebuild
    detected = detect(tmp_path)
    save_manifest(detected['files'], str(manifest_path))
    
    assert manifest_path.exists(), "manifest.json should exist after full rebuild"
    
    manifest = load_manifest(str(manifest_path))
    assert len(manifest) == 2, "manifest should track 2 files"
    

def test_incremental_rebuild_saves_manifest(tmp_path):
    """Incremental rebuild should also save manifest.json after detect_incremental()."""
    (tmp_path / "main.py").write_text("def hello(): pass")
    
    manifest_path = tmp_path / "graphify-out" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    
    # First full rebuild
    detected = detect(tmp_path)
    save_manifest(detected['files'], str(manifest_path))
    
    # Add a new file
    (tmp_path / "test.py").write_text("def test(): pass")
    
    # Incremental update
    detected_inc = detect_incremental(tmp_path, str(manifest_path))
    save_manifest(detected_inc['files'], str(manifest_path))
    
    manifest = load_manifest(str(manifest_path))
    assert len(manifest) == 2, "manifest should track both files after incremental update"


def test_manifest_prevents_ghost_nodes(tmp_path):
    """Manifest should correctly track deleted files to prevent ghost node warnings."""
    (tmp_path / "main.py").write_text("def hello(): pass")
    (tmp_path / "deleted.py").write_text("def old(): pass")
    
    manifest_path = tmp_path / "graphify-out" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Full rebuild with both files
    detected = detect(tmp_path)
    save_manifest(detected['files'], str(manifest_path))
    
    manifest = load_manifest(str(manifest_path))
    assert len(manifest) == 2
    
    # Delete one file
    (tmp_path / "deleted.py").unlink()
    
    # Run incremental - should detect the deletion
    detected_inc = detect_incremental(tmp_path, str(manifest_path))
    assert len(detected_inc['deleted_files']) == 1
    assert any('deleted.py' in f for f in detected_inc['deleted_files'])
    
    # Save manifest again - should remove deleted file
    save_manifest(detected_inc['files'], str(manifest_path))
    
    manifest_after = load_manifest(str(manifest_path))
    assert len(manifest_after) == 1, "manifest should only track the remaining file"
    assert not any('deleted.py' in f for f in manifest_after)
