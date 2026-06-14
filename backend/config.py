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

CELL_SIZE = SPECIALS[0]['radius']+SPECIALS[1]['radius']   # >= max(r1+r2). 15+12=27, round up.
