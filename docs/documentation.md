# Bumpyng Game: Technical Documentation

## Architecture

```text
main.py                  entry point, creates App, binds window close
backend/                 pure Python, no GUI dependency
  config.py              all constants
  colors.py              hex <-> RGB, linear blend
  physics.py             Particle, resolve_collision
  simulation.py          Simulation: particle list, grid, tick, spawn, repel, count, reset
frontend/gui/app.py      CustomTkinter window, tk.Canvas renderer, input, main loop
```

Data flow per frame:

```text
App._loop()
  -> Simulation.tick()        (skipped when paused)
       -> Particle.move()     for all particles
       -> _build_grid()
       -> resolve_collision() for each candidate pair
  -> App._render()            clear canvas, draw glow, trails, particles, HUD
  -> after(FRAME_DELAY_MS, _loop)
```

## Backend

### `Particle` (`backend/physics.py`)

| Attribute | Meaning |
|---|---|
| `x, y` | Position (px) |
| `vx, vy` | Velocity (px per frame), random in `[-RANDOM_VELOCITY_RANGE, RANDOM_VELOCITY_RANGE]` |
| `radius` | Collision radius (px) |
| `color`, `target_color` | Current and target fill color (hex) |
| `is_special` | Enables trail, glow, speed-based color |
| `path` | Trail points, capped at `TRAIL_LENGTH` |
| `trail_color` | Trail color |
| `pulse_phase` | Glow pulse phase (rad) |

`move(width, height)`: integrate position, reflect velocity at walls, and for specials append to trail, update speed-based color (eased by `EASE`), advance pulse.

### `resolve_collision(p1, p2)`

1. Collide if `distance < r1 + r2`.
2. Static: push each particle apart by `overlap / 2` along the normal.
3. Dynamic: if approaching (`dot < 0`), apply elastic impulse with mass `m = r^2`.

Elastic impulse, with unit normal `n` and relative velocity `v_rel = v1 - v2`:

```text
J  = 2 (v_rel . n) / (m1 + m2)
v1 = v1 - J m2 n
v2 = v2 + J m1 n
```

Momentum and kinetic energy are conserved.

### `Simulation` (`backend/simulation.py`)

| Method | Purpose |
|---|---|
| `_setup()` | Create specials from `SPECIALS`, then `BLUE_PARTICLE_COUNT` blues |
| `tick()` | Move all, build grid, resolve collisions in 3x3 cell neighborhoods, dedupe pairs with a set |
| `set_blue_count(n)` | Add or trim blues to reach `n` |
| `spawn(x, y)` | Add one blue |
| `repel(x, y)` | Radial velocity kick with linear falloff inside `REPEL_RADIUS` |
| `reset()` | Re-run `_setup()` |

Grid: `CELL_SIZE = 2 * max radius`, so any colliding pair lies in the same or an adjacent cell.

### `colors.py`

`hex_to_rgb`, `rgb_to_hex` (clamped 0..255), `blend(c1, c2, t)` (linear, `t=0 -> c1`, `t=1 -> c2`).

## Frontend (`frontend/gui/app.py`)

| Input | Action |
|---|---|
| Left click | Spawn a blue particle |
| Right click, middle click, Ctrl+click | Repel nearby particles |
| Space | Pause or resume |
| Slider (0 to 2000) | Set blue particle count |
| Reset button | Reinitialize simulation |

Render order per particle: glow rings (specials), trail (specials), body. HUD shows blue count, smoothed FPS (frames per second), and pause state.

## Configuration

All constants are in `backend/config.py`. Main groups:

| Group | Keys |
|---|---|
| World | `WIDTH`, `HEIGHT`, `FRAME_DELAY_MS` |
| Particles | `BLUE_PARTICLE_COUNT`, `BLUE_RADIUS`, `WHITE_RADIUS`, `RED_RADIUS`, `RANDOM_VELOCITY_RANGE`, `SPECIALS` |
| Colors | `BG_COLOR`, `BLUE_COLOR`, `TRAIL_COLOR`, `RED_COLOR`, `RED_TRAIL_COLOR` |
| Effects | `TRAIL_LENGTH`, `TRAIL_FADE`, `GLOW_ENABLED`, `GLOW_RINGS`, `GLOW_SPREAD`, `EASE` |
| Grid | `CELL_SIZE` (derived) |
| Interaction | `REPEL_RADIUS`, `REPEL_STRENGTH` |
| HUD | `HUD_COLOR`, `HUD_FONT` |

`SPECIALS` positions are fractions of `WIDTH` and `HEIGHT`.

## Known issues

Tracked in [`../redevelopment.md`](../redevelopment.md). Main ones: HUD drawn per particle, coarse collision grid, full canvas redraw per frame, no speed cap (tunneling), frame-dependent physics.
