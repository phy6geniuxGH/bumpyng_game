# Technical Documentation

## Purpose

Bumpyng Game is a Python desktop simulation of 2D particle collisions. It uses a CustomTkinter window with a `tk.Canvas` renderer, while the simulation state and physics are kept in backend modules.

The current simulation includes:

- two configurable special particles
- 500 initial blue particles
- boundary bouncing
- elastic collision response
- spatial-grid collision candidate lookup
- faded trails and glow effects for special particles
- click-to-spawn blue particles
- right-click repulsion for nearby particles
- pause/resume with the spacebar
- slider-controlled blue-particle count
- HUD with blue count, smoothed FPS, and paused state

## Runtime Entry Point

### `main.py`

`main.py` is the application entry point.

```python
from frontend.gui.app import App
```

When run directly, it:

1. creates an `App` instance
2. registers `app.on_close` for the window close event
3. starts the Tk event loop with `app.mainloop()`

## Project Structure

```text
particle_collisions/
├── main.py
├── backend/
│   ├── colors.py
│   ├── config.py
│   ├── physics.py
│   └── simulation.py
└── frontend/
    └── gui/
        └── app.py
```

## Configuration

### `backend/config.py`

This module centralizes simulation constants.

| Name | Current Value | Role |
| --- | --- | --- |
| `WIDTH` | `800` | Canvas/window width |
| `HEIGHT` | `600` | Canvas/window height |
| `BLUE_PARTICLE_COUNT` | `500` | Initial number of blue particles |
| `WHITE_RADIUS` | `20` | Radius of the white special particle |
| `RED_RADIUS` | `12` | Radius of the red special particle |
| `BLUE_RADIUS` | `5` | Radius of blue particles |
| `RANDOM_VELOCITY_RANGE` | `10` | Random velocity component range |
| `FRAME_DELAY_MS` | `16` | Tk animation delay, roughly 60 FPS |
| `TRAIL_LENGTH` | `200` | Maximum stored trail points |
| `BG_COLOR` | `"#0a0a19"` | Canvas background |
| `BLUE_COLOR` | `"#024265"` | Blue particle color |
| `TRAIL_COLOR` | `"#6464ff"` | Default special-particle trail color |
| `RED_COLOR` | `"#ff4040"` | Red special-particle initial color |
| `RED_TRAIL_COLOR` | `"#ff9900"` | Red special-particle trail color |
| `TRAIL_FADE` | `True` | Toggles faded/tapered trails versus fixed-color trails |
| `GLOW_RINGS` | `4` | Number of glow rings |
| `GLOW_SPREAD` | `0.6` | Glow-radius multiplier |
| `GLOW_ENABLED` | `True` | Enables special-particle glow rendering |
| `EASE` | `0.15` | Color interpolation factor |
| `SPECIALS` | list of dicts | Special-particle fractional positions and visuals |
| `_MAX_RADIUS` | computed | Largest radius among blue and special particles |
| `CELL_SIZE` | `2 * _MAX_RADIUS` | Spatial-grid cell size |
| `REPEL_RADIUS` | `120` | Radius affected by right-click repulsion |
| `REPEL_STRENGTH` | `8.0` | Maximum velocity kick near the repulsion center |
| `HUD_COLOR` | `"#48bcfa"` | HUD text color |
| `HUD_FONT` | `("Consolas", 14, "bold")` | HUD text font |

### `SPECIALS`

`SPECIALS` defines the special particles using fractional positions:

```python
SPECIALS = [
    {"x": 0.50, "y": 0.50, "radius": WHITE_RADIUS, "color": "#ffffff", "trail": TRAIL_COLOR},
    {"x": 0.25, "y": 0.25, "radius": RED_RADIUS, "color": RED_COLOR, "trail": RED_TRAIL_COLOR},
]
```

The simulation converts each fractional position to pixels:

```python
int(WIDTH * s["x"])
int(HEIGHT * s["y"])
```

This keeps special-particle spawn positions proportional to the window size.

## Color Utilities

### `backend/colors.py`

This module contains pure helper functions for hex color conversion and interpolation.

### `hex_to_rgb(h)`

Input:

- `h`: hex color string such as `"#ff4040"` or `"ff4040"`

Output:

- `(r, g, b)` tuple of integers

Purpose:

- Converts Tk-compatible hex color strings into numeric RGB tuples.

### `rgb_to_hex(rgb)`

Input:

- `rgb`: tuple-like RGB values

Output:

- clamped hex color string in `"#rrggbb"` format

Purpose:

- Converts interpolated numeric colors back into Tk-compatible hex strings.

### `blend(c1, c2, t)`

Input:

