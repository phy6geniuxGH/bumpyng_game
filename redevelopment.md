# Redevelopment Plan

Source: code audit of `main` at commit `aa8b937`. Item numbers are referenced in commits and pull requests (PRs).

Measured baseline (headless, backend only):

| Metric | Value |
|---|---|
| `Simulation.tick()` at N=502 | 4.4 ms |
| `Simulation.tick()` at N=2002 | 83.7 ms |
| HUD (heads-up display) redraw cost per frame, N=502 | 6.8 ms |
| Max particle speed after 300 ticks | 26.3 px/frame (blue diameter 10 px) |
| Max particle speed after 20 repels | 144.9 px/frame |
| Kinetic energy ratio after 300 ticks | 1.0000 (conserved) |

## Phase 1: Quick fixes

Effort: small. Impact: high.

| # | File | Issue | Fix |
|---|---|---|---|
| 1 | `frontend/gui/app.py:96-103` | HUD drawn inside the particle loop, O(N^2) per frame, N stacked text items | Dedent the HUD block out of the loop |
| 4 | `backend/simulation.py:68-69` | `list.remove()` in a loop, O(N^2) when shrinking via slider | Rebuild the list in one pass |
| 5 | `frontend/gui/app.py:70-77` | Outer glow ring equals background color (invisible); inner ring smaller than particle (hidden) | Remap ring radius and blend factor so every ring is visible |
| 6 | `backend/colors.py:6` | `int()` truncation stalls color easing (`#ff0000` to `#ff6464` stops at `#ff5e5e`) | Use `round()` |
| 9 | `frontend/gui/app.py:43-46` | Slider has no initial value; Reset does not sync slider | Set slider to `BLUE_PARTICLE_COUNT`, sync on Reset and on click-spawn |
| 11 | `backend/simulation.py:18-24` | Specials drawn first, blues cover them | Render specials last |
| 13 | `simulation.py:7`, `app.py:7-8` | Unused imports (`TRAIL_COLOR`, `EASE`) | Remove |
| 16 | `backend/physics.py:17, 39, 53` | Noise comment, duplicated `if self.is_special` | Merge blocks, remove comment |

Acceptance: app runs, HUD shows once, slider matches count, FPS (frames per second) improves at N=502.

## Phase 2: Physics robustness and tests

Effort: medium. Impact: stability and regression safety.

| # | File | Issue | Fix |
|---|---|---|---|
| 8 | `physics.py`, `simulation.py` | Tunneling (speed > diameter); repel has no speed cap | Add `MAX_SPEED` clamp and optional damping in config |
| 12 | `physics.py:71-74` | Positional correction splits overlap 50/50 regardless of mass | Weight by inverse mass |
| 14 | `physics.py:16, 45, 54` | Hardcoded `"#6464ff"`, `10.0`, `0.1` | Move to `config.py` |
| 15 | `physics.py:40-42` | `path.pop(0)` is O(n) | `collections.deque(maxlen=TRAIL_LENGTH)` |
| 20 | new `tests/` | No tests | pytest: momentum and energy conservation, wall bounce, grid vs brute-force collision parity, `set_blue_count` |

Acceptance: `pytest` passes; no speed above `MAX_SPEED`; energy ratio stays within tolerance.

## Phase 3: Performance

Effort: medium to large. Impact: usable at N=2000.

| # | File | Issue | Fix |
|---|---|---|---|
| 2 | `config.py:32-33`, `simulation.py:33-59` | `CELL_SIZE` set by the largest radius (40 px), too coarse for blues | Cell size from blue radius; handle specials separately, or vectorize with NumPy |
| 3 | `frontend/gui/app.py:66` | `canvas.delete("all")` then recreate every item each frame | Create items once, update with `coords()` and `itemconfig()` |
| 4b | `app.py:83-86` | `blend()` called per trail segment per frame | Precompute trail gradient palette |

Acceptance: `tick()` under 16 ms at N=2002; steady FPS near target.

## Phase 4: Architecture

Effort: medium. Impact: correctness independent of machine speed.

| # | File | Issue | Fix |
|---|---|---|---|
| 10 | `app.py:63`, `physics.py:22` | Physics in px/frame, no time step; slow frames slow the simulation | Fixed timestep (dt) with accumulator; velocities in px/s |
| 7 | `physics.py:44-50` | Speed-color formula overwrites configured special colors | Per-special color ramp in `SPECIALS` config |
| 17 | `app.py:108-110` | Pending `after` callback not cancelled on close | Store id, `after_cancel` |
| 18 | `config.py:41` | `Consolas` font is Windows-only | Use `TkFixedFont` or a fallback list |

## Hygiene (any phase)

| # | Issue | Fix |
|---|---|---|
| 19 | `requirements.txt` unpinned | Pin `customtkinter` version |
| 21 | README structure outdated | Done in `feature/fsdc-0001` |

## Tracking

| Phase | Branch | Status |
|---|---|---|
| Docs and plan | `feature/fsdc-0001` | In progress |
| Phase 1 | TBD | Not started |
| Phase 2 | TBD | Not started |
| Phase 3 | TBD | Not started |
| Phase 4 | TBD | Not started |
