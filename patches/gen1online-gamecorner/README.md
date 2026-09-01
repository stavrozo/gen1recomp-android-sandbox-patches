# Gen1Online / Game Corner Edition v0.3.4.3

**Status:** ✅ Android sandbox compatibility patch + Rare Candy evolution stack fix verified on a real Android device. Live multiplayer/network behavior remains experimental until exercised end-to-end.

This patch targets the exact `mod.zip` package identified as Gen1Online / Game Corner Edition v0.3.4.3 during testing.

## Sandbox compatibility fix

- Removes direct `love.thread` dependency from the compatibility build.
- Replaces raw filesystem-dependent asset/save paths with sandbox-compatible paths used by the tested build.
- Uses cooperative request queues in place of the old LÖVE worker-thread channels.
- Loads bundled Blackjack card art through the mod asset interface.

The first-stage compatibility output is:

```text
Gen1Online-GameCorner-v0.3.4.3-sandbox.1-android-patch.zip
```

`android-sandbox.patch.gz` is the exact compressed compatibility diff used by the normal patcher.

## sandbox.4 Rare Candy evolution fix

A separate runtime bug was reproduced on Android with Gen1Online as the only enabled mod: a Rare Candy evolution completed, displayed the evolved Pokémon, then exposed the stale `What? ... is evolving!` textbox instead of returning to the bag/party flow.

The root cause was not saving or networking. `pokemon.evolved` fires while Gen1Recomp's `EvolutionState` is still on the state stack. If that event raises the Gen1Online MMO level, `addMmoXp()` immediately pushes its own `LEVEL UP! REACHED MMO LEVEL ...` textbox between `EvolutionState` and Gen1Recomp's normal evolution-result textbox. When the result textbox closes, the engine pops the unexpected Gen1Online textbox instead of `EvolutionState`, leaving the completed evolution state and original intro textbox visible.

`sandbox.4` preserves the MMO XP and MMO level-up message but defers that notification until `EvolutionState` has fully left the stack.

The exact reviewed overlay is:

```text
patches/gen1online-gamecorner/evolution-stack.patch
```

The earlier offline forced-save hypothesis was tested separately and did **not** fix the device reproduction; it is intentionally not part of sandbox.4.

## Apply

First build the verified sandbox.1 package from the exact upstream v0.3.4.3 `mod.zip`:

```bash
python scripts/patch_mod.py mod.zip
```

Then upgrade that verified sandbox.1 package to sandbox.4:

```bash
python scripts/upgrade_gen1online_sandbox1.py Gen1Online-GameCorner-v0.3.4.3-sandbox.1-android-patch.zip
```

The upgrader refuses an unknown sandbox.1 `main.lua` or `manifest.json`, applies the exact evolution-stack overlay, and verifies the final sandbox.4 hashes.

Run the regression checks with:

```bash
python tests/test_gen1online_sandbox4.py
```

## Android verification

The Rare Candy evolution fix was verified on-device in two stages:

1. With Gen1Online as the only enabled mod, the evolution completed and returned normally instead of exposing the stale evolution textbox.
2. The same sandbox.4 build was then tested with the full 15-mod Android setup enabled and the evolution flow still completed normally.

The generated sandbox.4 payload that passed device testing has these changed-file hashes:

```text
main.lua      2e886850ec2fb0a7982b03ed080e7f035abdb752b46218d5adb095b6ca382f1c
manifest.json cd6161cf5eef62f0e9be9e93171c7909b42cdfca75c875e51bcc519d73311da5
```

## Important

Do not treat the verified evolution/sandbox behavior as proof that every online feature behaves identically. PvP, GTS, Game Corner networking, and live multiplayer should still be treated as experimental until independently exercised against the live service.

## Distribution note

The licensing of the complete current package is not sufficiently clear for this repository to republish the whole mod, so the compatibility work remains patch-only.
