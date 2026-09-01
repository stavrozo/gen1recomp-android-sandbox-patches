#!/usr/bin/env python3
"""Regression checks for the verified Gen1Online sandbox.4 evolution overlay."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "upgrade_gen1online_sandbox1.py"
PATCH = ROOT / "patches" / "gen1online-gamecorner" / "evolution-stack.patch"


def load_upgrader():
    spec = importlib.util.spec_from_file_location("upgrade_gen1online_sandbox1", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load Gen1Online sandbox.4 upgrader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_overlay_targets_only_runtime_and_manifest():
    upgrader = load_upgrader()
    file_patches = upgrader.parse_unified_diff(PATCH.read_text(encoding="utf-8"))
    assert {fp.new_path for fp in file_patches} == {"main.lua", "manifest.json"}


def test_overlay_defers_mmo_level_popup_until_evolution_unwinds():
    text = PATCH.read_text(encoding="utf-8")
    assert 'local EvolutionState = require("src.ui.EvolutionState")' in text
    assert "pendingMmoLevelUp = math.max(pendingMmoLevelUp or 0, mmoLevel)" in text
    assert "if pendingMmoLevelUp and not evolutionStateActive(game) then" in text
    assert "showMmoLevelUp(game, level)" in text


def test_overlay_keeps_failed_forced_save_hypothesis_out():
    text = PATCH.read_text(encoding="utf-8")
    assert "Offline saves are written explicitly" not in text
    assert "if not isGtsServerConnected then" not in text


def test_manifest_bumps_to_sandbox4():
    text = PATCH.read_text(encoding="utf-8")
    assert '-  "version": "0.3.4.3-sandbox.1"' in text
    assert '+  "version": "0.3.4.3-sandbox.4"' in text


if __name__ == "__main__":
    test_overlay_targets_only_runtime_and_manifest()
    test_overlay_defers_mmo_level_popup_until_evolution_unwinds()
    test_overlay_keeps_failed_forced_save_hypothesis_out()
    test_manifest_bumps_to_sandbox4()
    print("Gen1Online sandbox.4 regression tests passed")
