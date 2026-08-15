# Gen1Recomp Android Sandbox Patches

Unofficial compatibility fixes for Gen1Recomp mods affected by newer Android sandbox/runtime restrictions.

> [!IMPORTANT]
> This project is **not affiliated with Gen1Recomp or the original mod authors**. It contains no Pokémon ROMs, baseroms, save files, or extracted game data.

## The fixes are here

| Mod | Original | Android status | Fix |
|---|---:|---|---|
| [Crystal Animated Sprites](patches/crystal-animated-sprites/) | 1.6 | ✅ Verified | [patch](patches/crystal-animated-sprites/android-sandbox.patch) |
| [Wilds of Kanto](patches/wilds-of-kanto/) | 2.1.0 | ✅ Verified | [patch](patches/wilds-of-kanto/android-sandbox.patch) |
| [Shiny Pokémon](patches/shiny-pokemon/) | 1.0.1 | ✅ Verified | [patch](patches/shiny-pokemon/android-sandbox.patch) + ready build |
| [Gen1Online / Game Corner](patches/gen1online-gamecorner/) | 0.3.4.3 | ⚠️ Sandbox load fixed; live online behavior experimental | [patch](patches/gen1online-gamecorner/android-sandbox.patch) |
| [Dramaless Shape](patches/dramaless-shape/) | 2.0.1 | ✅ Verified | [patch](patches/dramaless-shape/android-sandbox.patch) |

## Easiest way to use the patch-only fixes

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

The newer runtime blocks raw `love.filesystem` access from mods. This patch moves the affected reads/checks to sandbox-safe mod access and keeps the animated/shiny sprite behavior working.

### Wilds of Kanto v2.1.0

This patch replaces blocked filesystem paths and preserves packaged-asset fallbacks. It also includes the follow-up rendering correction discovered during testing: when runtime luminance generation is unavailable, full-color Pokémon sprites stay `trueColor` instead of being misinterpreted as Game Boy shade sheets.

### Shiny Pokémon v1.0.1

This patch removes blocked filesystem use while retaining shiny DV generation, Gen 2-style palettes, battle sparkles, Wilds integration, and follower rendering. Runtime recolor caching is kept in memory rather than written through the blocked filesystem API.

### Gen1Online / Game Corner Edition v0.3.4.3

This compatibility patch removes direct `love.thread` and blocked filesystem dependencies from the build we tested. The mod loads under the newer sandbox, but the live online/network behavior should still be treated as **experimental** until independently exercised end-to-end.

### Dramaless Shape v2.0.1

This fixes the Voxel-mode bug where followers, wild Pokémon, and trainers could render normally and then suddenly disappear while only their shadow remained.

The root cause was a unit mismatch in render-distance culling: NPC/follower positions were in **world pixels**, while the player was compared using **grid cells**. The patch uses the player's pixel coordinates (with a 16-pixel cell fallback). It also removes the `baseroms/` placeholder folder because the current Android importer rejects packages containing that path.

## Why most full mod ZIPs are not hosted here

We researched the upstream licensing before publishing anything:

- **Shiny Pokémon:** upstream MIT license permits redistribution with attribution, so a ready-to-install compatibility build can be provided.
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

The fixes were developed against a Gen1Recomp Android setup where Crystal Animated Sprites, Wilds of Kanto, Shiny Pokémon, and Dramaless Shape were tested in-game after the sandbox/runtime change. Gen1Online's sandbox error was fixed, but its live network path remains marked experimental.

## License

Original compatibility tooling/documentation in this repository is MIT licensed. Upstream mods, upstream patch context, third-party assets, and Pokémon intellectual property keep their own rights/licenses. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
