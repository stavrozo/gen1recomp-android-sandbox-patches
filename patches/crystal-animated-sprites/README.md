# Crystal Animated Sprites with Shiny Visuals

## Android sandbox patch (v1.6)

**Status:** ✅ Verified on Android after the Gen1Recomp sandbox/runtime update.

This patch targets the exact original `crystal_animated_sprites_with_shiny_visuals_v1.6.zip` used during testing.

### Fix

- Replaces blocked raw `love.filesystem` reads/checks with sandbox-safe mod-owned reads.
- Reworks player-sprite discovery without unrestricted directory enumeration.
- Keeps animated battle sprites and shiny visuals working.

### Apply

From the repository root:

```bash
python scripts/patch_mod.py crystal_animated_sprites_with_shiny_visuals_v1.6.zip
```

Generated output:

```text
crystal_animated_sprites_with_shiny_visuals_v1.6.1_android_sandbox_patch.zip
```

The patcher validates the exact source ZIP before applying the patch. The original ZIP is not modified.

## Dramaless Shape 2.x compatibility (v2.0.2)

**Status:** ✅ Verified in-game on Gen1Recomp Android with Dramaless Shape 2.0.3.

Reviewable source diff:

```text
dramaless-2x-compat-v2.0.2.patch
```

The v2.0.2 patch keeps the existing legacy voxel-provider fallback while adding detection for the current Dramaless 2.x runtime providers:

- `voxel2DBattleHost.session`
- `voxelArenaProvider.state`

It also rebuilds Crystal's player and enemy animation frames once when the Dramaless voxel session becomes active after Crystal's initial battle-frame setup.

Verified behavior includes stable animated player/enemy sprites, no half-sprite/clipping or idle-frame jumping, and compatibility with Dramaless WIDE/FILL battle rendering.

## Distribution note

The full upstream mod is not redistributed here because no clear upstream license was found when these compatibility patches were prepared. Obtain the original mod from its author/source, then apply the relevant source patch locally.
