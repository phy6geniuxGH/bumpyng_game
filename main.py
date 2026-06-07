import pygame
import random
import math

# --- Configuration ---
WIDTH, WIDTH_SIZE = 800, 600
PARTICLE_COUNT = 500
WHITE_RADIUS = 15
BLUE_RADIUS = 7
WHITE_COLOR = (255, 255, 255)
BLUE_COLOR = (0, 100, 255)
TRAIL_COLOR = (100, 100, 255)
RANDOM_VELOCITY_RANGE = 10

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, WIDTH_SIZE))
pygame.display.set_caption("Stable Particle Collision")
clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y, radius, color, is_special=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.is_special = is_special
        
        # Random velocity
        self.vx = random.uniform(-RANDOM_VELOCITY_RANGE, RANDOM_VELOCITY_RANGE)
        self.vy = random.uniform(-RANDOM_VELOCITY_RANGE, RANDOM_VELOCITY_RANGE)

        # Trail logic for the special particle
        self.path = []

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Wall collisions (Bounce off edges and stay in bounds)
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -1
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -1

        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -1
        elif self.y + self.radius > WIDTH_SIZE: # Fixed height reference
            self.y = WIDTH_SIZE - self.radius
            self.vy *= -1

        if self.is_special:
            self.path.append((self.x, self.y))
            if len(self.path) > 200: # Slightly longer trail for better visuals
                self.path.pop(0)

            # --- NEW CODE START ---
            # Calculate speed (magnitude of velocity vector)
            speed = math.sqrt(self.vx**2 + self.vy**2)
            
            # Map speed to a color change (e.g., White -> Red as it gets faster)
            # We use 'min' and 'max' logic to ensure values stay between 0-255
            intensity = min(1.0, speed / 10.0) # Adjust the '10.0' to change sensitivity
            
            # Interpolate: if intensity is 0, color is (255, 255, 255)
            # If intensity is 1, color becomes (255, 100, 0) [Orange/Red]
            r = 255
            g = int(255 * (1 - intensity * 0.8)) # Green decreases as speed goes up
            b = int(255 * (1 - intensity))         # Blue decreases faster
            self.color = (r, g, b)
            # --- NEW CODE END ---


    def draw(self, surface):
        if self.is_special and len(self.path) > 2:
            # Draw the path line
            pygame.draw.lines(surface, TRAIL_COLOR, False, self.path, 2)
        
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

def resolve_collision(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = math.sqrt(dx**2 + dy**2)
    min_dist = p1.radius + p2.radius

    if distance < min_dist:
        # 1. Prevent Division by Zero
        # If particles are at the exact same spot, provide a default direction
        if distance == 0:
            nx, ny = 1, 0
            distance = 1
        else:
            nx = dx / distance
            ny = dy / distance

        # 2. Static Resolution (The "Anti-Glitch" Step)
        # Physically push the particles apart so they no longer overlap in the next frame.
        overlap = min_dist - distance
        p1.x += nx * (overlap / 2)
        p1.y += ny * (overlap / 2)
        p2.x -= nx * (overlap / 2)
        p2.y -= ny * (overlap / 2)

        # 3. Dynamic Resolution (The "Bounce" Step)
        # Only change velocity if they are moving TOWARDS each other.
        # This prevents the 'jitter'/acceleration loop.
        dot_product = (p1.vx - p2.vx) * nx + (p1.vy - p2.vy) * ny

        if dot_product < 0: # They are moving toward each other
            # Calculate impulse scalar based on mass (proportional to radius squared)
            # This makes the bigger white circle feel heavier/slower to move.
            m1 = p1.radius**2
            m2 = p2.radius**2
            total_m = m1 + m2

            # Standard 2D Elastic Collision formula simplified for this use-case:
            impulse = (2 * dot_product) / total_m
            
            p1.vx -= (impulse * m2) * nx
            p1.vy -= (impulse * m2) * ny
            p2.vx += (impulse * m1) * nx
            p2.vy += (impulse * m1) * ny

def main():
    # Setup constants again for clarity in logic
    WIDTH, HEIGHT = 800, 600
    particles = []

    # Create the White Particle
    white_p = Particle(WIDTH//2, HEIGHT//2, WHITE_RADIUS, WHITE_COLOR, True)
    particles.append(white_p)

    # Create Blue Particles
    for _ in range(PARTICLE_COUNT - 1):
        p = Particle(random.randint(50, WIDTH-50), 
                      random.randint(50, HEIGHT-50), 
                      BLUE_RADIUS, BLUE_COLOR)
        particles.append(p)

    running = True
    while running:
        screen.fill((10, 10, 25)) # Dark blue background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update and Draw logic
        for i in range(len(particles)):
            p1 = particles[i]
            p1.move()
            
            for j in range(i + 1, len(particles)):
                p2 = particles[j]
                resolve_collision(p1, p2)

            p1.draw(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
