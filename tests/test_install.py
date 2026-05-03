"""Tests for graphify install --platform routing."""
from pathlib import Path
from unittest.mock import patch
import pytest


PLATFORMS = {
    "claude": (".claude/skills/graphify/SKILL.md",),
    "codex": (".agents/skills/graphify/SKILL.md",),
    "opencode": (".config/opencode/skills/graphify/SKILL.md",),
    "claw": (".openclaw/skills/graphify/SKILL.md",),
    "droid": (".factory/skills/graphify/SKILL.md",),
    "trae": (".trae/skills/graphify/SKILL.md",),
    "trae-cn": (".trae-cn/skills/graphify/SKILL.md",),
    "windows": (".claude/skills/graphify/SKILL.md",),
}


def _install(tmp_path, platform):
    from graphify.__main__ import install
    with patch("graphify.__main__.Path.home", return_value=tmp_path):
        install(platform=platform)


def test_install_default_claude(tmp_path):
    _install(tmp_path, "claude")
    assert (tmp_path / ".claude" / "skills" / "graphify" / "SKILL.md").exists()


def test_install_codex(tmp_path):
    _install(tmp_path, "codex")
    assert (tmp_path / ".agents" / "skills" / "graphify" / "SKILL.md").exists()


def test_install_opencode(tmp_path):
    _install(tmp_path, "opencode")
    assert (tmp_path / ".config" / "opencode" / "skills" / "graphify" / "SKILL.md").exists()


def test_install_claw(tmp_path):
    _install(tmp_path, "claw")
    assert (tmp_path / ".openclaw" / "skills" / "graphify" / "SKILL.md").exists()


def test_install_droid(tmp_path):
    _install(tmp_path, "droid")
    assert (tmp_path / ".factory" / "skills" / "graphify" / "SKILL.md").exists()


def test_install_trae(tmp_path):
    _install(tmp_path, "trae")
    assert (tmp_path / ".trae" / "skills" / "graphify" / "SKILL.md").exists()


def test_install_trae_cn(tmp_path):
    _install(tmp_path, "trae-cn")
    assert (tmp_path / ".trae-cn" / "skills" / "graphify" / "SKILL.md").exists()


def test_install_windows(tmp_path):
    _install(tmp_path, "windows")
    assert (tmp_path / ".claude" / "skills" / "graphify" / "SKILL.md").exists()


def test_install_unknown_platform_exits(tmp_path):
    with pytest.raises(SystemExit):
        _install(tmp_path, "unknown")


def test_codex_skill_contains_spawn_agent():
    """Codex skill file must reference spawn_agent."""
    import graphify
    skill = (Path(graphify.__file__).parent / "skill-codex.md").read_text()
    assert "spawn_agent" in skill


def test_opencode_skill_contains_mention():
    """OpenCode skill file must reference @mention."""
    import graphify
    skill = (Path(graphify.__file__).parent / "skill-opencode.md").read_text()
    assert "@mention" in skill


def test_claw_skill_is_sequential():
    """OpenClaw skill file must describe sequential extraction."""
    import graphify
    skill = (Path(graphify.__file__).parent / "skill-claw.md").read_text()
    assert "sequential" in skill.lower()
    assert "spawn_agent" not in skill
    assert "@mention" not in skill


def test_all_skill_files_exist_in_package():
    """All installable platform skill files must be present in the installed package."""
    import graphify
    pkg = Path(graphify.__file__).parent
    for name in ("skill.md", "skill-codex.md", "skill-opencode.md", "skill-claw.md", "skill-windows.md", "skill-droid.md", "skill-trae.md"):
        assert (pkg / name).exists(), f"Missing: {name}"


def test_claude_install_registers_claude_md(tmp_path):
    """Claude platform install writes CLAUDE.md; others do not."""
    _install(tmp_path, "claude")
    assert (tmp_path / ".claude" / "CLAUDE.md").exists()


def test_codex_install_does_not_write_claude_md(tmp_path):
    _install(tmp_path, "codex")
    assert not (tmp_path / ".claude" / "CLAUDE.md").exists()


# --- always-on AGENTS.md install/uninstall tests ---

def _agents_install(tmp_path, platform):
    from graphify.__main__ import _agents_install as _install_fn
    _install_fn(tmp_path, platform)


def _agents_uninstall(tmp_path, platform=""):
    from graphify.__main__ import _agents_uninstall as _uninstall_fn
    _uninstall_fn(tmp_path, platform=platform)


def test_codex_agents_install_writes_agents_md(tmp_path):
    _agents_install(tmp_path, "codex")
    agents_md = tmp_path / "AGENTS.md"
    assert agents_md.exists()
    assert "graphify" in agents_md.read_text()
    assert "GRAPH_REPORT.md" in agents_md.read_text()


