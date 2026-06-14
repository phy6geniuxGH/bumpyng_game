# Bumpyng Game

## Overview

Bumpyng Game is a 2D elastic particle collision simulation built with Python and CustomTkinter. It currently simulates one white special particle, one red special particle, and 499 small blue particles. All particles move with random velocities, bounce off window boundaries, and collide with each other.

The special particles leave faded motion trails and shift color smoothly based on speed.

## Features

- 2D particle motion with boundary bouncing
- Pairwise elastic collision resolution
- White and red special particles with faded motion trails
- Smooth speed-dependent special-particle color shift toward orange-red
- Optional pulsing glow effect for special particles
- Real-time animation at ~60 FPS
- Reset button to reinitialize simulation

## Requirements

Python 3.13+. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

```bash
python main.py
```

A window titled `Stable Particle Collision` opens with the simulation and a Reset button.

## Project Structure

```text
particle_collisions/
├── main.py                      ← entry point
├── backend/
│   ├── colors.py                <- hex color conversion and blending helpers
│   ├── config.py                <- simulation constants and visual effect settings
│   ├── physics.py               <- Particle class, resolve_collision
│   └── simulation.py            <- Simulation class, particle setup, tick loop
└── frontend/
    ├── assets/
    └── gui/
        └── app.py               <- CustomTkinter window and canvas renderer
```

## Simulation Parameters

All constants live in `backend/config.py`:

| Parameter | Default | Description |
| --- | --- | --- |
| `WIDTH` | `800` | Window width in pixels |
| `HEIGHT` | `600` | Window height in pixels |
| `BLUE_PARTICLE_COUNT` | `500` | White-plus-blue setup count before appending the red special particle |
| `WHITE_RADIUS` | `15` | Radius of the white special particle |
| `RED_RADIUS` | `12` | Radius of the red special particle |
| `BLUE_RADIUS` | `7` | Radius of regular blue particles |
| `RANDOM_VELOCITY_RANGE` | `10` | Max starting velocity component |
| `TRAIL_LENGTH` | `200` | Max path points stored for trail |
| `FRAME_DELAY_MS` | `16` | Milliseconds between frames (~60 FPS) |
| `BG_COLOR` | `"#0a0a19"` | Canvas background color |
| `BLUE_COLOR` | `"#48bcfa"` | Regular particle color |
| `TRAIL_COLOR` | `"#6464ff"` | Default special-particle trail color |
| `RED_COLOR` | `"#ff4040"` | Initial red special-particle color |
| `RED_TRAIL_COLOR` | `"#ff9900"` | Red special-particle trail color |
| `TRAIL_FADE` | `True` | Intended trail-fade setting; current renderer always fades trails |
| `GLOW_ENABLED` | `False` | Enables/disables special-particle glow rendering |
| `GLOW_RINGS` | `4` | Number of glow rings when glow is enabled |
| `GLOW_SPREAD` | `0.6` | Glow ring radius multiplier |
| `EASE` | `0.15` | Color-blending factor for special-particle color transitions |

Current total particle count is 501:

```text
1 white special + 499 blue regular + 1 red special = 501 particles
```

## Main Components

### `backend.physics.Particle`

Stores particle state:

- position: `x`, `y`
- radius
- color as a hex string
- velocity: `vx`, `vy`
- special-particle flag: `is_special`
- path history for trails
- trail color
- pulse phase for optional glow animation
- target color for smooth color interpolation

The `move(width, height)` method updates position, handles wall bouncing, records the trail for special particles, updates the special-particle target color based on speed, and blends the current color toward that target.

The class also includes `rx`, `ry`, and `ease_render(factor)` for eased render positions. These are currently available but not used by the canvas renderer.

### `backend.colors`

Provides small color utilities:

- `hex_to_rgb(h)`
- `rgb_to_hex(rgb)`
- `blend(c1, c2, t)`

These helpers are used for speed-based color smoothing and trail/glow color blending.

### `backend.physics.resolve_collision`

Handles pairwise particle collisions. It works for all particle combinations, including white-special vs red-special collisions.

### `backend.simulation.Simulation`

Owns the particle list and simulation update step.

During setup, it creates:

1. one white special particle at the window center
2. 499 blue regular particles at random positions
3. one red special particle at one-quarter window position

### `frontend.gui.app.App`

Builds the CustomTkinter window, renders particles using `tk.Canvas`, draws faded trails, optionally draws glow rings, runs the animation loop with `after()`, and provides the Reset button.

## Physics Model

**Collision resolution** uses three steps:

1. **Distance check** — collision occurs when `distance < r1 + r2`
2. **Static resolution** — overlapping particles pushed apart by `overlap / 2` each to prevent embedding
3. **Dynamic resolution** — elastic velocity impulse applied only when particles move toward each other (prevents jitter)

Mass is proportional to `radius²`, making the special particle behave heavier than blue particles.

Collision detection is O(n²) — intentional simplicity, acceptable at the current scale.

## Rendering Notes

The renderer currently draws special-particle trails segment-by-segment. Older trail segments are blended closer to the background color, while newer segments are brighter and slightly thicker.

Glow rendering is implemented but disabled by default:

```python
GLOW_ENABLED = False
```

Set it to `True` in `backend/config.py` to enable pulsing glow rings around special particles.

## Possible Improvements

- Spatial partitioning (uniform grid, quadtree) for O(n²) bottleneck
- Pause/resume keyboard shortcut
- FPS and particle count display
- Deterministic seeding for reproducible runs
- Adjustable particle count via UI slider
- Wire `TRAIL_FADE` into the renderer so faded trails can be toggled
- Use `Particle.rx` and `Particle.ry` if eased rendering is desired
- Clarify whether `BLUE_PARTICLE_COUNT` should include or exclude the white special particle
