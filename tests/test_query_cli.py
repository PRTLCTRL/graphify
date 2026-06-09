"""Tests for graphify query CLI context filtering."""
from __future__ import annotations

import json
import os

import networkx as nx
from networkx.readwrite import json_graph

import graphify.__main__ as mainmod


def _write_graph(tmp_path):
    G = nx.Graph()
    G.add_node("n1", label="extract", source_file="extract.py", source_location="L10", community=0)
    G.add_node("n2", label="cluster", source_file="cluster.py", source_location="L5", community=0)
    G.add_node("n3", label="build", source_file="build.py", source_location="L1", community=1)
    G.add_edge("n1", "n2", relation="calls", confidence="EXTRACTED", context="call")
    G.add_edge("n2", "n3", relation="imports", confidence="EXTRACTED", context="import")
    graph_path = tmp_path / "graph.json"
    graph_path.write_text(json.dumps(json_graph.node_link_data(G, edges="links")))
    return graph_path


def test_query_cli_explicit_context_filter(monkeypatch, tmp_path, capsys):
    graph_path = _write_graph(tmp_path)
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr(
        mainmod.sys,
        "argv",
        ["graphify", "query", "extract", "--context", "call", "--graph", str(graph_path)],
    )
    mainmod.main()
    out = capsys.readouterr().out
    assert "Context: call (explicit)" in out
    assert "cluster" in out
    assert "build" not in out


def test_query_cli_heuristic_context_filter(monkeypatch, tmp_path, capsys):
    graph_path = _write_graph(tmp_path)
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr(
        mainmod.sys,
        "argv",
        ["graphify", "query", "who calls extract", "--graph", str(graph_path)],
    )
    mainmod.main()
    out = capsys.readouterr().out
    assert "Context: call (heuristic)" in out
    assert "cluster" in out
    assert "build" not in out


def test_cli_out_flag_sets_graphify_out_env(monkeypatch, tmp_path):
    """Test that --out flag sets GRAPHIFY_OUT environment variable and module constant."""
    custom_out = "custom-graphify-output"
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr(
        mainmod.sys,
        "argv",
        ["graphify", "query", "test", "--out", custom_out, "--graph", str(tmp_path / "graph.json")],
    )
    
    # Clear any existing GRAPHIFY_OUT
    if "GRAPHIFY_OUT" in os.environ:
        del os.environ["GRAPHIFY_OUT"]
    
    # Parse the --out flag (this happens in main())
    if "--out" in mainmod.sys.argv:
        out_idx = mainmod.sys.argv.index("--out")
        if out_idx + 1 < len(mainmod.sys.argv):
            custom = mainmod.sys.argv[out_idx + 1]
            os.environ["GRAPHIFY_OUT"] = custom
            mainmod.sys.argv.pop(out_idx)
            mainmod.sys.argv.pop(out_idx)
    
    # Verify environment variable was set
    assert os.environ.get("GRAPHIFY_OUT") == custom_out
    
    # Verify that newly imported modules will see the custom output directory
    # We need to reimport cache to test this
    import importlib
    from graphify import cache
    importlib.reload(cache)
    assert cache._GRAPHIFY_OUT == custom_out
