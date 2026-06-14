# Bumpyng Game

## Overview

Bumpyng Game is a 2D elastic particle collision simulation built with Python and CustomTkinter. It currently simulates two configurable special particles and 500 blue particles. All particles move with random velocities, bounce off window boundaries, and collide with each other.

The special particles leave faded motion trails and shift color smoothly based on speed.

## Features

- 2D particle motion with boundary bouncing
- Pairwise elastic collision resolution
- White and red special particles with faded motion trails
- Smooth speed-dependent special-particle color shift toward orange-red
- Pulsing glow effect for special particles
- Spatial-grid collision candidate search
- Click-to-spawn blue particles
- Right-click repulsion force for nearby particles
- Spacebar pause/resume
- Slider to adjust blue-particle count
- On-canvas HUD with blue count, FPS, and paused state
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
│   ├── config.py                <- simulation constants, specials, effects, grid, interaction, HUD
│   ├── physics.py               <- Particle class, resolve_collision
│   └── simulation.py            <- Simulation class, spatial grid, spawn/repel/count/reset logic
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
| `BLUE_PARTICLE_COUNT` | `500` | Initial number of regular blue particles |
| `WHITE_RADIUS` | `20` | Radius of the white special particle |
| `RED_RADIUS` | `12` | Radius of the red special particle |
| `BLUE_RADIUS` | `5` | Radius of regular blue particles |
| `RANDOM_VELOCITY_RANGE` | `10` | Max starting velocity component |
| `TRAIL_LENGTH` | `200` | Max path points stored for trail |
| `FRAME_DELAY_MS` | `16` | Milliseconds between frames (~60 FPS) |
| `BG_COLOR` | `"#0a0a19"` | Canvas background color |
| `BLUE_COLOR` | `"#024265"` | Regular particle color |
| `TRAIL_COLOR` | `"#6464ff"` | Default special-particle trail color |
| `RED_COLOR` | `"#ff4040"` | Initial red special-particle color |
| `RED_TRAIL_COLOR` | `"#ff9900"` | Red special-particle trail color |
| `TRAIL_FADE` | `True` | Toggles faded/tapered trails versus fixed-color trails |
| `GLOW_ENABLED` | `True` | Enables/disables special-particle glow rendering |
| `GLOW_RINGS` | `4` | Number of glow rings when glow is enabled |
| `GLOW_SPREAD` | `0.6` | Glow ring radius multiplier |
| `EASE` | `0.15` | Color-blending factor for special-particle color transitions |
| `SPECIALS` | list of 2 dicts | Fractional-position configuration for special particles |
| `_MAX_RADIUS` | computed | Largest radius among blue and special particles |
| `CELL_SIZE` | `2 * _MAX_RADIUS` | Spatial-grid cell size used for collision candidate lookup |
| `REPEL_RADIUS` | `120` | Right-click repulsion radius in pixels |
| `REPEL_STRENGTH` | `8.0` | Maximum velocity kick near the repulsion center |
| `HUD_COLOR` | `"#48bcfa"` | HUD text color |
| `HUD_FONT` | `("Consolas", 14, "bold")` | HUD text font |

Current initial total particle count is 502:

```text
2 special particles + 500 blue regular particles = 502 particles
```

The slider and click-spawn interaction can change the live blue-particle count during runtime.

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
- pulse phase for glow animation
- target color for smooth color interpolation

The `move(width, height)` method updates position, handles wall bouncing, records the trail for special particles, updates the special-particle target color based on speed, and blends the current color toward that target.

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

1. special particles from the `SPECIALS` config list
2. `BLUE_PARTICLE_COUNT` blue regular particles at random positions

The simulation also provides:

- `_build_grid()` for spatial-grid collision candidates
- `set_blue_count(target)` for slider-controlled blue-particle count
- `spawn(x, y)` for click-created blue particles
- `repel(x, y)` for right-click velocity kicks
- `reset()` for reinitializing all particles

### `frontend.gui.app.App`

Builds the CustomTkinter window, renders particles using `tk.Canvas`, draws faded trails, draws glow rings, runs the animation loop with `after()`, and provides interactive controls.

Controls:

- `Reset` button: reinitializes the simulation
- Spacebar: toggles pause/resume
- Mouse click on canvas: spawns one blue particle
- Right-click / middle-click / Control-click: repels nearby particles
- Slider: changes the target number of blue particles from 0 to 2000
- Top-right HUD: displays blue count, smoothed FPS, and `[PAUSED]` state

## Physics Model

**Collision resolution** uses three steps:

1. **Distance check** — collision occurs when `distance < r1 + r2`
2. **Static resolution** — overlapping particles pushed apart by `overlap / 2` each to prevent embedding
3. **Dynamic resolution** — elastic velocity impulse applied only when particles move toward each other (prevents jitter)

Mass is proportional to `radius²`, making the special particle behave heavier than blue particles.

Collision candidate search now uses a uniform spatial grid:

1. Move all particles.
2. Assign each particle to a grid cell based on `CELL_SIZE`.
3. For each cell, compare particles against candidates from the same cell and the 8 neighboring cells.
4. Use a `checked` set to prevent resolving the same pair twice.

This keeps the collision logic simple while avoiding full all-pairs checks in typical cases.

## Rendering Notes

The renderer draws special-particle trails segment-by-segment. When `TRAIL_FADE = True`, older trail segments are blended closer to the background color while newer segments are brighter and slightly thicker. When `TRAIL_FADE = False`, trails use a fixed color and width.

Glow rendering is enabled by default:

```python
GLOW_ENABLED = True
```

Set it to `False` in `backend/config.py` to disable pulsing glow rings around special particles.

## Possible Improvements

- Tune or validate `CELL_SIZE` if collision tunneling appears at higher speeds or larger radii
- Deterministic seeding for reproducible runs
- Avoid drawing the HUD once per particle; draw it once after the particle loop
- Remove unused imports from `frontend/gui/app.py` and `backend/simulation.py`
