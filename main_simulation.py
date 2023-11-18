# main_simulation.py

import pygame
import random
from particle import Particle, inelastic_collision, apply_air_resistance
from math import atan2, cos, sin

# Simulation parameters
space_size = 500
rate = 120  # Frames per second
dt = 1 / rate  # Time steps between frames
gravity = 200  # Adjust the strength of gravity
restitution_coefficient = 0.8  # Adjust the coefficient of restitution (elasticity)
damping_factor = 0.02  # Adjust the damping factor
velocity_threshold = 10  # Adjust the velocity threshold
drag_coefficient = 0.005  # Adjust the drag coefficient
throwing_strength = 300  # Adjust the throwing strength

# Create an empty array to store particles
particles = []

pygame.init()

screen = pygame.display.set_mode([space_size, space_size])

clock = pygame.time.Clock()

running = True
selected_particle = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Generate a new particle with random properties
                new_particle = Particle(
                    radius=5,
                    x=random.randint(0, space_size),
                    y=random.randint(200, 350),
                    vx=-random.randint(50, 200),  # Random initial velocity
                    vy=0,
                    mass=1,
                    color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                )
                particles.append(new_particle)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check if a particle is clicked
                for particle in particles:
                    distance_to_particle = ((event.pos[0] - particle.x) ** 2 + (event.pos[1] - particle.y) ** 2) ** 0.5
                    if distance_to_particle < particle.radius:
                        selected_particle = particle
            elif event.button == 3:  # Right mouse button
                # Apply a pushing force to particles within the range of the mouse
                for particle in particles:
                    distance_to_mouse = ((event.pos[0] - particle.x) ** 2 + (event.pos[1] - particle.y) ** 2) ** 0.5
                    if distance_to_mouse < 50:  # Adjust the pushing range
                        angle_to_mouse = atan2(event.pos[1] - particle.y, event.pos[0] - particle.x)
                        particle.vx += throwing_strength * cos(angle_to_mouse) / particle.mass
                        particle.vy += throwing_strength * sin(angle_to_mouse) / particle.mass
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                selected_particle = None

    screen.fill((0, 0, 0))

    for particle in particles:
        pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), particle.radius)

        # Check if the particle is off the top of the screen
        if particle.y < 0:
            particles.remove(particle)

        # Bounce when touching the ground
        if particle.y + particle.radius > space_size:
            particle.vy = -particle.vy * restitution_coefficient
            particle.y = space_size - particle.radius  # Ensure particle is above the ground

        # Bounce when touching the horizontal edges
        if (particle.x - particle.radius) < 0:
            particle.vx = abs(particle.vx) * restitution_coefficient
            particle.x = particle.radius  # Ensure particle is within the screen
        elif (particle.x + particle.radius) > space_size:
            particle.vx = -abs(particle.vx) * restitution_coefficient
            particle.x = space_size - particle.radius  # Ensure particle is within the screen

        # Update particle position and velocity with gravity in the y-direction
        particle.y += particle.vy * dt
        particle.vy += gravity * dt  # Gravity effect

        # Update particle position with velocity in the x-direction
        particle.x += particle.vx * dt

        # Apply air resistance
        apply_air_resistance(particle, drag_coefficient)

    # Inelastic collisions between particles
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            inelastic_collision(particles[i], particles[j], restitution_coefficient, damping_factor, velocity_threshold)

    # If a particle is selected, move it with the mouse
    if selected_particle:
        selected_particle.x, selected_particle.y = pygame.mouse.get_pos()

    pygame.display.flip()
    clock.tick(rate)

pygame.quit()


