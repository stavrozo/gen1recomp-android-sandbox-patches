#!/usr/bin/env python3
"""Regression coverage for the Gen1Online sandbox.2 evolution-save backport."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "upgrade_gen1online_sandbox1.py"


def load_upgrader():
    spec = importlib.util.spec_from_file_location("upgrade_gen1online_sandbox1", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load Gen1Online sandbox.2 upgrader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_offline_forced_save_guard():
    upgrader = load_upgrader()
    old = (
        "  performForcedSave = function(game)\n"
        "    if not game or not game.save then return end\n"
        "    if game.overworld and game.overworld.captureSave then\n"
    )
    new = upgrader.upgrade_main_lua(old)
    assert "if not isGtsServerConnected then" in new
    assert "Offline saves are written explicitly" in new
    assert "if game.overworld and game.overworld.captureSave then" in new


def test_manifest_bumps_to_sandbox2():
    upgrader = load_upgrader()
    manifest = '{"version": "0.3.4.3-sandbox.1"}'
    upgraded = upgrader.upgrade_manifest(manifest)
    assert '"version": "0.3.4.3-sandbox.2"' in upgraded


if __name__ == "__main__":
    test_offline_forced_save_guard()
    test_manifest_bumps_to_sandbox2()
    print("Gen1Online sandbox.2 regression tests passed")
