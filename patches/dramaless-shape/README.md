# Dramaless Shape compatibility fixes

**Status:** ✅ The current Android battle fixes were verified in-game against Dramaless Shape 2.0.3. The older 2.0.1 sandbox/import patch remains here only for legacy installs.

## Current upstream 2.0.3 status

Upstream Dramaless Shape **2.0.3** now fixes the older render-distance unit mismatch as well as the 2.0.2 packaging/import issue. New installs should use upstream 2.0.3 rather than the historical 2.0.1 patch for those problems.

We re-checked current upstream `main` before preparing the battle patches below. The relevant battle files are still the same blobs as the 2.0.3 line, so these WIDE/FILL and Splash fixes are not already present upstream.

## Battle patches

### `2.0.3-wide-fill-splash.patch` — upstream-ready

This is the clean source patch intended for upstream review. It is based on the exact current upstream blobs for:

- `lib/BattleCam.lua` — `be07353424df945bc1df2ab4ee2b792967e70925`
- `lib/VoxelBattleArenaProvider.lua` — `6b9500744f7b81de95dceb360bd095dc34b6e310`
- `lib/VoxelBattleScene.lua` — `4b7fd0719a465e8be17881c4d95a7eff5179e297`
- `lib/VoxelBattleCardProvider.lua` — `02af78257d968da70ca51553851ab868f819e9e7`

It fixes three related native-card presentation problems:

1. **WIDE battle anchors** — Gen1Recomp's 304x144 WIDE layout translates the player/enemy battle slots. Dramaless now selects WIDE-specific solved camera rigs so the voxel cards remain aligned with native move and Poké Ball effects.
2. **WIDE + FILL scaling** — the voxel camera follows `Renderer:frameRects().Up` in WIDE mode so the fractional FILL presentation scale matches the native battle layer instead of using integer `fitScale()`.
3. **Splash bounce** — `SE_BOUNCE_UP_AND_DOWN` is removed from the off-screen card capture and promoted to a small world-space hop, preventing the captured card from clipping/wrapping through the floor.

The native-card camera is also held on the solved battle shot while fixed-screen Gen 1 move/Poké Ball effects are active, including when StadiumBattleFX hosts the Dramaless providers.

### `2.0.3-portrait-wide-hud.patch` — optional compatibility layer

This is the Android portrait HUD fix proven in the final test build. It relocates the enemy 128x32 WIDE/FILL status panel into the free space immediately above the centred battle surface and keeps it stable during attack shake/flash frames.

It is intentionally **not** part of the Dramaless upstream patch. Dramaless 2.0's provider boundary explicitly avoids owning HUD presentation, so this remains a compatibility patch while a cleaner Gen1Recomp-side/extended-HUD solution is considered.

Apply this only after the WIDE/FILL/Splash patch above.

## Verified Android combination

The final combination was exercised on a 685x1536 portrait Android display with:

- Dramaless Shape 2.0.3
- Gen1Recomp WIDE battle layout
- BATTLE SIZE = FILL
- Crystal Animated Sprites with the Dramaless 2.x compatibility fix
- idle animated Pokémon frames
- normal attacks and incoming attacks
- Poké Ball targeting
- Splash's repeated bounce
- enemy HUD placement during idle, attack shake, and flash frames
- CLASSIC layout regression checks

## Historical 2.0.1 patch

`android-sandbox.patch` targets the exact legacy `DRAMALESS_SHAPE-2.0.1.zip` used during the original Android sandbox/import work. It corrected the old render-distance world-pixel/grid-cell mismatch and removed the rejected `baseroms/` placeholder from the generated package.

Those two problems are superseded by upstream releases and the historical patch should **not** be applied to 2.0.3.

## Distribution note

This repository publishes compatibility diffs and tooling rather than repacking the complete upstream mod.
