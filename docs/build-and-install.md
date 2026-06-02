# Build And Install Checklist

This checklist is for the GBC patch.

## Requirements

- A clean `budude2/openfpga-GBC` checkout.
- Quartus, or Docker with the `raetro/quartus:21.1` image.
- An Analogue Pocket SD card.
- Your own BIOS and ROM files.

## Patch

```bash
git clone https://github.com/budude2/openfpga-GBC.git
git clone https://github.com/editnori/analogue-pocket-fastforward-guide.git
cd openfpga-GBC
git apply ../analogue-pocket-fastforward-guide/patches/gbc-speed-level.patch
```

Verify the menu metadata:

```bash
python3 ../analogue-pocket-fastforward-guide/scripts/verify-interact-speed-level.py \
  pkg/gbc/Cores/budude2.GBC/interact.json
```

Expected output includes:

```text
ok: Speed Level has options 1x=100, 1.5x=150, 2x=200, 3x=300, 4x=400
```

## Build

One working Docker build form:

```bash
docker run --rm \
  -v "$PWD:/build" \
  -w /build/src \
  raetro/quartus:21.1 \
  quartus_sh --flow compile ap_core
```

Quartus output paths can vary. Find the generated `.rbf`:

```bash
find . -name '*.rbf' -print
```

Convert to Pocket `.rbf_r`:

```bash
python3 ../analogue-pocket-fastforward-guide/scripts/reverse-rbf-bits.py \
  path/to/ap_core.rbf \
  pkg/gbc/Cores/budude2.GBC/gbc.rbf_r
```

## Install

Copy the packaged GBC core metadata and bitstream to the Pocket SD root:

```text
Cores/budude2.GBC/
Platforms/
```

Place your own GBC BIOS at the path expected by your core/package. A common path
is:

```text
Assets/gbc/common/gbc_bios.bin
```

This repo does not provide that file.

## Verify On Pocket

1. Boot `openFPGA`.
2. Launch a GBC ROM through the patched GBC core.
3. Open core settings.
4. Confirm `Speed Level` appears.
5. Test `1.5x`, `2x`, `3x`, and `4x` while fast-forward is active.

If `Speed Level` is missing, recheck that the patched `interact.json` is on the
SD in `Cores/budude2.GBC/interact.json`.

If the menu appears but speed does not change, recheck that the patched `.rbf_r`
was installed, not only the metadata.
