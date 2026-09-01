#!/usr/bin/env python3
"""Upgrade the known Gen1Online v0.3.4.3 sandbox.1 package to sandbox.2.

sandbox.2 backports the newer Gen1Online behavior that forced saves do not run
while the online service is disconnected. This avoids firing Game:writeSave()
inside the pokemon.evolved event while Gen1Recomp is still unwinding the Rare
Candy evolution UI stack.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

MAIN_PATH = "main.lua"
MANIFEST_PATH = "manifest.json"
SANDBOX1_MAIN_SHA256 = "0f3c34f8f742ec9577f6be66d8cf6d7ee81d3070fd45d47c52cab4287f16d05f"
SANDBOX1_MANIFEST_SHA256 = "89ad0fb7e91cc221b0b109b68831f39b5243257d7d9a1c2a309a0db4336070c8"

_OLD_SAVE_PREFIX = """  performForcedSave = function(game)\n    if not game or not game.save then return end\n    if game.overworld and game.overworld.captureSave then\n"""
_NEW_SAVE_PREFIX = """  performForcedSave = function(game)\n    if not game or not game.save then return end\n    if not isGtsServerConnected then\n      -- Offline saves are written explicitly by the in-game Save menu.\n      -- Do not force Game:writeSave() from pokemon.evolved while the\n      -- evolution UI stack is still unwinding.\n      return\n    end\n    if game.overworld and game.overworld.captureSave then\n"""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def upgrade_main_lua(text: str) -> str:
    count = text.count(_OLD_SAVE_PREFIX)
    if count != 1:
        raise ValueError(f"expected one Gen1Online performForcedSave block, found {count}")
    return text.replace(_OLD_SAVE_PREFIX, _NEW_SAVE_PREFIX, 1)


def upgrade_manifest(text: str) -> str:
    old = '"version": "0.3.4.3-sandbox.1"'
    new = '"version": "0.3.4.3-sandbox.2"'
    count = text.count(old)
    if count != 1:
        raise ValueError(f"expected one sandbox.1 manifest version, found {count}")
    return text.replace(old, new, 1)


def default_output(source: Path) -> Path:
    name = source.name
    if "sandbox.1" in name:
        name = name.replace("sandbox.1", "sandbox.2", 1)
    else:
        name = source.stem + "-sandbox.2" + source.suffix
    return source.with_name(name)


def upgrade_zip(source: Path, output: Path) -> None:
    with zipfile.ZipFile(source, "r") as src:
        infos = src.infolist()
        payload = {i.filename: src.read(i.filename) for i in infos if not i.is_dir()}

    main = payload.get(MAIN_PATH)
    manifest = payload.get(MANIFEST_PATH)
    if main is None or manifest is None:
        raise ValueError("package is missing main.lua or manifest.json")
    if sha256(main) != SANDBOX1_MAIN_SHA256:
        raise ValueError("main.lua is not the verified sandbox.1 build")
    if sha256(manifest) != SANDBOX1_MANIFEST_SHA256:
        raise ValueError("manifest.json is not the verified sandbox.1 build")

    payload[MAIN_PATH] = upgrade_main_lua(main.decode("utf-8")).encode("utf-8")
    payload[MANIFEST_PATH] = upgrade_manifest(manifest.decode("utf-8")).encode("utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as dst:
        for info in infos:
            if info.is_dir() or info.filename not in payload:
                continue
            clone = zipfile.ZipInfo(filename=info.filename, date_time=info.date_time)
            clone.compress_type = zipfile.ZIP_DEFLATED
            clone.external_attr = info.external_attr
            clone.create_system = info.create_system
            clone.flag_bits = info.flag_bits
            dst.writestr(clone, payload[info.filename])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Upgrade verified Gen1Online sandbox.1 to sandbox.2")
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    output = args.output or default_output(args.source_zip)
    try:
        upgrade_zip(args.source_zip, output)
    except (OSError, UnicodeDecodeError, ValueError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Patched Gen1Online sandbox.2: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
