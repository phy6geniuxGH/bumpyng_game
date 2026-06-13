import random
import math
from backend.config import RANDOM_VELOCITY_RANGE, TRAIL_LENGTH

class Particle:
    def __init__(self, x, y, radius, color, is_special=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.is_special= is_special
        self.vx = random.uniform(-RANDOM_VELOCITY_RANGE, RANDOM_VELOCITY_RANGE)
        self.vy = random.uniform(-RANDOM_VELOCITY_RANGE, RANDOM_VELOCITY_RANGE)
        self.path = []
        self.trail_color = "#6464ff"
    
    def move(self, width, height):
        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -1
        elif self.x + self.radius > width:
            self.x = width - self.radius 
            self.vx *= -1
        
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -1
        elif self.y + self.radius > height:
            self.y = height - self.radius 
            self.vy *= -1
        
        if self.is_special:
            self.path.append((self.x, self.y))
            if len(self.path) > TRAIL_LENGTH:
                self.path.pop(0)

            speed = math.sqrt(self.vx**2 + self.vy**2)
            intensity = min(1.0, speed /10.0)
            r = 255
            g = int(255 * (1 - intensity * 0.8))
            b = int(255 * (1 - intensity))
            self.color = "#%02x%02x%02x" % (r, g, b)

def resolve_collision(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = math.sqrt(dx**2 + dy**2)
    min_dist = p1.radius + p2.radius

    if distance < min_dist:
        if distance == 0:
            nx, ny = 1, 0
            distance = 1
        else:
            nx = dx/distance
            ny = dy/distance
        
        overlap = min_dist - distance
        p1.x += nx * (overlap / 2)
        p1.y += ny * (overlap / 2)
        p2.x -= nx * (overlap / 2)
        p2.y -= ny * (overlap / 2)

        dot_product = (p1.vx - p2.vx) * nx + (p1.vy - p2.vy) * ny

        if dot_product < 0:
            m1 = p1.radius**2
            m2 = p2.radius**2
            total_m = m1 + m2
            impulse = (2 * dot_product) / total_m
            p1.vx -= (impulse * m2) * nx
            p1.vy -= (impulse * m2) * ny
            p2.vx += (impulse * m1) * nx
            p2.vy += (impulse * m1) * ny