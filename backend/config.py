WIDTH = 800
HEIGHT = 600
BLUE_PARTICLE_COUNT = 500
WHITE_RADIUS = 20
BLUE_RADIUS = 5
RANDOM_VELOCITY_RANGE = 10
FRAME_DELAY_MS = 16
TRAIL_LENGTH = 200
BG_COLOR = "#0a0a19"
BLUE_COLOR = "#024265"
TRAIL_COLOR = "#6464ff"

RED_RADIUS = 12
RED_COLOR = '#ff4040'
RED_TRAIL_COLOR = '#ff9900'

# --- visual effects ---
TRAIL_FADE = True
GLOW_RINGS = 4
GLOW_SPREAD = 0.6      # how far each ring grows past radius
GLOW_ENABLED = True
EASE = 0.15            # 0..1, higher = snappier

# fractions of WIDTH/HEIGHT so spawn scales with window
SPECIALS = [
    {"x": 0.50, "y": 0.50, "radius": WHITE_RADIUS, "color": "#ffffff", "trail": TRAIL_COLOR},
    {"x": 0.25, "y": 0.25, "radius": RED_RADIUS,   "color": RED_COLOR,  "trail": RED_TRAIL_COLOR},
]

# grid cell must be >= largest possible collision distance = sum of the two
# biggest radii in play. 2 * max radius is a safe upper bound for any pair.
_MAX_RADIUS = max([BLUE_RADIUS] + [s["radius"] for s in SPECIALS])
CELL_SIZE = 2 * _MAX_RADIUS

# --- interaction ---
REPEL_RADIUS = 120     # right-click push reaches this far (px)
REPEL_STRENGTH = 8.0   # velocity kick at click center, falls off with distance

# --- HUD ---
HUD_COLOR = "#48bcfa"
HUD_FONT = ("Consolas", 14, "bold")
