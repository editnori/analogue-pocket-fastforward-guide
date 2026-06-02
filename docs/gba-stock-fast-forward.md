# GBA Stock Fast-Forward Notes

This is separate from the experimental GBA speed-level patch.

The stock `mincer-ray/openfpga-GBA` core already exposes useful fast-forward and
turbo controls:

- `Fast Forward Mode`
  - `Hold`
  - `Toggle`
  - `Disabled`
- `Turbo`
  - `Disabled`
  - `Turbo A Button`
  - `Turbo B Button`

For an Emerald-style test where the Pocket right trigger should fast-forward:

1. Set `Fast Forward Mode = Hold`.
2. Set `Turbo = Disabled`.
3. Remap the input metadata so:
   - `Fast Forward` uses `pad_trig_r`
   - GBA `R` moves to `pad_btn_y`
   - `Turbo` stays on `pad_btn_x`

The relevant `input.json` mapping shape is:

```json
[
  { "name": "R", "key": "pad_btn_y" },
  { "name": "Fast Forward", "key": "pad_trig_r" },
  { "name": "Turbo", "key": "pad_btn_x" }
]
```

This is useful because it avoids changing the GBA bitstream while still making
the Pocket right trigger behave like fast-forward.

It does not add multiple GBA fast-forward speeds. Multiple GBA speed choices
require a working synthesized and hardware-tested GBA speed-level core.
