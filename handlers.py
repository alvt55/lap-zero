import pygame

# mainly for humans, not the agent 
# translating keystrokes into game logic inputs (e.g right arrow changes the heading of the car)
def get_controls():
    keys = pygame.key.get_pressed()

    steering = 0
    acceleration = 0

    if keys[pygame.K_LEFT]:
        steering = -1

    if keys[pygame.K_RIGHT]:
        steering = 1

    if keys[pygame.K_UP]:
        acceleration = 1

    if keys[pygame.K_DOWN]:
        acceleration = -1

    return steering, acceleration