- `c1`: first hex color
- `c2`: second hex color
- `t`: interpolation value where `0` gives `c1` and `1` gives `c2`

Output:

- blended hex color string

Used by:

- `Particle.move()` for smooth speed-based color transitions
- `App._render()` for faded trails and glow colors

## Physics Layer

### `backend/physics.py`

This module defines particle state and pairwise collision response.

## `Particle`

### Constructor

```python
Particle(x, y, radius, color, is_special=False)
```

Creates one particle.

### Attributes

| Attribute | Meaning |
| --- | --- |
| `x`, `y` | Physical position |
| `radius` | Particle radius |
| `color` | Current hex color |
| `is_special` | Whether the particle uses trail, glow, and speed-color behavior |
| `vx`, `vy` | Velocity components |
| `path` | Stored trail points for special particles |
| `trail_color` | Trail color used by the renderer |
| `pulse_phase` | Phase value for glow animation |
| `target_color` | Desired color for smooth color interpolation |

### `move(width, height)`

Updates particle state for one frame.

Step-by-step:

1. Add velocity to position.
2. Check left/right wall collisions.
3. Check top/bottom wall collisions.
4. Clamp the particle inside the window after wall collision.
5. For special particles:
   - append current position to `path`
   - trim `path` to `TRAIL_LENGTH`
   - compute speed magnitude
   - map speed to a target orange-red color
   - blend current color toward `target_color`
   - increment `pulse_phase`

## `resolve_collision(p1, p2)`

Resolves overlap and velocity exchange between two particles.

The function works for all particle combinations:

- blue vs blue
- blue vs special
- special vs special

### Collision Steps

1. Compute displacement:

```python
dx = p1.x - p2.x
dy = p1.y - p2.y
```

2. Compute distance and minimum non-overlap distance:

```python
distance = math.sqrt(dx**2 + dy**2)
min_dist = p1.radius + p2.radius
```

3. If `distance < min_dist`, particles overlap.

4. Compute the collision normal.

5. Push both particles apart by half the overlap.

6. Compute relative velocity along the normal.

7. If particles are moving toward each other, apply an elastic impulse.

Mass is approximated as:

```python
mass = radius**2
```

This makes larger particles behave as heavier particles.

## Simulation Layer

### `backend/simulation.py`

The `Simulation` class owns the particle list and advances physics.

## `Simulation`

### Attributes

| Attribute | Meaning |
| --- | --- |
| `particles` | List of all `Particle` instances |

### `__init__()`

Initializes the particle list and calls `_setup()`.

### `_setup()`

Rebuilds the simulation from scratch.

It:

1. clears `self.particles`
2. creates all special particles from `SPECIALS`
3. creates `BLUE_PARTICLE_COUNT` blue particles

Initial particle count:

```text
2 special particles + 500 blue particles = 502 particles
```

### `_make_blue()`

Creates one blue particle at a random position inside the window.

Uses:

- `BLUE_RADIUS`
- `BLUE_COLOR`
- random `x` between `50` and `WIDTH - 50`
- random `y` between `50` and `HEIGHT - 50`

### `_build_grid()`

Builds a spatial lookup dictionary:

```python
key = (int(p.x // CELL_SIZE), int(p.y // CELL_SIZE))
```

Output:

- dictionary mapping grid-cell coordinates to particles in that cell

Purpose:

- Reduces collision candidate checks compared with checking every pair directly.

### `tick()`

Advances the simulation by one frame.

Step-by-step:

1. Move all particles.
2. Build the spatial grid.
3. For each grid cell:
   - gather particles in the current cell and 8 neighboring cells
   - skip self-comparisons
   - skip pairs already handled using `checked`
   - call `resolve_collision(p1, p2)`

This separates movement from collision resolution more cleanly than moving and resolving pairwise in the same nested loop.

### `set_blue_count(target)`

Adjusts the number of non-special particles.

If `target` is larger than the current blue count:

- appends new blue particles

If `target` is smaller:

- removes blue particles from the end of the blue list

Used by:

- `App._on_count()`
- the CustomTkinter slider

### `spawn(x, y)`

Adds one blue particle at the provided canvas position.

Used by:

- `App._on_click()`
- left mouse clicks on the canvas

### `repel(x, y, radius=REPEL_RADIUS, strength=REPEL_STRENGTH)`

Applies an outward velocity kick to particles inside a circular area.

Step-by-step:

1. Compute squared distance from the click point to each particle.
2. Skip particles outside `radius`.
3. Skip particles exactly at the click center to avoid division by zero.
4. Compute linear falloff:

```python
falloff = 1 - d / radius
```

5. Add an outward velocity kick:

