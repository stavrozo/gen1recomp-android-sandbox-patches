# Gen1Recomp Android Sandbox Patches — Design

## Purpose

Create a public, unofficial compatibility project that documents and distributes safe fixes for Gen1Recomp mods that broke after the newer Android sandbox/runtime API changes.

The project must be useful to players while respecting original mod authors, upstream licenses, third-party asset restrictions, and Gen1Recomp's no-ROM-content rules.

## Scope

Initial coverage is limited to the five mods already repaired and tested on Android:

1. Crystal Animated Sprites with Shiny Visuals v1.6
2. Wilds of Kanto v2.1.0
3. Shiny Pokémon v1.0.1
4. Gen1Online / Game Corner Edition v0.3.4.3
5. Dramaless Shape v2.0.1

No unrelated mod hosting, ROM distribution, ROM patching, or copyrighted game-file distribution is in scope.

## Distribution Model

Use a hybrid model based on the upstream license status of each mod.

### Full patched build allowed

**Shiny Pokémon v1.0.1**

The upstream project is MIT licensed. A ready-to-install patched ZIP may be distributed if the original MIT notice is preserved and the package is clearly labeled as an unofficial compatibility build.

### Patch-only / local patcher

The following projects will not have their full original packages redistributed from this repository:

- **Crystal Animated Sprites v1.6** — no clear upstream license found.
- **Wilds of Kanto v2.1.0** — MIT-covered code exists, but the package includes separately licensed third-party artwork/assets.
- **Gen1Online / Game Corner v0.3.4.3** — licensing of the whole project/package is unclear.
- **Dramaless Shape v2.0.1** — mixed/complicated licensing and inherited components make full-package redistribution unnecessarily risky.

For these four mods, the repository will contain only our patch logic, documentation, checksums/version requirements, and a local patching workflow. Users must obtain the original mod from its original author/source and apply the patch locally.

## Repository Structure

```text
/
├── README.md
├── LICENSE
├── NOTICE.md
├── CHANGELOG.md
├── docs/
│   ├── licensing.md
│   ├── compatibility.md
│   └── superpowers/
│       ├── specs/
│       └── plans/
├── patches/
│   ├── crystal-animated-sprites/
│   ├── wilds-of-kanto/
│   ├── shiny-pokemon/
│   ├── gen1online-gamecorner/
│   └── dramaless-shape/
├── scripts/
│   ├── patch_mod.py
│   └── lib/
└── tests/
```

Each mod folder will contain:

- `README.md` with upstream attribution and exact supported source version.
- a machine-readable patch definition or unified diff containing only our changes.
- expected source-file hashes/checksums where practical.
- expected output version name.
- a concise test/reproduction note.

## Patcher Architecture

A small Python patcher will operate only on a user-supplied original ZIP.

Workflow:

1. User downloads the exact original mod version from the upstream author.
2. User runs the patcher against that ZIP.
3. The patcher validates the mod identity/version and, where possible, checks expected hashes before modifying anything.
4. It extracts into a temporary working directory.
5. It applies only the compatibility changes defined for that mod/version.
6. It removes prohibited packaging artifacts only when required, such as the `baseroms/` placeholder directory that caused the Dramaless Android importer rejection.
7. It updates the local compatibility version string so the result is distinguishable from upstream.
8. It scans the patched runtime code for blocked APIs relevant to the fix.
9. It rebuilds a new ZIP without altering the user's original download.
10. It reports the output filename and verification results.

The patcher must refuse unknown versions rather than guessing.

## Compatibility Fixes to Preserve

### Crystal Animated Sprites

- Replace blocked direct filesystem access with Gen1Recomp mod-safe read behavior.
- Replace unsupported directory/file checks with package-safe equivalents.
- Preserve animated Pokémon sprite behavior and shiny visual support.

Target compatibility build name: `v1.6.1-android-sandbox` or equivalent.

### Wilds of Kanto

- Remove direct use of blocked `love.filesystem` APIs from the affected runtime paths.
- Preserve packaged-asset fallback behavior.
- Preserve the corrected `trueColor` fallback so full-color Pokémon sprites are not incorrectly treated as Game Boy luminance sheets.

Target compatibility build name: `v2.1.1-android-sandbox` or equivalent.

