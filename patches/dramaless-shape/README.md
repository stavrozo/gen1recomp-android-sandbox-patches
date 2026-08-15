# Dramaless Shape v2.0.1

**Status:** ✅ Verified on Android with Voxel mode enabled.

This patch targets the exact original `DRAMALESS_SHAPE-2.0.1.zip` used during testing.

## Fix

The visible bug was very specific: followers, wild Pokémon, and some trainers rendered normally, then disappeared after crossing certain map coordinates while their shadows remained.

The render-distance check compared NPC/follower `px`/`py` **world-pixel coordinates** against player `cellX`/`cellY` **grid-cell coordinates**. The patch compares in the same pixel space, using the player's pixel position with a 16-pixel cell fallback.

It also removes the upstream `baseroms/` placeholder directory from the generated ZIP because the current Android importer rejects packages containing that path even when it contains only a text placeholder.

## Apply

```bash
python scripts/patch_mod.py DRAMALESS_SHAPE-2.0.1.zip
```

Generated output:

```text
DRAMALESS_SHAPE-2.0.1-sandbox.2-android-import-fix.zip
```

The original ZIP is left untouched.

## Distribution note

Because Dramaless contains inherited/attributed components with mixed licensing history, this repository publishes the compatibility diff and patcher rather than repacking the complete upstream mod.
