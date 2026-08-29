# Gen1Recomp Android Sandbox Patches

Unofficial compatibility fixes and proper sandbox migrations for Gen1Recomp mods affected by newer mod sandbox/runtime changes.

> [!IMPORTANT]
> This project is **not affiliated with Gen1Recomp or the original mod authors**. It contains no Pokémon ROMs, baseroms, save files, or extracted game data.

## Current upstream status

Gen1Recomp **0.1.91** added a temporary legacy compatibility layer for many pre-sandbox APIs. Older mods using calls such as `love.filesystem`, `io.open`, `dofile`, `loadfile`, `love.system`, and `love.event` may therefore start loading again without these patches.

That compatibility layer is intentionally a migration bridge rather than the long-term API. It reroutes old calls through safer per-mod behavior and reports which calls should be migrated.

Upstream releases now supersede parts of this repository:

- **Wilds of Kanto 2.1.5:** officially migrated to the current Gen1Recomp sandbox APIs and also fixes Wilds/followers/town Pokémon disappearing after battles. **Use upstream 2.1.5; our Wilds patch is archived for older 2.1.0 installs.**
- **Dramaless Shape 2.0.3:** fixes the older importer/package problem and the render-distance world-pixel/grid-cell mismatch. **Use upstream 2.0.3 for those issues.** Our current Dramaless work now focuses on WIDE/FILL native-card alignment, Splash presentation, and an optional Android portrait HUD compatibility layer.

Other important notes:

- `love.thread` is **still not available to mods**, so the Gen1Online/Game Corner compatibility rewrite remains relevant for the exact older build tested here.
- Crystal Animated Sprites has an additional small Dramaless Shape 2.x compatibility diff for voxel battles.
- If an original mod author releases an official updated version, prefer the upstream release.

## The fixes are here

| Mod | Original tested | Current status | Fix |
|---|---:|---|---|
| [Crystal Animated Sprites](patches/crystal-animated-sprites/) | 1.6 / v1.6.1 patched | Sandbox migration verified; Dramaless 2.x compatibility diff also verified | [sandbox patch](patches/crystal-animated-sprites/android-sandbox.patch) · [Dramaless 2.x patch](patches/crystal-animated-sprites/dramaless-2x-compat-v1.6.1.patch) |
| [Wilds of Kanto](patches/wilds-of-kanto/) | 2.1.0 | **Archived:** superseded by official Wilds 2.1.5 | [historical exact patch](patches/wilds-of-kanto/android-sandbox.patch.gz) |
| [Shiny Pokémon](patches/shiny-pokemon/) | 1.0.1 | Legacy compat may allow the original to load; patch removes the old filesystem dependency | [exact compressed patch](patches/shiny-pokemon/android-sandbox.patch.gz) |
| [Gen1Online / Game Corner](patches/gen1online-gamecorner/) | 0.3.4.3 | `love.thread` rewrite still relevant for this tested build; live online behavior experimental | [exact compressed patch](patches/gen1online-gamecorner/android-sandbox.patch.gz) |
| [Dramaless Shape](patches/dramaless-shape/) | 2.0.1 / 2.0.3 | Old 2.0.1 import/render-distance patch is historical; current 2.0.3 battle patches are verified on Android | [WIDE/FILL + Splash](patches/dramaless-shape/2.0.3-wide-fill-splash.patch) · [portrait HUD](patches/dramaless-shape/2.0.3-portrait-wide-hud.patch) |

The larger/exact diffs may be stored as `.patch.gz` to keep the repository compact. The patcher reads them directly; users do not need to decompress them.

## Easiest way to use the legacy sandbox fixes

You need **Python 3.10+**. Download/clone this repository, then run:

```bash
python scripts/patch_mod.py /path/to/original-mod.zip
```

You do **not** need to choose the mod manually. The patcher checks the SHA-256 of the original ZIP, identifies the exact supported version, applies the matching compatibility patch, verifies the changed files, rejects prohibited ROM/baserom paths, and creates a new ZIP beside the original.

Example for the legacy Dramaless 2.0.1 package:

```bash
python scripts/patch_mod.py DRAMALESS_SHAPE-2.0.1.zip
```

Output:

```text
DRAMALESS_SHAPE-2.0.1-sandbox.2-android-import-fix.zip
```

Your original ZIP is never modified.

> [!NOTE]
> Do **not** apply the historical 2.0.1 Dramaless patch to 2.0.3. Upstream 2.0.3 already supersedes its packaging and render-distance fixes. The newer battle patches are documented separately under [`patches/dramaless-shape/`](patches/dramaless-shape/).

