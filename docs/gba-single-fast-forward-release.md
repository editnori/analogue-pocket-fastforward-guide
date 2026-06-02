# GBA Single Fast-Forward Release Notes

This is a simpler GBA build than the experimental multi-speed patch.

Source base:

- `mincer-ray/openfpga-GBA` 0.4.0 source package

Behavior:

- Pocket right trigger is the only fast-forward input.
- Fast-forward is hold-only.
- Pocket `Y` is mapped to the GBA `R` button.
- The old `Fast Forward Mode` and `Turbo` menu entries are removed.
- Turbo input handling is removed from the HDL.

BIOS handling:

- The GBA BIOS BRAM default contents were changed to zeroes.
- `gba_bios.bin` is marked required in `data.json`.
- The release package does not include BIOS, ROM, save, or SD user-data files.

Build status:

- Quartus full compilation completed with 0 errors.
- Timing analysis reported setup timing violations on the fast system clock.
- Treat this as an alpha build until tested on hardware.

This is still the normal SD-ROM GBA core path. It does not enable physical GBA
cartridge loading or cart-save behavior.
