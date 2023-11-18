# Particle 1
r1 = 8
x1 = 200
vx1 = -100
m1 = 15
c1 = (255, 255, 255)

# Particle 2
r2 = 5
x2 = 300
vx2 = -150
m2 = 1
c2 = (255, 0, 0)

# Simulation parameters
space_size = 500
rate = 60 # Frames per seconds
dt = 1/rate #Time steps between frames

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([space_size, space_size])


clock = pygame.time.Clock()

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((0, 0, 0))

    # Draw a solid white circle 1
    pygame.draw.circle(screen, c1, (x1, 250), r1)

    # Draw a solid red circle 2
    pygame.draw.circle(screen, c2, (x2, 250), r2)

    # Particle - particle collisions
    if (abs(x2 - x1) < (r1 + r2)) :
        ux1, ux2 = vx1, vx2
        vx1 = ux1 * (m1 - m2)/(m1 + m2) + 2 * ux2 * m2/(m1 + m2)
        vx2 = 2 * ux1 * m1/(m1 + m2) + ux2 * (m2 - m1)/(m1 + m2)

    # Bounce when touch the edge 1
    if ((x1 - r1) < 0 or (x1 + r1 > space_size)) :
        vx1 = - vx1

    # Bounce when touch the edge 2
    if ((x2 - r2) < 0 or (x2 + r2 > space_size)) :
        vx2 = - vx2

    # Flip the display (update the display)
    pygame.display.flip()

    # Dynamices for particle 1 
    x1 += vx1*dt
    # Dynamices for particle 2
    x2 += vx2*dt

    # Limit the frame rate to desire number of frames per second
    clock.tick(rate)

# Done! Time to quit.
pygame.quit()