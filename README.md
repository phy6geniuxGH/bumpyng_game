# Bumpyng Game (under development)

## Overview

Bumpyng Game is a 2D elastic particle collision simulation built with Python and CustomTkinter. One larger special particle and 499 smaller blue particles move with random velocities, bounce off window boundaries, and collide with each other. The special particle leaves a motion trail and shifts color based on speed.

## Features

- 2D particle motion with boundary bouncing
- Pairwise elastic collision resolution
- Special particle with motion trail and speed-dependent color shift (white → orange-red)
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
│   ├── config.py                ← all simulation constants
│   ├── physics.py               ← Particle class, resolve_collision
│   └── simulation.py            ← Simulation class, tick loop
└── frontend/
    ├── assets/
    └── gui/
        └── app.py               ← CustomTkinter window and canvas renderer
```

## Simulation Parameters

All constants live in `backend/config.py`:

| Parameter | Default | Description |
| --- | --- | --- |
| `WIDTH` | `800` | Window width in pixels |
| `HEIGHT` | `600` | Window height in pixels |
| `PARTICLE_COUNT` | `500` | Total number of particles |
| `WHITE_RADIUS` | `15` | Radius of special particle |
| `BLUE_RADIUS` | `7` | Radius of regular particles |
| `RANDOM_VELOCITY_RANGE` | `10` | Max starting velocity component |
| `TRAIL_LENGTH` | `200` | Max path points stored for trail |
| `FRAME_DELAY_MS` | `16` | Milliseconds between frames (~60 FPS) |

## Physics Model

**Collision resolution** uses three steps:

1. **Distance check** — collision occurs when `distance < r1 + r2`
2. **Static resolution** — overlapping particles pushed apart by `overlap / 2` each to prevent embedding
3. **Dynamic resolution** — elastic velocity impulse applied only when particles move toward each other (prevents jitter)

Mass is proportional to `radius²`, making the special particle behave heavier than blue particles.

Collision detection is O(n²) — intentional simplicity, acceptable at 500 particles.

## Possible Improvements

- Spatial partitioning (uniform grid, quadtree) for O(n²) bottleneck
- Pause/resume keyboard shortcut
- FPS and particle count display
- Deterministic seeding for reproducible runs
- Adjustable particle count via UI slider
