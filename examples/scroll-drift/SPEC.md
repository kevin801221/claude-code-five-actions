# Scroll drift acceptance contract

Goal: remove idle drift without removing manual scrolling.

- Starting at 120, ten idle ticks leave the position at 120.
- A wheel delta of +80 moves position 120 to 200.
- A wheel delta of -60 moves position 120 to 60.
- A wheel delta of -80 from position 20 clamps at 0.

Timer interval in the optional browser demo: 750ms. The automated suite drives the policy synchronously; it does not measure timer timing, layout, device-specific wheel units, keyboard input, or real browser integration.

Intentional fixtures: `buggy` fails idle stability; `overfixed` fails manual behavior; `fixed` meets all four policy conditions.