### Shiny Pokémon

- Replace blocked filesystem use.
- Keep shiny DV generation, battle sparkle behavior, shiny palettes, Wilds integration, and follower rendering.
- Use in-memory caching where the original implementation attempted runtime filesystem cache writes.

A ready-to-install patched ZIP may be published under the upstream MIT terms.

### Gen1Online / Game Corner

- Remove direct `love.thread` and blocked filesystem dependencies from the compatibility build.
- Keep networking/persistence behavior documented as experimental until separately verified against the live server.
- Do not claim online behavior is fully equivalent unless runtime tests prove it.

### Dramaless Shape

- Correct the render-distance coordinate-space bug that compared world-pixel NPC/follower coordinates against player grid-cell coordinates.
- Keep Voxel mode behavior intact rather than bypassing occlusion globally.
- Remove the `baseroms/` placeholder directory from generated Android-compatible packages because the current importer rejects the package based on that path.

## Licensing and Attribution Rules

- Never include ROMs, baseroms, extracted Pokémon game data, or user ROM files.
- Never copy an entire upstream mod into this repository unless its license clearly permits redistribution and all bundled assets are covered.
- Preserve upstream copyright and license notices when redistribution is allowed.
- Keep our own repository license scoped to original code written for this compatibility project; it does not relicense upstream mods or third-party assets.
- `NOTICE.md` will identify each original project and make clear that the compatibility project is unofficial and unaffiliated with the original authors or Gen1Recomp.
- License status must be rechecked before each public release because upstream repositories can change.

## User Experience

The root README should make the safe path obvious:

- identify the mod that broke;
- download the original supported version from upstream;
- use the local patcher for patch-only mods;
- use the ready-made package only where redistribution is clearly permitted;
- import the generated ZIP through Gen1Recomp's normal mod importer;
- keep original downloads as backups;
- never delete saves or ROMs as part of this process.

## Error Handling

The patcher must stop with a clear message when:

- the ZIP is not the expected mod;
- the source version is unsupported;
- required source files are missing;
- expected content has changed enough that the patch cannot safely apply;
- a generated archive still contains prohibited ROM-like/baserom paths;
- output verification fails.

It must not silently apply partial patches.

## Testing Strategy

Testing is split into three levels.

### Static tests

- Validate ZIP integrity.
- Validate expected files are present.
- Verify prohibited paths are absent from generated packages.
- Scan relevant Lua sources for banned direct APIs targeted by each patch.
- Validate manifests/version metadata.

### Regression tests

Each patch gets a targeted test for the actual bug it fixes. Examples:

- Wilds: full-color fallback must remain `trueColor=true` when luminance generation is unavailable.
- Dramaless: render distance must compare coordinates in the same unit space.
- Shiny: runtime cache behavior must not require filesystem writes.

### Android runtime verification

Document real-device results separately. Static checks must not be described as proof that a mod works on Android. A compatibility build is marked "Android verified" only after the relevant feature is exercised in Gen1Recomp on-device.

## Release Policy

- Patch-only projects publish source patches/patcher definitions and instructions.
- Shiny Pokémon may additionally publish a ready-to-install ZIP while its MIT licensing remains clear.
- Compatibility versions use an explicit suffix such as `-android-sandbox` so users do not confuse them with upstream releases.
- Every release states the exact upstream version it targets.
- Future upstream versions require a new verification pass; patches are never assumed forward-compatible.

## Success Criteria

The first public version is successful when:

- all five repaired mods have clear documentation;
- the four restricted/unclear-license mods can be patched locally without redistributing their original packages;
- Shiny Pokémon has a license-compliant ready-to-install compatibility build;
- generated ZIPs contain no ROM/baserom content;
- the known Android sandbox errors are covered by regression/static tests;
- the Dramaless render-distance regression is covered by a specific test;
- the README clearly credits original authors and labels the project unofficial;
- no compatibility claim exceeds what was actually verified on-device.

## Non-Goals

- Hosting Pokémon ROMs or ROM-derived game data.
- Replacing the original mod repositories.
- Claiming ownership of upstream mods or artwork.
- Automatically patching unknown/new versions.
- Making a universal Gen1Recomp mod fixer in the first release.
- Hiding upstream attribution or license notices.
