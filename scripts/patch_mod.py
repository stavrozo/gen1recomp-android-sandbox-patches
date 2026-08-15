#!/usr/bin/env python3
"""Apply known Gen1Recomp Android compatibility patches to original mod ZIPs.

The patcher identifies a supported source archive by SHA-256, applies a small
unified diff in memory, removes explicitly prohibited packaging paths, and
writes a new ZIP. The original archive is never modified.
"""
from __future__ import annotations

import argparse
import hashlib
import gzip
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META_PATH = ROOT / "patches" / "metadata.json"
HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
ROM_EXTENSIONS = {".gb", ".gbc", ".gba", ".rom"}


class PatchError(RuntimeError):
    pass


@dataclass
class FilePatch:
    old_path: str
    new_path: str
    hunks: list[list[str]]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def clean_diff_path(value: str) -> str:
    value = value.strip().split("\t", 1)[0]
    if value == "/dev/null":
        return value
    if value.startswith("a/") or value.startswith("b/"):
        value = value[2:]
    return value


def is_file_header(line: str) -> bool:
    return line.startswith("--- a/") or line == "--- /dev/null"


def parse_unified_diff(text: str) -> list[FilePatch]:
    lines = text.splitlines()
    patches: list[FilePatch] = []
    i = 0
    while i < len(lines):
        if not is_file_header(lines[i]):
            i += 1
            continue
        old_path = clean_diff_path(lines[i][4:])
        i += 1
        if i >= len(lines) or not lines[i].startswith("+++ "):
            raise PatchError("Malformed patch: missing +++ header")
        new_path = clean_diff_path(lines[i][4:])
        i += 1
        hunks: list[list[str]] = []
        while i < len(lines) and not is_file_header(lines[i]):
            if lines[i].startswith("@@ "):
                hunk = [lines[i]]
                i += 1
                while i < len(lines) and not lines[i].startswith("@@ ") and not is_file_header(lines[i]):
                    if lines[i] == r"\ No newline at end of file":
                        i += 1
                        continue
                    hunk.append(lines[i])
                    i += 1
                hunks.append(hunk)
            else:
                i += 1
        patches.append(FilePatch(old_path=old_path, new_path=new_path, hunks=hunks))
    return patches


def apply_file_patch(original: bytes | None, fp: FilePatch, trailing_newline: bool) -> bytes:
    if fp.old_path == "/dev/null":
        source: list[str] = []
    else:
        if original is None:
            raise PatchError(f"Required source file is missing: {fp.old_path}")
        try:
            source = original.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").splitlines()
        except UnicodeDecodeError as exc:
            raise PatchError(f"Patch target is not UTF-8 text: {fp.old_path}") from exc

    output: list[str] = []
    src_index = 0
    for hunk in fp.hunks:
        match = HUNK_RE.match(hunk[0])
        if not match:
            raise PatchError(f"Malformed hunk header: {hunk[0]}")
        old_start = int(match.group(1))
        target_index = max(old_start - 1, 0)
        if target_index < src_index:
            raise PatchError(f"Overlapping hunks in {fp.new_path}")
        output.extend(source[src_index:target_index])
        src_index = target_index

        for line in hunk[1:]:
            if not line:
                raise PatchError(f"Malformed empty diff line in {fp.new_path}")
            kind, body = line[0], line[1:]
            if kind == " ":
                if src_index >= len(source) or source[src_index] != body:
                    raise PatchError(f"Patch context mismatch in {fp.old_path} at source line {src_index + 1}")
                output.append(body)
                src_index += 1
            elif kind == "-":
                if src_index >= len(source) or source[src_index] != body:
                    raise PatchError(f"Patch removal mismatch in {fp.old_path} at source line {src_index + 1}")
                src_index += 1
            elif kind == "+":
                output.append(body)
            else:
                raise PatchError(f"Unsupported diff line prefix {kind!r} in {fp.new_path}")

    output.extend(source[src_index:])
    rendered = "\n".join(output)
    if trailing_newline:
        rendered += "\n"
    return rendered.encode("utf-8")


