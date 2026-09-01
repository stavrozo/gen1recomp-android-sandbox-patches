#!/usr/bin/env python3
"""Upgrade the verified Gen1Online v0.3.4.3 sandbox.1 package to sandbox.4.

sandbox.4 fixes the Rare Candy evolution soft-lock by deferring Gen1Online's
MMO level-up notification until Gen1Recomp has fully unwound EvolutionState.
The exact reviewed overlay lives in patches/gen1online-gamecorner/evolution-stack.patch.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

from patch_mod import apply_file_patch, parse_unified_diff

ROOT = Path(__file__).resolve().parents[1]
PATCH_PATH = ROOT / "patches" / "gen1online-gamecorner" / "evolution-stack.patch"
MAIN_PATH = "main.lua"
MANIFEST_PATH = "manifest.json"

SANDBOX1_MAIN_SHA256 = "0f3c34f8f742ec9577f6be66d8cf6d7ee81d3070fd45d47c52cab4287f16d05f"
SANDBOX1_MANIFEST_SHA256 = "89ad0fb7e91cc221b0b109b68831f39b5243257d7d9a1c2a309a0db4336070c8"
SANDBOX4_MAIN_SHA256 = "2e886850ec2fb0a7982b03ed080e7f035abdb752b46218d5adb095b6ca382f1c"
SANDBOX4_MANIFEST_SHA256 = "cd6161cf5eef62f0e9be9e93171c7909b42cdfca75c875e51bcc519d73311da5"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def default_output(source: Path) -> Path:
    name = source.name
    if "sandbox.1" in name:
        name = name.replace("sandbox.1", "sandbox.4", 1)
    else:
        name = source.stem + "-sandbox.4" + source.suffix
    return source.with_name(name)


def upgrade_zip(source: Path, output: Path, patch_path: Path = PATCH_PATH) -> None:
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

    file_patches = parse_unified_diff(patch_path.read_text(encoding="utf-8"))
    expected_targets = {MAIN_PATH, MANIFEST_PATH}
    targets = {fp.new_path for fp in file_patches}
    if targets != expected_targets:
        raise ValueError(f"unexpected evolution patch targets: {sorted(targets)}")

    trailing = {MAIN_PATH: False, MANIFEST_PATH: True}
    for fp in file_patches:
        original = payload.get(fp.old_path)
        if original is None:
            raise ValueError(f"missing patch target: {fp.old_path}")
        payload[fp.new_path] = apply_file_patch(
            original, fp, trailing_newline=trailing[fp.new_path]
        )

    if sha256(payload[MAIN_PATH]) != SANDBOX4_MAIN_SHA256:
        raise ValueError("verification failed for sandbox.4 main.lua")
    if sha256(payload[MANIFEST_PATH]) != SANDBOX4_MANIFEST_SHA256:
        raise ValueError("verification failed for sandbox.4 manifest.json")

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
    parser = argparse.ArgumentParser(
        description="Upgrade verified Gen1Online sandbox.1 to sandbox.4"
    )
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--patch", type=Path, default=PATCH_PATH)
    args = parser.parse_args(argv)
    output = args.output or default_output(args.source_zip)
    try:
        upgrade_zip(args.source_zip, output, args.patch)
    except (OSError, UnicodeDecodeError, ValueError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Patched Gen1Online sandbox.4: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
