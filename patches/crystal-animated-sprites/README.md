# Crystal Animated Sprites with Shiny Visuals compatibility patches

**Status:** ✅ Verified on Android with the newer Gen1Recomp sandbox and with Dramaless Shape 2.0.3 voxel battles.

## Android sandbox patch

`android-sandbox.patch` targets the original Crystal Animated Sprites v1.6 package used during testing. It:

- replaces blocked raw `love.filesystem` reads/checks with sandbox-safe mod-owned reads;
- reworks player-sprite discovery without unrestricted directory enumeration;
- keeps animated battle sprites and shiny visuals working.

Apply it with the repository patcher:

```bash
python scripts/patch_mod.py crystal_animated_sprites_with_shiny_visuals_v1.6.zip
```

The generated build is the v1.6.1 Android sandbox patch used as the base for the compatibility fix below.

## Dramaless Shape 2.x compatibility

`dramaless-2x-compat-v1.6.1.patch` is an exact `main.lua` diff from the v1.6.1 Android-sandbox build to the combination verified in-game with Dramaless 2.0.3.

It:

- recognizes the `DRAMALESS_SHAPE` mod ID;
- detects Dramaless 2.x's active standalone voxel battle session;
- detects the same Dramaless arena provider when StadiumBattleFX is hosting it;
- rebuilds Crystal's battle frames once the voxel provider becomes live, so Crystal's existing voxel-specific frame preparation runs at the correct time.

The change is intentionally small and does not modify Crystal's normal 2D animation path.

The upstream Crystal repository currently publishes packaged ZIP releases rather than unpacked `main.lua` source, so this repository keeps the reviewable source diff. An upstream issue can point the author to this patch for inclusion in a future packaged release.

## Verified combination

The Dramaless compatibility patch was tested with animated Pokémon idling and attacking in WIDE/FILL voxel battles. The same Crystal build remained stable in ordinary 2D battles.

## Distribution note

The full upstream Crystal mod is not redistributed here because no clear upstream license was found when this compatibility work was prepared. Obtain the original mod from its author/source, then patch it locally.
