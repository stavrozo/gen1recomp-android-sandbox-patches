# Wilds of Kanto v2.1.0 — archived compatibility patch

**Status:** 🗃️ Archived. Superseded by upstream **Wilds of Kanto 2.1.5**.

This patch targets the exact original `Wilds.of.Kanto.v2.1.0.zip` used during our Android testing. It is kept for historical/reference purposes and for anyone intentionally staying on that exact old release.

## Upstream replacement

Wilds of Kanto **2.1.5** officially updates the mod for the current Gen1Recomp sandbox, replacing deprecated/direct filesystem access with supported mod asset APIs. Its changelog also fixes Wilds/followers/town Pokémon disappearing after battles and follower reattachment after returning to the overworld.

**New installs should use the official upstream 2.1.5 release instead of this patch.**

## What this old patch fixed

- Replaced affected direct `love.filesystem` runtime access for the newer sandbox.
- Preserved packaged sprite fallbacks.
- Included the follow-up `trueColor` correction discovered during testing so full-color Pokémon/follower sprites did not turn into dark silhouettes when runtime luminance generation was unavailable.

## Historical apply command

```bash
python scripts/patch_mod.py Wilds.of.Kanto.v2.1.0.zip
```

Generated output:

```text
Wilds.of.Kanto.v2.1.1-sandbox.2.android.patch.zip
```

`android-sandbox.patch.gz` is the exact compressed unified diff used by the patcher. It remains in the repository so the work is auditable, but it is no longer the recommended fix.

## Distribution note

Wilds code is MIT licensed, but the upstream package contains separately attributed/licensed third-party artwork. This repository therefore publishes the compatibility patch, not a full repack of the mod/assets.
