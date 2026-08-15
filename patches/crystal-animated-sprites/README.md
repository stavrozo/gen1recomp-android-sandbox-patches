# Crystal Animated Sprites with Shiny Visuals v1.6

**Status:** ✅ Verified on Android after the Gen1Recomp sandbox/runtime update.

This patch targets the exact original `crystal_animated_sprites_with_shiny_visuals_v1.6.zip` used during testing.

## Fix

- Replaces blocked raw `love.filesystem` reads/checks with sandbox-safe mod-owned reads.
- Reworks player-sprite discovery without unrestricted directory enumeration.
- Keeps animated battle sprites and shiny visuals working.

## Apply

From the repository root:

```bash
python scripts/patch_mod.py crystal_animated_sprites_with_shiny_visuals_v1.6.zip
```

Generated output:

```text
crystal_animated_sprites_with_shiny_visuals_v1.6.1_android_sandbox_patch.zip
```

The patcher validates the exact source ZIP before applying the patch. The original ZIP is not modified.

## Distribution note

The full upstream mod is not redistributed here because no clear upstream license was found when this compatibility patch was prepared. Obtain the original mod from its author/source, then patch it locally.
