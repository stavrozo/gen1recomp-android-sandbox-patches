# Gen1Recomp Android Sandbox Patches

Unofficial compatibility fixes and proper sandbox migrations for Gen1Recomp mods affected by the newer mod sandbox/runtime changes.

> [!IMPORTANT]
> This project is **not affiliated with Gen1Recomp or the original mod authors**. It contains no Pokémon ROMs, baseroms, save files, or extracted game data.

## Gen1Recomp 0.1.91 update

Gen1Recomp **0.1.91** added a temporary legacy compatibility layer for many pre-sandbox APIs. Older mods using calls such as `love.filesystem`, `io.open`, `dofile`, `loadfile`, `love.system`, and `love.event` may therefore start loading again without these patches.

That compatibility layer is intentionally a migration bridge rather than the long-term API. It reroutes old calls through safer per-mod behavior and reports which calls should be migrated.

These patches are still useful because they move supported mods toward the current mod APIs instead of depending on that temporary bridge. Also:

- `love.thread` is **still not available to mods**, so Gen1Online/Game Corner still needs its compatibility rewrite.
- The Dramaless Shape Voxel render-distance fix is a separate gameplay/rendering bug and is unrelated to the legacy compatibility layer.
- The Dramaless `baseroms/` packaging cleanup is separate from the filesystem compatibility shim.

If an original mod author releases an official updated version, prefer the upstream release.

## The fixes are here

| Mod | Original | Status on 0.1.91 | Fix |
|---|---:|---|---|
| [Crystal Animated Sprites](patches/crystal-animated-sprites/) | 1.6 | Legacy compat may allow the original to load; patch performs the proper migration | [patch](patches/crystal-animated-sprites/android-sandbox.patch) |
| [Wilds of Kanto](patches/wilds-of-kanto/) | 2.1.0 | Legacy compat helps old filesystem calls; patch also contains our rendering fallback correction | [exact compressed patch](patches/wilds-of-kanto/android-sandbox.patch.gz) |
| [Shiny Pokémon](patches/shiny-pokemon/) | 1.0.1 | Legacy compat may allow the original to load; patch removes the old filesystem dependency | [exact compressed patch](patches/shiny-pokemon/android-sandbox.patch.gz) |
| [Gen1Online / Game Corner](patches/gen1online-gamecorner/) | 0.3.4.3 | **Still relevant:** `love.thread` remains unsupported; live online behavior experimental | [exact compressed patch](patches/gen1online-gamecorner/android-sandbox.patch.gz) |
| [Dramaless Shape](patches/dramaless-shape/) | 2.0.1 | **Still relevant:** independent Voxel render-distance bug + packaging cleanup | [patch](patches/dramaless-shape/android-sandbox.patch) |

The larger/exact diffs may be stored as `.patch.gz` to keep the repository compact. The patcher reads them directly; users do not need to decompress them.

## Easiest way to use the fixes

You need **Python 3.10+**. Download/clone this repository, then run:

```bash
python scripts/patch_mod.py /path/to/original-mod.zip
```

You do **not** need to choose the mod manually. The patcher checks the SHA-256 of the original ZIP, identifies the exact supported version, applies the matching compatibility patch, verifies the changed files, rejects prohibited ROM/baserom paths, and creates a new ZIP beside the original.

Example:

```bash
python scripts/patch_mod.py DRAMALESS_SHAPE-2.0.1.zip
```

Output:

```text
DRAMALESS_SHAPE-2.0.1-sandbox.2-android-import-fix.zip
```

Your original ZIP is never modified.

## What was fixed

### Crystal Animated Sprites with Shiny Visuals v1.6

When the stricter sandbox first landed, raw `love.filesystem` access used by the mod stopped working. Gen1Recomp 0.1.91 now provides a temporary legacy stand-in for those calls, but this patch migrates the affected reads/checks to sandbox-safe mod access and keeps the animated/shiny sprite behavior working without relying on that compatibility bridge.

### Wilds of Kanto v2.1.0

This patch migrates affected filesystem paths and preserves packaged-asset fallbacks. It also includes the follow-up rendering correction discovered during testing: when runtime luminance generation is unavailable, full-color Pokémon sprites stay `trueColor` instead of being misinterpreted as Game Boy shade sheets.

### Shiny Pokémon v1.0.1

This patch removes the old filesystem dependency while retaining shiny DV generation, Gen 2-style palettes, battle sparkles, Wilds integration, and follower rendering. Runtime recolor caching is kept in memory rather than written through the old filesystem path.

### Gen1Online / Game Corner Edition v0.3.4.3

This compatibility patch removes direct `love.thread` and blocked filesystem dependencies from the build we tested. `love.thread` remains explicitly unsupported in Gen1Recomp 0.1.91, so this is not covered by the new legacy compatibility layer.

The mod loads under the newer sandbox, but the live online/network behavior should still be treated as **experimental** until independently exercised end-to-end.

### Dramaless Shape v2.0.1

This fixes the Voxel-mode bug where followers, wild Pokémon, and trainers could render normally and then suddenly disappear while only their shadow remained.

The root cause was a unit mismatch in render-distance culling: NPC/follower positions were in **world pixels**, while the player was compared using **grid cells**. The patch uses the player's pixel coordinates (with a 16-pixel cell fallback).

It also removes the `baseroms/` placeholder folder from the generated compatibility package because the stricter importer rejects packages containing that path. This issue is separate from the 0.1.91 legacy API compatibility layer.

## Why full mod ZIPs are not hosted here

We researched the upstream licensing before publishing anything:

- **Shiny Pokémon:** upstream MIT license permits redistribution with attribution. The exact compatibility patch is published here; a prebuilt package can also be released later while preserving the upstream license.
- **Crystal Animated Sprites:** no clear upstream license was found, so only the compatibility diff/tooling is published here.
- **Wilds of Kanto:** source code is MIT, but its package includes separately attributed/licensed third-party artwork, so the complete mod is not repacked here.
- **Gen1Online / Game Corner:** licensing of the complete current package is unclear, so only the patch is published.
- **Dramaless Shape:** inherited/mixed licensing makes patch-only distribution the conservative choice.

See [NOTICE.md](NOTICE.md) for attribution and scope details.

## Safety

- No ROMs or baseroms are distributed.
- No save-file modification is required.
- The patcher refuses unknown ZIP hashes instead of guessing.
- Keep your original mod downloads as backups.
- If an upstream author releases an official compatibility fix, prefer the official release.

## Tested combination

The fixes were developed against a Gen1Recomp Android setup where Crystal Animated Sprites, Wilds of Kanto, Shiny Pokémon, and Dramaless Shape were tested in-game after the sandbox/runtime change. Gen1Online's sandbox/load issue was fixed, but its live network path remains marked experimental.

Gen1Recomp 0.1.91's legacy compatibility layer may make some unpatched pre-sandbox mods load again. That should not be treated as proof that every old mod is fully migrated or that mod-specific bugs have been resolved.

## License

Original compatibility tooling/documentation in this repository is MIT licensed. Upstream mods, upstream patch context, third-party assets, and Pokémon intellectual property keep their own rights/licenses. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
