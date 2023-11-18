class Particle:
    def __init__(self, radius, x, y, vx, vy, mass, color):
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.color = color

# Simulation parameters
space_size = 500
rate = 120  # Frames per second
dt = 1 / rate  # Time steps between frames
gravity = 200  # Adjust the strength of gravity

# Create an array of particles
particles = [
    Particle(radius=5, x=200, y=250, vx=-100, vy=0, mass=1, color=(255, 255, 255)),
    Particle(radius=5, x=300, y=250, vx=-150, vy=0, mass=1, color=(255, 0, 0)),
    Particle(radius=5, x=350, y=250, vx=-150, vy=0, mass=1, color=(0, 255, 0)),
    Particle(radius=5, x=400, y=250, vx=-150, vy=0, mass=1, color=(0, 0, 255))
]

import pygame
pygame.init()

screen = pygame.display.set_mode([space_size, space_size])

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for particle in particles:
        pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), particle.radius)

        for other_particle in particles:
            if particle != other_particle and abs(particle.x - other_particle.x) < (particle.radius + other_particle.radius):
                ux1, ux2 = particle.vx, other_particle.vx
                particle.vx = ux1 * (particle.mass - other_particle.mass) / (particle.mass + other_particle.mass) + 2 * ux2 * other_particle.mass / (
                            particle.mass + other_particle.mass)
                other_particle.vx = 2 * ux1 * particle.mass / (particle.mass + other_particle.mass) + ux2 * (
                            other_particle.mass - particle.mass) / (particle.mass + other_particle.mass)

        # Bounce when touching the ground
        if particle.y + particle.radius > space_size:
            particle.vy = -particle.vy

        # Bounce when touching the horizontal edges
        if (particle.x - particle.radius) < 0 or (particle.x + particle.radius > space_size):
            particle.vx = -particle.vx

        # Update particle position and velocity with gravity in the y-direction
        particle.y += particle.vy * dt
        particle.vy += gravity * dt  # Gravity effect

        # Update particle position with velocity in the x-direction
        particle.x += particle.vx * dt

    pygame.display.flip()
    clock.tick(rate)

pygame.quit()
