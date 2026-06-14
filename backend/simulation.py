import math
import random
from backend.physics import Particle, resolve_collision
from backend.config import (
    WIDTH, HEIGHT, BLUE_PARTICLE_COUNT,
    BLUE_RADIUS, BLUE_COLOR, 
    SPECIALS, TRAIL_COLOR, EASE,
    CELL_SIZE, REPEL_RADIUS, REPEL_STRENGTH,
)

class Simulation:
    def __init__(self):
        self.particles = []
        self._setup()

    def _setup(self):
        self.particles.clear()
        for s in SPECIALS:
            p = Particle(int(WIDTH * s["x"]), int(HEIGHT * s["y"]),
                         s["radius"], s["color"], is_special=True)
            p.trail_color = s["trail"]
            self.particles.append(p)
        for _ in range(BLUE_PARTICLE_COUNT):
            self.particles.append(self._make_blue())
    
    def _make_blue(self):
        return Particle(
            random.randint(50, WIDTH - 50),
            random.randint(50, HEIGHT - 50),
            BLUE_RADIUS, BLUE_COLOR
        )
    
    def _build_grid(self):
        grid = {}
        for p in self.particles:
            key = (int(p.x // CELL_SIZE), int(p.y // CELL_SIZE))
            grid.setdefault(key, []).append(p)
        return grid

    def tick(self):
        for p in self.particles:
            p.move(WIDTH, HEIGHT)            # move ALL first, then collide

        grid = self._build_grid()
        checked = set()                       # avoid resolving a pair twice
        for (cx, cy), cell in grid.items():
            candidates = []
            for dx in (-1, 0, 1):             # this cell + 8 neighbors
                for dy in (-1, 0, 1):
                    candidates.extend(grid.get((cx + dx, cy + dy), []))
            for p1 in cell:
                for p2 in candidates:
                    if p1 is p2:
                        continue
                    key = (id(p1), id(p2)) if id(p1) < id(p2) else (id(p2), id(p1))
                    if key in checked:
                        continue
                    checked.add(key)
                    resolve_collision(p1, p2)
    
    def set_blue_count(self, target):
        blues = [p for p in self.particles if not p.is_special]
        diff = target - len(blues)
        if diff > 0:
            for _ in range(diff):
                self.particles.append(self._make_blue())
        elif diff < 0:
            for p in blues[diff:]:            # trim from the end
                self.particles.remove(p)

    def spawn(self, x, y):
        self.particles.append(Particle(x, y, BLUE_RADIUS, BLUE_COLOR))

    def repel(self, x, y, radius=REPEL_RADIUS, strength=REPEL_STRENGTH):
        r2 = radius * radius
        for p in self.particles:
            dx = p.x - x
            dy = p.y - y
            d2 = dx*dx + dy*dy
            if d2 > r2 or d2 == 0:
                continue
            d = math.sqrt(d2)
            falloff = 1 - d / radius          # 1 at center -> 0 at edge
            kick = strength * falloff
            p.vx += (dx / d) * kick
            p.vy += (dy / d) * kick


    def reset(self):
        self._setup()