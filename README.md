# Bumpyng Game

2D elastic particle collision simulation in Python with CustomTkinter.

Two special particles (white and red) with glowing bodies, faded trails, and speed-based color move among 500 blue particles. All particles bounce off walls and collide elastically.

## Features

- Elastic collisions with mass proportional to radius squared
- Spatial-grid collision search
- Special particles: faded trails, pulsing glow, speed-based color
- Click to spawn, right-click to repel, space to pause
- Slider for blue particle count (0 to 2000), Reset button
- HUD (heads-up display) with blue count, FPS (frames per second), pause state

## Requirements

- Python 3.13+
- `customtkinter`
- Tk support in your Python build (`python -m tkinter` should open a window)

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Controls

| Input | Action |
|---|---|
| Left click | Spawn a blue particle |
| Right click, middle click, Ctrl+click | Repel nearby particles |
| Space | Pause or resume |
| Slider | Set blue particle count |
| Reset | Reinitialize simulation |

## Project Structure

```text
bumpyng_game/
├── main.py                 entry point
├── backend/
│   ├── config.py           constants
│   ├── colors.py           color helpers
│   ├── physics.py          Particle, resolve_collision
│   └── simulation.py       Simulation, spatial grid, interactions
├── frontend/
│   └── gui/
│       └── app.py          window, renderer, input, main loop
├── docs/
│   └── documentation.md    technical documentation
├── redevelopment.md        audit findings and phased fix plan
└── github_rules.md         branching and pull request rules
```

## Configuration

Edit `backend/config.py`. See [docs/documentation.md](docs/documentation.md#configuration).

## Development

- Branch flow: `feature/fsdc-XXXX -> qa -> develop -> main`. See [github_rules.md](github_rules.md).
- Roadmap and known issues: [redevelopment.md](redevelopment.md).

## License

See [LICENSE](LICENSE).
