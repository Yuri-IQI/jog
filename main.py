import pygame, sys
from level import Level

pygame.init()
screen = pygame.display.set_mode((960, 1080))
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()

level = Level()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update
    level.update()

    # Draw
    screen.fill((120, 200, 224))  # sky blue
    level.draw(screen)

    pygame.display.flip()
    clock.tick(60)