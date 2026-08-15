# Wilds of Kanto v2.1.0

**Status:** ✅ Verified on Android.

This patch targets the exact original `Wilds.of.Kanto.v2.1.0.zip` used during testing.

## Fix

- Replaces affected direct `love.filesystem` runtime access for the newer sandbox.
- Preserves packaged sprite fallbacks.
- Includes the follow-up `trueColor` correction discovered during testing so full-color Pokémon/follower sprites do not turn into dark silhouettes when runtime luminance generation is unavailable.

## Apply

```bash
python scripts/patch_mod.py Wilds.of.Kanto.v2.1.0.zip
```

Generated output:

```text
Wilds.of.Kanto.v2.1.1-sandbox.2.android.patch.zip
```

`android-sandbox.patch.gz` is the exact compressed unified diff used by the patcher. It is compressed only because the Wilds diff is comparatively large.

## Distribution note

Wilds code is MIT licensed, but the upstream package contains separately attributed/licensed third-party artwork. This repository therefore publishes the compatibility patch, not a full repack of the mod/assets.