def is_prohibited_path(name: str) -> bool:
    p = Path(name)
    lower_parts = {part.lower() for part in p.parts}
    if "baseroms" in lower_parts:
        return True
    return p.suffix.lower() in ROM_EXTENSIONS


def load_metadata() -> dict:
    return json.loads(META_PATH.read_text(encoding="utf-8"))


def load_patch_text(path: Path) -> str:
    data = path.read_bytes()
    if path.suffix.lower() == ".gz":
        data = gzip.decompress(data)
    return data.decode("utf-8")


def find_target(source_zip: Path, metadata: dict) -> tuple[str, dict]:
    digest = sha256_file(source_zip)
    for slug, entry in metadata.items():
        if entry["source_sha256"].lower() == digest.lower():
            return slug, entry
    raise PatchError(
        "Unsupported source ZIP. This patcher only accepts the exact original versions listed in the repository README."
    )


def patch_zip(source_zip: Path, output_zip: Path) -> tuple[str, list[str]]:
    metadata = load_metadata()
    slug, entry = find_target(source_zip, metadata)
    patch_text = load_patch_text(ROOT / entry["patch_file"])
    file_patches = parse_unified_diff(patch_text)
    trailing = {item["path"]: item["trailing_newline"] for item in entry["changed_files"]}
    expected_hashes = {item["path"]: item["sha256"] for item in entry["changed_files"]}
    remove_paths = set(entry.get("remove_paths", []))
    remove_prefixes = tuple(entry.get("remove_prefixes", []))

    with zipfile.ZipFile(source_zip, "r") as src:
        infos = src.infolist()
        payload = {info.filename: src.read(info.filename) for info in infos if not info.is_dir()}

    for fp in file_patches:
        target_path = fp.new_path
        original = None if fp.old_path == "/dev/null" else payload.get(fp.old_path)
        payload[target_path] = apply_file_patch(original, fp, trailing_newline=trailing[target_path])
        if fp.old_path != "/dev/null" and fp.old_path != target_path:
            payload.pop(fp.old_path, None)

    for path in remove_paths:
        payload.pop(path, None)
    for path in list(payload):
        if any(path.startswith(prefix) for prefix in remove_prefixes):
            payload.pop(path, None)

    for path, expected in expected_hashes.items():
        actual = sha256_bytes(payload.get(path, b""))
        if actual != expected:
            raise PatchError(f"Verification failed for patched file {path}")

    prohibited = sorted(name for name in payload if is_prohibited_path(name))
    if prohibited:
        raise PatchError("Refusing to create output containing prohibited ROM/baserom path(s): " + ", ".join(prohibited))

    output_zip.parent.mkdir(parents=True, exist_ok=True)
    original_info = {info.filename: info for info in infos}
    ordered_names = [info.filename for info in infos if not info.is_dir() and info.filename in payload]
    added_names = [name for name in payload if name not in original_info]

    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as dst:
        for name in ordered_names + sorted(added_names):
            data = payload[name]
            info = original_info.get(name)
            if info is not None:
                clone = zipfile.ZipInfo(filename=name, date_time=info.date_time)
                clone.compress_type = zipfile.ZIP_DEFLATED
                clone.external_attr = info.external_attr
                clone.create_system = info.create_system
                clone.flag_bits = info.flag_bits
                dst.writestr(clone, data)
            else:
                dst.writestr(name, data)

    return slug, sorted(payload)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Patch supported Gen1Recomp mods for newer Android sandbox behavior.")
    parser.add_argument("source_zip", type=Path, help="Exact original mod ZIP downloaded from the upstream author")
    parser.add_argument("--output", type=Path, help="Output ZIP path (defaults beside the source ZIP)")
    args = parser.parse_args(argv)

    try:
        metadata = load_metadata()
        slug, entry = find_target(args.source_zip, metadata)
        output = args.output or args.source_zip.with_name(entry["output_name"])
        patched_slug, _ = patch_zip(args.source_zip, output)
        print(f"Patched {patched_slug}: {output}")
        return 0
    except (OSError, zipfile.BadZipFile, PatchError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