## What was fixed

### Crystal Animated Sprites with Shiny Visuals

When the stricter sandbox first landed, raw `love.filesystem` access used by the mod stopped working. Gen1Recomp 0.1.91 now provides a temporary legacy stand-in for those calls, but our sandbox patch migrates the affected reads/checks to sandbox-safe mod access and keeps the animated/shiny sprite behavior working without relying on that compatibility bridge.

The additional `dramaless-2x-compat-v1.6.1.patch` recognizes Dramaless Shape 2.x's standalone/hosted voxel battle lifecycle and rebuilds Crystal battle frames once the voxel provider is actually live. This exact change was verified in-game with Dramaless 2.0.3.

### Wilds of Kanto v2.1.0 — archived

This historical patch migrated affected filesystem paths, preserved packaged-asset fallbacks, and included the follow-up `trueColor` rendering correction discovered during testing.

**Upstream Wilds of Kanto 2.1.5 now replaces this patch.** The official release migrates to supported mod asset APIs and fixes Wilds/followers/town Pokémon disappearing after battles. New installs should use the upstream release instead of patching 2.1.0.

### Shiny Pokémon v1.0.1

This patch removes the old filesystem dependency while retaining shiny DV generation, Gen 2-style palettes, battle sparkles, Wilds integration, and follower rendering. Runtime recolor caching is kept in memory rather than written through the old filesystem path.

### Gen1Online / Game Corner Edition v0.3.4.3

This compatibility patch removes direct `love.thread` and blocked filesystem dependencies from the build we tested. `love.thread` remains explicitly unsupported in Gen1Recomp 0.1.91, so this is not covered by the legacy compatibility layer.

The mod loads under the newer sandbox, but the live online/network behavior should still be treated as **experimental** until independently exercised end-to-end.

### Dramaless Shape

The historical 2.0.1 patch fixed the Voxel-mode render-distance bug where followers, wild Pokémon, and trainers could disappear while only their shadows remained, and removed the rejected `baseroms/` placeholder from the generated package. Both problems are now superseded by upstream **Dramaless Shape 2.0.3**.

The current `2.0.3-wide-fill-splash.patch` instead fixes native 2D card presentation in Gen1Recomp WIDE battles: WIDE-specific solved camera anchors, fractional FILL presentation scaling, camera locking while fixed screen-space move/Poké Ball FX target the cards, and Splash's bounce as a world-space hop rather than a clipped card capture.

The separate `2.0.3-portrait-wide-hud.patch` relocates the enemy WIDE/FILL status panel above the battle surface on tall Android portrait displays and keeps it stationary through attack shake/flash frames. It remains an optional compatibility layer rather than part of the intended Dramaless upstream PR because Dramaless 2.0 deliberately does not own the HUD.

## Why full mod ZIPs are not hosted here

We researched the upstream licensing before publishing anything:

- **Shiny Pokémon:** upstream MIT license permits redistribution with attribution. The exact compatibility patch is published here; a prebuilt package can also be released later while preserving the upstream license.
- **Crystal Animated Sprites:** no clear upstream license was found, so only compatibility diffs/tooling are published here.
- **Wilds of Kanto:** source code is MIT, but its package includes separately attributed/licensed third-party artwork, so the complete mod is not repacked here.
- **Gen1Online / Game Corner:** licensing of the complete current package is unclear, so only the patch is published.
- **Dramaless Shape:** this repository keeps patch-only distribution rather than repacking the complete upstream mod.

See [NOTICE.md](NOTICE.md) for attribution and scope details.

## Safety

- No ROMs or baseroms are distributed.
- No save-file modification is required.
- The legacy patcher refuses unknown ZIP hashes instead of guessing.
- Keep your original mod downloads as backups.
- If an upstream author releases an official compatibility fix, prefer the official release.

## Tested combination

The sandbox fixes were developed against a Gen1Recomp Android setup where Crystal Animated Sprites, Wilds of Kanto, Shiny Pokémon, and Dramaless Shape were tested in-game after the sandbox/runtime change. Gen1Online's sandbox/load issue was fixed, but its live network path remains marked experimental.

The newer battle compatibility work was verified on a **685x1536 Android portrait display** using Dramaless Shape 2.0.3, WIDE + FILL battles, Crystal animated sprites, idle animation, attacks/incoming attacks, Poké Ball targeting, Splash, and the stable enemy HUD placement. CLASSIC layout regression checks were also included.

## License

Original compatibility tooling/documentation in this repository is MIT licensed. Upstream mods, upstream patch context, third-party assets, and Pokémon intellectual property keep their own rights/licenses. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