def test_opencode_agents_install_writes_agents_md(tmp_path):
    _agents_install(tmp_path, "opencode")
    assert (tmp_path / "AGENTS.md").exists()


def test_claw_agents_install_writes_agents_md(tmp_path):
    _agents_install(tmp_path, "claw")
    assert (tmp_path / "AGENTS.md").exists()


def test_agents_install_idempotent(tmp_path):
    """Installing twice does not duplicate the section."""
    _agents_install(tmp_path, "codex")
    _agents_install(tmp_path, "codex")
    content = (tmp_path / "AGENTS.md").read_text()
    assert content.count("## graphify") == 1


def test_agents_install_appends_to_existing(tmp_path):
    """Installs into an existing AGENTS.md without overwriting other content."""
    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# Existing rules\n\nDo not break things.\n")
    _agents_install(tmp_path, "codex")
    content = agents_md.read_text()
    assert "Do not break things." in content
    assert "## graphify" in content


def test_agents_uninstall_removes_section(tmp_path):
    _agents_install(tmp_path, "codex")
    _agents_uninstall(tmp_path)
    agents_md = tmp_path / "AGENTS.md"
    # File deleted when it only contained graphify section
    assert not agents_md.exists()


def test_agents_uninstall_preserves_other_content(tmp_path):
    """Uninstall keeps pre-existing content."""
    agents_md = tmp_path / "AGENTS.md"
    agents_md.write_text("# Existing rules\n\nDo not break things.\n")
    _agents_install(tmp_path, "codex")
    _agents_uninstall(tmp_path)
    assert agents_md.exists()
    content = agents_md.read_text()
    assert "Do not break things." in content
    assert "## graphify" not in content


def test_agents_uninstall_no_op_when_not_installed(tmp_path, capsys):
    _agents_uninstall(tmp_path)
    out = capsys.readouterr().out
    assert "nothing to do" in out


# --- OpenCode plugin tests ---

def test_opencode_agents_install_writes_plugin(tmp_path):
    """opencode install writes .opencode/plugins/graphify.js."""
    _agents_install(tmp_path, "opencode")
    plugin = tmp_path / ".opencode" / "plugins" / "graphify.js"
    assert plugin.exists()
    assert "tool.execute.before" in plugin.read_text()


def test_opencode_agents_install_registers_plugin_in_config(tmp_path):
    """opencode install registers the plugin in .opencode/opencode.json."""
    _agents_install(tmp_path, "opencode")
    config_file = tmp_path / ".opencode" / "opencode.json"
    assert config_file.exists()
    import json as _json
    config = _json.loads(config_file.read_text())
    assert any("graphify.js" in p for p in config.get("plugin", []))


def test_opencode_agents_install_merges_existing_config(tmp_path):
    """opencode install preserves existing .opencode/opencode.json keys."""
    import json as _json
    config_file = tmp_path / ".opencode" / "opencode.json"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(_json.dumps({"model": "claude-opus-4-5", "plugin": []}))
    _agents_install(tmp_path, "opencode")
    config = _json.loads(config_file.read_text())
    assert config["model"] == "claude-opus-4-5"
    assert any("graphify.js" in p for p in config["plugin"])


def test_opencode_agents_uninstall_removes_plugin(tmp_path):
    """opencode uninstall removes the plugin file and deregisters from opencode.json."""
    import json as _json
    _agents_install(tmp_path, "opencode")
    _agents_uninstall(tmp_path, platform="opencode")
    plugin = tmp_path / ".opencode" / "plugins" / "graphify.js"
    assert not plugin.exists()
    config_file = tmp_path / ".opencode" / "opencode.json"
    if config_file.exists():
        config = _json.loads(config_file.read_text())
        assert not any("graphify.js" in p for p in config.get("plugin", []))


# ── Cursor ────────────────────────────────────────────────────────────────────

def test_cursor_install_writes_rule(tmp_path):
    """cursor install writes .cursor/rules/graphify.mdc."""
    from graphify.__main__ import _cursor_install
    _cursor_install(tmp_path)
    rule = tmp_path / ".cursor" / "rules" / "graphify.mdc"
    assert rule.exists()
    content = rule.read_text()
    assert "alwaysApply: true" in content
    assert "graphify-out/GRAPH_REPORT.md" in content


def test_cursor_install_idempotent(tmp_path):
    """cursor install does not overwrite an existing rule file."""
    from graphify.__main__ import _cursor_install
    _cursor_install(tmp_path)
    rule = tmp_path / ".cursor" / "rules" / "graphify.mdc"
    original = rule.read_text()
    _cursor_install(tmp_path)
    assert rule.read_text() == original


