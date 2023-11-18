import pygame
import random

class Particle:
    def __init__(self, radius, x, y, vx, vy, mass, color):
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.color = color

def inelastic_collision(particle1, particle2, restitution_coefficient, damping_factor, velocity_threshold):
    # Calculate relative velocity
    relative_vx = particle2.vx - particle1.vx
    relative_vy = particle2.vy - particle1.vy

    # Calculate relative distance
    dx = particle2.x - particle1.x
    dy = particle2.y - particle1.y
    distance = (dx ** 2 + dy ** 2) ** 0.5

    # Check if particles are colliding
    if distance < particle1.radius + particle2.radius:
        # Calculate normal vector
        nx = dx / distance
        ny = dy / distance

        # Calculate relative velocity in the normal direction
        relative_speed_normal = relative_vx * nx + relative_vy * ny

        # Calculate impulse for normal direction
        impulse_normal = (2 * (particle1.mass * particle2.mass) * relative_speed_normal) / ((particle1.mass + particle2.mass) * distance)

        # Update velocities with restitution, damping, and velocity threshold
        if abs(relative_speed_normal) > velocity_threshold:
            particle1.vx += (impulse_normal * particle2.mass * nx / particle1.mass) * restitution_coefficient - particle1.vx * damping_factor
            particle1.vy += (impulse_normal * particle2.mass * ny / particle1.mass) * restitution_coefficient - particle1.vy * damping_factor
            particle2.vx -= (impulse_normal * particle1.mass * nx / particle2.mass) * restitution_coefficient - particle2.vx * damping_factor
            particle2.vy -= (impulse_normal * particle1.mass * ny / particle2.mass) * restitution_coefficient - particle2.vy * damping_factor
        else:
            # If relative speed is below the threshold, reduce restitution (less bounciness)
            particle1.vx -= particle1.vx * damping_factor
            particle1.vy -= particle1.vy * damping_factor
            particle2.vx -= particle2.vx * damping_factor
            particle2.vy -= particle2.vy * damping_factor

        # Move particles away from each other to prevent overlap
        overlap = (particle1.radius + particle2.radius) - distance
        move_x = overlap * nx / 2
        move_y = overlap * ny / 2
        particle1.x -= move_x
        particle1.y -= move_y
        particle2.x += move_x
        particle2.y += move_y

def apply_air_resistance(particle, drag_coefficient):
    # Calculate the magnitude of velocity
    velocity_magnitude = (particle.vx ** 2 + particle.vy ** 2) ** 0.5

    # Calculate the drag force
    drag_force_x = -drag_coefficient * particle.vx
    drag_force_y = -drag_coefficient * particle.vy

    # Update the particle's velocity with the drag force
    particle.vx += drag_force_x / particle.mass
    particle.vy += drag_force_y / particle.mass

# Simulation parameters
space_size = 500
rate = 120  # Frames per second
dt = 1 / rate  # Time steps between frames
gravity = 200  # Adjust the strength of gravity
restitution_coefficient = 0.9  # Adjust the coefficient of restitution (elasticity)
damping_factor = 0.02  # Adjust the damping factor
velocity_threshold = 10  # Adjust the velocity threshold
drag_coefficient = 0.005  # Adjust the drag coefficient

# Create an empty array to store particles
particles = []

pygame.init()

screen = pygame.display.set_mode([space_size, space_size])

clock = pygame.time.Clock()

running = True
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

    pygame.display.flip()
    clock.tick(rate)

pygame.quit()
