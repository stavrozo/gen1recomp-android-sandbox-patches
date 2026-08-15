# Gen1Online / Game Corner Edition v0.3.4.3

**Status:** ⚠️ Android sandbox compatibility patch prepared. The original sandbox errors are addressed, but live multiplayer/network behavior remains experimental until exercised end-to-end.

This patch targets the exact `mod.zip` package identified as Gen1Online / Game Corner Edition v0.3.4.3 during testing.

## Fix

- Removes direct `love.thread` dependency from the compatibility build.
- Replaces raw filesystem-dependent asset/save paths with sandbox-compatible paths used by the tested build.
- Uses cooperative request queues in place of the old LÖVE worker-thread channels.
- Loads bundled Blackjack card art through the mod asset interface.

## Apply

```bash
python scripts/patch_mod.py mod.zip
```

Generated output:

```text
Gen1Online-GameCorner-v0.3.4.3-sandbox.1-android-patch.zip
```

`android-sandbox.patch.gz` is the exact compressed compatibility diff used by the patcher.

## Important

Do not treat static/sandbox loading as proof that every online feature behaves identically. PvP/GTS/Game Corner networking should be tested against the live service before this patch is marked fully Android-verified.

## Distribution note

The licensing of the complete current package is not sufficiently clear for this repository to republish the whole mod, so the compatibility work is patch-only.