def test_cursor_uninstall_removes_rule(tmp_path):
    """cursor uninstall removes the rule file."""
    from graphify.__main__ import _cursor_install, _cursor_uninstall
    _cursor_install(tmp_path)
    _cursor_uninstall(tmp_path)
    rule = tmp_path / ".cursor" / "rules" / "graphify.mdc"
    assert not rule.exists()


def test_cursor_uninstall_noop_if_not_installed(tmp_path):
    """cursor uninstall does nothing if rule was never written."""
    from graphify.__main__ import _cursor_uninstall
    _cursor_uninstall(tmp_path)  # should not raise


# ── Gemini CLI ────────────────────────────────────────────────────────────────

def test_gemini_install_writes_gemini_md(tmp_path):
    from graphify.__main__ import gemini_install
    gemini_install(tmp_path)
    md = tmp_path / "GEMINI.md"
    assert md.exists()
    assert "graphify-out/GRAPH_REPORT.md" in md.read_text()

def test_gemini_install_writes_hook(tmp_path):
    import json as _json
    from graphify.__main__ import gemini_install
    gemini_install(tmp_path)
    settings = _json.loads((tmp_path / ".gemini" / "settings.json").read_text())
    hooks = settings["hooks"]["BeforeTool"]
    assert any("graphify" in str(h) for h in hooks)

def test_gemini_install_idempotent(tmp_path):
    from graphify.__main__ import gemini_install
    gemini_install(tmp_path)
    gemini_install(tmp_path)
    md = tmp_path / "GEMINI.md"
    assert md.read_text().count("## graphify") == 1

def test_gemini_install_merges_existing_gemini_md(tmp_path):
    from graphify.__main__ import gemini_install
    (tmp_path / "GEMINI.md").write_text("# My project rules\n")
    gemini_install(tmp_path)
    content = (tmp_path / "GEMINI.md").read_text()
    assert "# My project rules" in content
    assert "graphify-out/GRAPH_REPORT.md" in content

def test_gemini_uninstall_removes_section(tmp_path):
    from graphify.__main__ import gemini_install, gemini_uninstall
    gemini_install(tmp_path)
    gemini_uninstall(tmp_path)
    md = tmp_path / "GEMINI.md"
    assert not md.exists()

def test_gemini_uninstall_removes_hook(tmp_path):
    import json as _json
    from graphify.__main__ import gemini_install, gemini_uninstall
    gemini_install(tmp_path)
    gemini_uninstall(tmp_path)
    settings_path = tmp_path / ".gemini" / "settings.json"
    if settings_path.exists():
        settings = _json.loads(settings_path.read_text())
        hooks = settings.get("hooks", {}).get("BeforeTool", [])
        assert not any("graphify" in str(h) for h in hooks)

def test_gemini_uninstall_noop_if_not_installed(tmp_path):
    from graphify.__main__ import gemini_uninstall
    gemini_uninstall(tmp_path)  # should not raise


# ── Codex hooks ───────────────────────────────────────────────────────────────

def test_codex_install_writes_hooks_json(tmp_path):
    """codex install writes .codex/hooks.json with graphify hook-check command."""
    from graphify.__main__ import _install_codex_hook
    import json as _json
    _install_codex_hook(tmp_path)
    hooks_path = tmp_path / ".codex" / "hooks.json"
    assert hooks_path.exists()
    hooks = _json.loads(hooks_path.read_text())
    pre_tool_hooks = hooks["hooks"]["PreToolUse"]
    assert len(pre_tool_hooks) > 0
    assert pre_tool_hooks[0]["matcher"] == "Bash"
    command = pre_tool_hooks[0]["hooks"][0]["command"]
    assert "graphify" in command
    assert "hook-check" in command


def test_codex_install_uses_absolute_path(tmp_path):
    """codex install resolves absolute path to graphify executable (Windows fix)."""
    from graphify.__main__ import _install_codex_hook
    import json as _json
    _install_codex_hook(tmp_path)
    hooks_path = tmp_path / ".codex" / "hooks.json"
    hooks = _json.loads(hooks_path.read_text())
    command = hooks["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
    # Should contain full path or at minimum "graphify hook-check"
    # On Windows, may be "C:\\...\\graphify.exe hook-check"
    # On Unix, may be "/usr/local/bin/graphify hook-check"
    assert "hook-check" in command


def test_codex_install_is_cross_platform(tmp_path):
    """codex install does not use bash-specific syntax like [ -f ] or &&."""
    from graphify.__main__ import _install_codex_hook
    import json as _json
    _install_codex_hook(tmp_path)
    hooks_path = tmp_path / ".codex" / "hooks.json"
    hooks = _json.loads(hooks_path.read_text())
    command = hooks["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
    # Bash-specific operators should NOT be present
    assert "[ -f" not in command
    assert "&&" not in command
    assert "||" not in command
    # Should use graphify hook-check instead
    assert "hook-check" in command


def test_codex_install_merges_existing_hooks(tmp_path):
    """codex install preserves existing PreToolUse hooks."""
    from graphify.__main__ import _install_codex_hook
    import json as _json
    hooks_path = tmp_path / ".codex" / "hooks.json"
    hooks_path.parent.mkdir(parents=True, exist_ok=True)
    existing_hooks = {
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [{"type": "command", "command": "echo 'user hook'"}]
                }
            ]
        }
    }
    hooks_path.write_text(_json.dumps(existing_hooks))
    _install_codex_hook(tmp_path)
    hooks = _json.loads(hooks_path.read_text())
    pre_tool_hooks = hooks["hooks"]["PreToolUse"]
    # Should have both user hook and graphify hook
    commands = [h["hooks"][0]["command"] for h in pre_tool_hooks]
    assert any("echo 'user hook'" in cmd for cmd in commands)
    assert any("hook-check" in cmd for cmd in commands)


