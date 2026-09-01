# Gen1Online / Game Corner Edition v0.3.4.3

**Status:** ⚠️ Android sandbox compatibility patch prepared. The original sandbox errors are addressed, but live multiplayer/network behavior remains experimental until exercised end-to-end.

This patch targets the exact `mod.zip` package identified as Gen1Online / Game Corner Edition v0.3.4.3 during testing.

## Fix

- Removes direct `love.thread` dependency from the compatibility build.
- Replaces raw filesystem-dependent asset/save paths with sandbox-compatible paths used by the tested build.
- Uses cooperative request queues in place of the old LÖVE worker-thread channels.
- Loads bundled Blackjack card art through the mod asset interface.

## sandbox.2 Rare Candy evolution backport

A reproducible Android issue was isolated to Gen1Online v0.3.4.3-sandbox.1: when a Pokémon evolves from a Rare Candy while Gen1Online is the only enabled mod, the evolution completes but the stale `What? ... is evolving!` textbox becomes visible again instead of returning cleanly to the party/bag flow.

Vanilla Gen1Recomp does not reproduce the issue. The older Gen1Online v0.3.4.3 code force-saves from `pokemon.evolved`, including while offline. Newer Gen1Online code explicitly skips forced saves while disconnected. `sandbox.2` backports only that offline-save guard so the evolution UI can finish unwinding before any normal save occurs.

The first-stage sandbox patch remains unchanged and fully hash-verified. The `sandbox.2` upgrader accepts only the known `sandbox.1` `main.lua` and `manifest.json` hashes before applying the backport.

## Apply

First build the verified sandbox.1 package from the exact upstream v0.3.4.3 `mod.zip`:

```bash
python scripts/patch_mod.py mod.zip
```

Generated output:

```text
Gen1Online-GameCorner-v0.3.4.3-sandbox.1-android-patch.zip
```

Then upgrade that exact package to the sandbox.2 test build:

```bash
python scripts/upgrade_gen1online_sandbox1.py Gen1Online-GameCorner-v0.3.4.3-sandbox.1-android-patch.zip
```

The output filename is automatically changed from `sandbox.1` to `sandbox.2`, and the embedded manifest version becomes `0.3.4.3-sandbox.2`.

Run the regression checks with:

```bash
python tests/test_gen1online_sandbox2.py
```

`android-sandbox.patch.gz` remains the exact compressed compatibility diff used for the original sandbox.1 migration.

## Important

Do not treat static/sandbox loading as proof that every online feature behaves identically. PvP/GTS/Game Corner networking should still be tested against the live service before this patch is marked fully Android-verified.

The sandbox.2 Rare Candy evolution backport should also be considered provisional until verified on a real Android device with Gen1Online enabled.

## Distribution note

The licensing of the complete current package is not sufficiently clear for this repository to republish the whole mod, so the compatibility work is patch-only.
