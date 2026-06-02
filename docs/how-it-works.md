# How The Speed Control Works

The useful pattern is:

1. Add an openFPGA `interact.json` list setting.
2. Write that setting to a private bridge/register address.
3. Clamp and synchronize the value into the core clock domain.
4. Use a small accumulator to pace clock-enable pulses during fast-forward.

## GBC Menu Variable

The proven GBC build adds:

- Name: `Speed Level`
- Address: `0xF3000000`
- Values: `100`, `150`, `200`, `300`, `400`
- Meaning: `1x`, `1.5x`, `2x`, `3x`, `4x`

`interact.json` persists the choice, so the Pocket remembers it per the normal
openFPGA settings flow.

## Bridge/Register Side

The core adds a `speed_settings` register. Writes to `0xF3000000` update it, and
reads from the same address return it.

The value is synchronized from the bridge clock domain to the system clock domain
with the same synchronizer style used for other runtime settings.

## Clamp

The GBC patch clamps the lower 10 bits:

```systemverilog
ff_speed_percent = (speed_settings_s[9:0] < 10'd100) ? 10'd100 :
                   (speed_settings_s[9:0] > 10'd400) ? 10'd400 :
                                                        speed_settings_s[9:0];
```

That keeps bad menu writes from requesting a speed below normal or above the
tested range.

## Pacing

The original fast-forward path was effectively one fixed faster mode. The patch
turns it into a percent-controlled clock-enable pulse generator.

At `400`, the accumulator emits pulses at the highest tested rate. At `200`, it
emits half as many. At `100`, it behaves like normal speed.

The key detail is that this pacing is used only while fast-forward is active. If
fast-forward is off, normal play stays locked to the original pacing.

## Why Percent Values

Using `100`, `150`, `200`, `300`, and `400` keeps the menu easy to read and gives
future scripts a common meaning across cores:

- `100` = `1x`
- `150` = `1.5x`
- `200` = `2x`
- `300` = `3x`
- `400` = `4x`

That is easier to reason about than core-specific magic enum values.