def test_codex_install_replaces_old_graphify_hooks(tmp_path):
    """codex install removes old bash-style graphify hooks before adding new one."""
    from graphify.__main__ import _install_codex_hook
    import json as _json
    hooks_path = tmp_path / ".codex" / "hooks.json"
    hooks_path.parent.mkdir(parents=True, exist_ok=True)
    # Old v0.4.25 style hook with bash syntax
    old_hooks = {
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [{
                        "type": "command",
                        "command": "[ -f graphify-out/graph.json ] && echo '{...}' || true"
                    }]
                }
            ]
        }
    }
    hooks_path.write_text(_json.dumps(old_hooks))
    _install_codex_hook(tmp_path)
    hooks = _json.loads(hooks_path.read_text())
    pre_tool_hooks = hooks["hooks"]["PreToolUse"]
    # Old bash hook should be removed
    for hook in pre_tool_hooks:
        for h in hook["hooks"]:
            assert "[ -f" not in h["command"]
            assert "||" not in h["command"]
    # New hook should be present
    assert any("hook-check" in hook["hooks"][0]["command"] for hook in pre_tool_hooks)


def test_codex_install_idempotent(tmp_path):
    """codex install can be run multiple times without duplicating hooks."""
    from graphify.__main__ import _install_codex_hook
    import json as _json
    _install_codex_hook(tmp_path)
    _install_codex_hook(tmp_path)
    hooks_path = tmp_path / ".codex" / "hooks.json"
    hooks = _json.loads(hooks_path.read_text())
    pre_tool_hooks = hooks["hooks"]["PreToolUse"]
    # Should only have one graphify hook
    graphify_hooks = [h for h in pre_tool_hooks 
                      if any("graphify" in hook["command"] 
                            for hook in h.get("hooks", []))]
    assert len(graphify_hooks) == 1


def test_codex_uninstall_removes_hook(tmp_path):
    """codex uninstall removes graphify hook from .codex/hooks.json."""
    from graphify.__main__ import _install_codex_hook, _uninstall_codex_hook
    import json as _json
    _install_codex_hook(tmp_path)
    hooks_path = tmp_path / ".codex" / "hooks.json"
    assert hooks_path.exists()
    _uninstall_codex_hook(tmp_path)
    if hooks_path.exists():
        hooks = _json.loads(hooks_path.read_text())
        pre_tool_hooks = hooks.get("hooks", {}).get("PreToolUse", [])
        # No graphify hooks should remain
        for hook in pre_tool_hooks:
            for h in hook.get("hooks", []):
                assert "graphify" not in h.get("command", "")


def test_codex_uninstall_preserves_user_hooks(tmp_path):
    """codex uninstall keeps non-graphify hooks intact."""
    from graphify.__main__ import _install_codex_hook, _uninstall_codex_hook
    import json as _json
    hooks_path = tmp_path / ".codex" / "hooks.json"
    hooks_path.parent.mkdir(parents=True, exist_ok=True)
    user_hooks = {
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [{"type": "command", "command": "echo 'user hook'"}]
                }
            ]
        }
    }
    hooks_path.write_text(_json.dumps(user_hooks))
    _install_codex_hook(tmp_path)
    _uninstall_codex_hook(tmp_path)
    hooks = _json.loads(hooks_path.read_text())
    pre_tool_hooks = hooks["hooks"]["PreToolUse"]
    # User hook should still be there
    assert any("echo 'user hook'" in h["hooks"][0]["command"] for h in pre_tool_hooks)
    # But graphify hook should be gone
    assert not any("graphify" in str(h) for h in pre_tool_hooks)


def test_codex_uninstall_noop_if_not_installed(tmp_path):
    """codex uninstall does nothing if hooks.json doesn't exist."""
    from graphify.__main__ import _uninstall_codex_hook
    _uninstall_codex_hook(tmp_path)  # should not raise
