# Stable Particle Collision Simulation

## Overview

This project is a simple `pygame` simulation of elastic particle collisions in a 2D rectangular window.

The simulation creates one larger special particle and many smaller blue particles. Each particle moves with a random initial velocity, bounces off the window boundaries, and collides with other particles. The special particle leaves a visual trail and changes color based on its speed.

## Features

- 2D particle motion using `pygame`
- Boundary collision with edge bouncing
- Pairwise particle collision resolution
- One special particle with:
  - larger radius
  - motion trail
  - speed-dependent color shift
- Real-time animation at 60 frames per second

## Requirements

The code requires Python and `pygame`.

Install `pygame` with:

```bash
pip install pygame
```

## How to Run

From the project directory, run:

```bash
python main.py
```

A window titled `Stable Particle Collision` should open and display the particle simulation.

## Code Structure

The main file is `main.py`.

```text
main.py
├── Imports
├── Simulation configuration
├── Pygame initialization
├── Particle class
├── resolve_collision function
└── main simulation loop
```

## Simulation Parameters

The top section of `main.py` defines the main simulation constants:

| Parameter | Description |
| --- | --- |
| `WIDTH` | Window width in pixels |
| `WIDTH_SIZE` | Window height in pixels |
| `PARTICLE_COUNT` | Total number of particles |
| `WHITE_RADIUS` | Radius of the special particle |
| `BLUE_RADIUS` | Radius of the regular particles |
| `WHITE_COLOR` | Initial color of the special particle |
| `BLUE_COLOR` | Color of regular particles |
| `TRAIL_COLOR` | Color of the special particle's trail |
| `RANDOM_VELOCITY_RANGE` | Maximum magnitude range for random starting velocity components |

Current default values:

```python
WIDTH, WIDTH_SIZE = 800, 600
PARTICLE_COUNT = 500
WHITE_RADIUS = 15
BLUE_RADIUS = 7
RANDOM_VELOCITY_RANGE = 10
```

## Particle Class

The `Particle` class represents each moving particle in the simulation.

Each particle stores:

- position: `x`, `y`
- radius
- color
- velocity: `vx`, `vy`
- whether it is the special particle
- path history for the special particle trail

### Movement

The `move()` method updates particle position:

```python
self.x += self.vx
self.y += self.vy
```

It also handles wall collisions by reversing the relevant velocity component when the particle reaches a boundary.

For example, when a particle hits the left or right wall, `vx` is multiplied by `-1`.

### Special Particle Behavior

If a particle is marked as special with `is_special=True`, it stores recent positions in `self.path`.

This path is used to draw a motion trail.

The special particle also changes color based on speed:

```python
speed = math.sqrt(self.vx**2 + self.vy**2)
intensity = min(1.0, speed / 10.0)
```

As the speed increases, the particle shifts from white toward orange-red.

## Collision Resolution

Particle collisions are handled by:

```python
resolve_collision(p1, p2)
```

The function has three main steps.

### 1. Distance Check

The function computes the distance between two particles:

```python
dx = p1.x - p2.x
dy = p1.y - p2.y
distance = math.sqrt(dx**2 + dy**2)
```

A collision occurs when:

```python
distance < p1.radius + p2.radius
```

### 2. Static Resolution

If particles overlap, they are pushed apart.

This prevents particles from remaining embedded in each other across frames, which can cause visual glitches and unstable motion.

### 3. Dynamic Resolution

The function then updates particle velocities using an elastic-collision style impulse calculation.

Mass is approximated as proportional to radius squared:

```python
m1 = p1.radius**2
m2 = p2.radius**2
```

This makes the larger special particle behave as if it is heavier than the smaller particles.

Velocity is only changed when particles are moving toward each other. This avoids repeated acceleration from already-separated particles.

## Main Loop

The `main()` function performs the full simulation workflow:

1. Create the special particle at the center of the window.
2. Create regular blue particles at random positions.
3. Start the simulation loop.
4. Handle quit events.
5. Move each particle.
6. Resolve collisions between particle pairs.
7. Draw each particle.
8. Refresh the screen.
9. Limit the simulation to 60 FPS.

The loop continues until the user closes the `pygame` window.

## Notes

The current implementation checks every particle against every other particle. This is simple and readable, but it has quadratic complexity:

```text
O(n^2)
```

With `PARTICLE_COUNT = 500`, this means many collision checks per frame.

For larger simulations, possible optimizations include:

- spatial partitioning
- uniform grids
- quadtrees
- reducing the particle count
- separating physics update and rendering logic

## Possible Improvements

- Rename `WIDTH_SIZE` to `HEIGHT` for clarity.
- Move configuration constants into a dedicated settings section or file.
- Add keyboard controls to pause, reset, or adjust particle count.
- Add a frame-rate or particle-count display.
- Use spatial partitioning to improve performance for larger particle counts.
- Add deterministic seeding for reproducible simulations.

