# Dramaless Shape render-distance fix

**Status:** ✅ Our 2.0.1 patch was verified on Android with Voxel mode enabled. Upstream **2.0.2 fixes packaging, but not the render-distance bug**.

The patch currently stored here targets the exact original `DRAMALESS_SHAPE-2.0.1.zip` used during testing.

## Current upstream 2.0.2 status

Dramaless Shape **2.0.2** officially fixes the Gen1Recomp importer/package problem by removing the old `baseroms/` directory and placing the mod files directly at the ZIP root.

However, the separate Voxel culling bug is still present in the 2.0.2 source: NPC/follower positions use `px`/`py` world-pixel coordinates while the player side of the distance calculation still uses `cellX`/`cellY` grid-cell coordinates. The upstream issue for invisible NPCs with visible shadows remains open.

Until upstream fixes that calculation, setting **RENDER DISTANCE = FULL** avoids the faulty distance culling. Do not apply this 2.0.1 patch directly to a 2.0.2 ZIP.

## What the 2.0.1 patch fixes

The visible bug was very specific: followers, wild Pokémon, and some trainers rendered normally, then disappeared after crossing certain map coordinates while their shadows remained.

The render-distance check compared NPC/follower `px`/`py` **world-pixel coordinates** against player `cellX`/`cellY` **grid-cell coordinates**. The patch compares in the same pixel space, using the player's pixel position with a 16-pixel cell fallback.

For the old 2.0.1 package, it also removes the upstream `baseroms/` placeholder directory because the newer importer rejects that package layout. That packaging workaround is no longer needed in upstream 2.0.2.

## Apply to the legacy 2.0.1 release

```bash
python scripts/patch_mod.py DRAMALESS_SHAPE-2.0.1.zip
```

Generated output:

```text
DRAMALESS_SHAPE-2.0.1-sandbox.2-android-import-fix.zip
```

The original ZIP is left untouched.

## Distribution note

This repository publishes the compatibility diff and patcher rather than repacking the complete upstream mod.
