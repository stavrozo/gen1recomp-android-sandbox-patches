# Shiny Pokémon v1.0.1

**Status:** ✅ Verified on Android with Wilds of Kanto and the other repaired visual mods.

This patch targets the exact original `SHINY_POKEMON-1.0.1.zip` used during testing.

## Fix

- Removes blocked direct filesystem access.
- Keeps shiny DV generation, Gen 2-style shiny palettes, battle sparkles, overworld shiny rendering, and follower integration.
- Uses in-memory recolor caching instead of raw filesystem cache writes.
- Sends diagnostics through the mod logger instead of writing a debug file directly.

## Apply

```bash
python scripts/patch_mod.py SHINY_POKEMON-1.0.1.zip
```

Generated output:

```text
SHINY_POKEMON-1.0.1-sandbox.1-android-patch.zip
```

`android-sandbox.patch.gz` contains the exact compatibility diff used by the patcher.

## License note

The upstream Shiny Pokémon project is MIT licensed. This repository currently publishes the exact patch/tooling; a prebuilt compatibility ZIP may also be distributed later with the upstream MIT notice preserved.