```python
p.vx += (dx / d) * kick
p.vy += (dy / d) * kick
```

Used by:

- `App._on_repel()`
- right-click, middle-click, and Control-click bindings

### `reset()`

Calls `_setup()` to restore the initial configured simulation state.

## GUI Layer

### `frontend/gui/app.py`

The `App` class owns the desktop window, canvas rendering, input bindings, and UI controls.

## `App`

Inherits from:

```python
ctk.CTk
```

### Attributes

| Attribute | Meaning |
| --- | --- |
| `sim` | `Simulation` instance |
| `_running` | Main-loop control flag |
| `_paused` | Pause/resume state |
| `_fps` | Smoothed frames-per-second estimate |
| `_last_t` | Previous frame timestamp from `time.perf_counter()` |
| `canvas` | Tk drawing surface |

### `__init__()`

Initializes the GUI.

Step-by-step:

1. initialize base `CTk`
2. set window title
3. disable resizing
4. create `Simulation`
5. build UI
6. initialize pause state
7. bind spacebar to `_toggle_pause()`
8. bind right-click variants to `_on_repel()`
9. initialize FPS tracking
10. start `_loop()`

### `_build_ui()`

Creates:

- `tk.Canvas`
- canvas click binding
- controls frame
- blue-count slider
- Reset button

The slider range is:

```python
0 to 2000
```

### `_loop()`

Main animation loop.

If `_running` is false, it exits.

If `_paused` is false:

- advances physics using `self.sim.tick()`

Then it:

- calls `_render()`
- updates smoothed FPS using `time.perf_counter()`
- schedules itself again with `self.after(FRAME_DELAY_MS, self._loop)`

### `_render()`

Redraws the entire frame.

For every particle:

1. Draw glow rings for special particles when `GLOW_ENABLED` is true.
2. Draw special-particle trail segments.
3. Draw the particle core as an oval.
4. Draw the HUD text.

Rendering details:

- glow uses `pulse_phase`
- when `TRAIL_FADE` is true, trail colors are blended from `BG_COLOR` to `p.trail_color`
- when `TRAIL_FADE` is true, trail width tapers from thin older segments to thicker newer segments
- when `TRAIL_FADE` is false, trails use fixed color and width
- particle bodies are drawn with `create_oval()`
- HUD includes blue-particle count, smoothed FPS, and `[PAUSED]` when paused

Current implementation note:

- the HUD overlay is inside the particle loop, so it is drawn repeatedly once per particle per frame
- behavior is visually acceptable but inefficient

### `_reset()`

Calls:

```python
self.sim.reset()
```

### `on_close()`

Stops the animation loop and destroys the window.

### `_on_click(event)`

Spawns one blue particle at:

```python
event.x, event.y
```

### `_toggle_pause(event=None)`

Toggles `_paused`.

Bound to:

```python
<space>
```

### `_on_count(value)`

Converts slider value to an integer and calls:

```python
self.sim.set_blue_count(int(value))
```

### `_on_repel(event)`

Calls:

```python
self.sim.repel(event.x, event.y)
```

Bound to:

- `<Button-2>`
- `<Button-3>`
- `<Control-Button-1>`

## How Components Work Together

High-level flow:

```text
main.py
  -> App
     -> Simulation
        -> Particle objects
        -> resolve_collision()
     -> tk.Canvas rendering
```

Frame flow:

```text
App._loop()
  -> if not paused: Simulation.tick()
       -> move all particles
       -> build spatial grid
       -> resolve nearby collisions
  -> App._render()
       -> clear canvas
       -> draw glow/trails/particles/counter
  -> schedule next frame
```

Interaction flow:

```text
Mouse click
  -> App._on_click()
  -> Simulation.spawn()
  -> new blue particle appears

Right-click / middle-click / Control-click
  -> App._on_repel()
  -> Simulation.repel()
  -> nearby particles receive outward velocity kicks

Slider movement
  -> App._on_count()
  -> Simulation.set_blue_count()
  -> blue particle count changes

Spacebar
  -> App._toggle_pause()
  -> Simulation.tick() pauses/resumes

Reset button
  -> App._reset()
  -> Simulation.reset()
  -> configured initial state is rebuilt
```

## Known Implementation Notes

- `TRAIL_FADE` is now wired into trail rendering.
- `TRAIL_COLOR` and `EASE` are imported in `frontend/gui/app.py` but not used directly there.
- `TRAIL_COLOR` and `EASE` are imported in `backend/simulation.py` but not used directly there.
- `CELL_SIZE` is computed from the largest configured radius, but should still be validated if speeds or collision behavior change substantially.
- The HUD overlay should ideally be drawn once after the particle loop.
