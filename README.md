# Analogue Pocket Fast-Forward Speed Controls

This repo documents the openFPGA fast-forward speed-control pattern used for an
Analogue Pocket GBC custom-speed build.

It does not contain ROMs, BIOS files, saves, or generated bitstreams.

## What Is Proven

- `budude2/openfpga-GBC` can expose a persistent `Speed Level` menu with:
  `1x`, `1.5x`, `2x`, `3x`, and `4x`.
- The setting is written through openFPGA `interact.json`.
- The HDL clamps the requested percent to `100..400`.
- The core clock-enable pacing changes only while fast-forward is active.

The working GBC menu variable is:

```json
{
  "name": "Speed Level",
  "id": 1010,
  "type": "list",
  "address": "0xF3000000",
  "persist": true,
  "writeonly": true,
  "defaultval": 100,
  "options": [
    { "name": "1x", "value": 100 },
    { "name": "1.5x", "value": 150 },
    { "name": "2x", "value": 200 },
    { "name": "3x", "value": 300 },
    { "name": "4x", "value": 400 }
  ]
}
```

## Repo Contents

- `patches/gbc-speed-level.patch`: proven GBC source patch.
- `patches/gba-speed-level-experimental.patch`: experimental GBA source patch.
- `docs/how-it-works.md`: the openFPGA menu/register/HDL pattern.
- `docs/build-and-install.md`: build and SD install checklist.
- `docs/gba-stock-fast-forward.md`: stock GBA fast-forward and input remap notes.
- `docs/gba-single-fast-forward-release.md`: GBA single-mode release notes.
- `scripts/reverse-rbf-bits.py`: helper to convert Quartus `.rbf` to Pocket `.rbf_r`.
- `scripts/verify-interact-speed-level.py`: checks an `interact.json` speed menu.

## Prebuilt Core Releases

Compiled cores are published as GitHub Release assets instead of being committed
directly to git history:

https://github.com/editnori/analogue-pocket-fastforward-guide/releases

The `v0.1.0-gbc-speed-level` release contains an installable GBC custom-speed
core package with:

- `Cores/budude2.GBC/gbc.rbf_r`
- GBC core metadata
- GBC platform metadata/image
- release provenance notes

It still excludes BIOS files, ROMs, saves, and SD user data.

The `v0.1.0-gba-single-fastforward-alpha` release contains an installable GBA
test core package with:

- `Cores/mincer_ray.GBA/bitstream.rbf_r`
- GBA core metadata
- GBA platform metadata/image
- SD folder scaffold and install notes

This GBA build has one hold-to-fast-forward mode: hold Pocket right trigger for
fast-forward, and use Pocket `Y` for the GBA `R` button. It does not include or
embed a BIOS; `gba_bios.bin` is required from the user's SD card.

## Quick Start: GBC

```bash
git clone https://github.com/budude2/openfpga-GBC.git
git clone https://github.com/editnori/analogue-pocket-fastforward-guide.git

cd openfpga-GBC
git apply ../analogue-pocket-fastforward-guide/patches/gbc-speed-level.patch
python3 ../analogue-pocket-fastforward-guide/scripts/verify-interact-speed-level.py \
  pkg/gbc/Cores/budude2.GBC/interact.json
```

Build with Quartus. One Docker-based command that worked in the local build
workspace was:

```bash
docker run --rm \
  -v "$PWD:/build" \
  -w /build/src \
  raetro/quartus:21.1 \
  quartus_sh --flow compile ap_core
```

After Quartus emits an `.rbf`, reverse bits per byte for the Pocket `.rbf_r`
format:

```bash
python3 ../analogue-pocket-fastforward-guide/scripts/reverse-rbf-bits.py \
  src/output_files/ap_core.rbf \
  pkg/gbc/Cores/budude2.GBC/gbc.rbf_r
```

If your build writes the `.rbf` somewhere else, pass that actual path instead.

Copy the packaged core folder to the Pocket SD:

```text
Cores/budude2.GBC/
Platforms/
Assets/gbc/common/
```

You need your own legally obtained BIOS/ROM files. They are intentionally not in
this repo.

## Pocket Test

1. Boot `openFPGA`.
2. Launch the GBC core and a staged GBC ROM.
3. Open core settings.
4. Enable fast-forward.
5. Set `Speed Level` to `1.5x`, `2x`, `3x`, or `4x`.
6. Hold the fast-forward input and verify the game runs at the selected speed.

## GBA Status

The GBA multi-speed patch in this repo is still experimental. It documents the
same percent/list idea for `mincer-ray/openfpga-GBA`, but it still needs
synthesis and hardware acceptance before it should be treated as proven.

There is now a simpler compiled GBA alpha release that removes the menu/toggle
fast-forward options and leaves exactly one mode:

- Pocket right trigger: hold-to-fast-forward
- Pocket `Y`: GBA `R`
- Turbo removed
- `gba_bios.bin` required on SD; no BIOS is embedded in the bitstream

This is the normal SD-ROM GBA core path. It is not a physical cartridge adapter
or cart-save alpha build.

For stock GBA on Pocket, the useful proven path is input/settings based:

- `Fast Forward Mode = Hold`
- `Turbo = Disabled` unless testing A/B turbo
- optional input remap: Pocket right trigger = Fast Forward, `Y` = GBA `R`

See `docs/gba-stock-fast-forward.md`.

## Safety

Do not publish or commit:

- Nintendo BIOS files
- game ROMs
- save files
- `.rbf` or `.rbf_r` bitstreams
- full copied proprietary/vendor workspaces

This repo is documentation, patches, and small helper scripts only.
