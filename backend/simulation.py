import random
from backend.physics import Particle, resolve_collision
from backend.config import (
    WIDTH, HEIGHT, BLUE_PARTICLE_COUNT,
    WHITE_RADIUS, BLUE_RADIUS, BLUE_COLOR, 
    RED_RADIUS, RED_COLOR, RED_TRAIL_COLOR
)

class Simulation:
    def __init__(self):
        self.particles = []
        self._setup()

    def _setup(self):
        self.particles.clear()
        special = Particle(WIDTH // 2, HEIGHT // 2, WHITE_RADIUS, "#ffffff", is_special=True)
        self.particles.append(special)
        for _ in range(BLUE_PARTICLE_COUNT - 1):
            p = Particle(
                random.randint(50, WIDTH - 50),
                random.randint(50, HEIGHT - 50),
                BLUE_RADIUS,
                BLUE_COLOR
            )
            self.particles.append(p)
        red_p = Particle(WIDTH // 4, HEIGHT // 4, RED_RADIUS, RED_COLOR, is_special=True)
        red_p.trail_color = RED_TRAIL_COLOR
        self.particles.append(red_p)


    def tick(self):
        for i, p1 in enumerate(self.particles):
            p1.move(WIDTH, HEIGHT)
            for j in range(i + 1, len(self.particles)):
                resolve_collision(p1, self.particles[j])
    
    def reset(self):
        self._setup()