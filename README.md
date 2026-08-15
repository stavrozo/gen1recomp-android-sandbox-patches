# Gen1Recomp Android Sandbox Patches

Unofficial compatibility fixes for Gen1Recomp mods affected by newer Android sandbox/runtime API restrictions.

> [!IMPORTANT]
> This project is **not affiliated with Gen1Recomp or the original mod authors**. It does not distribute ROMs, baseroms, Pokémon game files, or other copyrighted game data.

## Why this exists

Recent Gen1Recomp Android builds restrict direct mod access to APIs such as `love.filesystem` and `love.thread`. Several existing mods were written for the older runtime and began failing after the update.

This repository documents the fixes we reproduced and tested, and provides a safe path for applying them without unnecessarily redistributing original mod packages or third-party artwork.

## Current compatibility work

| Mod | Original version | Fix status | Distribution plan |
|---|---:|---|---|
| Crystal Animated Sprites with Shiny Visuals | 1.6 | ✅ Android verified | Patch/local patcher only |
| Wilds of Kanto | 2.1.0 | ✅ Android verified | Patch/local patcher only |
| Shiny Pokémon | 1.0.1 | ✅ Android verified | Ready-to-install build allowed under MIT + patch source |
| Gen1Online / Game Corner Edition | 0.3.4.3 | ⚠️ Compatibility patch prepared; online behavior still needs runtime verification | Patch/local patcher only |
| Dramaless Shape | 2.0.1 | ✅ Android verified | Patch/local patcher only |

## Fixes covered

### Crystal Animated Sprites
- Replaces blocked direct filesystem access with mod-safe reads.
- Reworks unsupported file/directory checks.
- Preserves animated Pokémon sprites and shiny visuals.

### Wilds of Kanto
- Removes blocked direct filesystem usage from affected runtime paths.
- Preserves packaged-asset fallbacks.
- Fixes the fallback path that could incorrectly treat full-color sprites as Game Boy luminance sheets.

### Shiny Pokémon
- Removes blocked filesystem usage.
- Keeps shiny DV generation, palettes, battle sparkle behavior, Wilds integration, and follower rendering.
- Uses in-memory caching where the original implementation attempted runtime filesystem cache writes.

### Gen1Online / Game Corner
- Removes direct `love.thread` usage from the compatibility build.
- Reworks blocked filesystem-dependent behavior.
- Considered **experimental** until live online behavior is tested end-to-end on Android.

### Dramaless Shape
- Fixes the render-distance bug that compared NPC/follower world-pixel coordinates against player grid-cell coordinates.
- Keeps Voxel mode enabled rather than bypassing occlusion globally.
- Removes the `baseroms/` placeholder directory from generated Android-compatible packages because current import validation rejects that path.

## Distribution and licensing

This repo uses a conservative hybrid model:

- **Shiny Pokémon:** upstream is MIT licensed, so a complete compatibility build may be distributed while preserving the upstream license and attribution.
- **Crystal Animated Sprites:** no clear upstream license was found, so this repo will not redistribute the full original package.
- **Wilds of Kanto:** code is MIT licensed, but the package includes separately licensed third-party assets, so this repo will publish patch logic instead of a full repack.
- **Gen1Online / Game Corner:** licensing of the complete project/package is unclear, so this repo will publish patch logic only.
- **Dramaless Shape:** mixed/inherited licensing makes patch-only distribution the safer approach.

Users should download the exact supported original mod version from its original author/source, then apply the local compatibility patch.

## Safety rules

- No ROMs or baseroms.
- No extracted Pokémon game assets.
- No save-file modification is required.
- Patch tools will operate on a copy of the original mod ZIP and leave the user's source download untouched.
- Unknown mod versions will be rejected rather than patched blindly.
- Static checks are not treated as proof of Android runtime compatibility; device testing is documented separately.

## Project status

🚧 **Work in progress.** Patch files, patcher scripts, tests, attribution notes, and release packaging are being added next.

## Credits

All original mods remain the work of their respective authors. This project only contains compatibility work needed to make supported versions function with newer Gen1Recomp Android sandbox behavior.

If an upstream author ships an official fix, that official version should be preferred over these compatibility patches.
