import pygame
import sys
from level import Level, SCREEN_WIDTH, SCREEN_HEIGHT
from level2 import WaterLevel
from level3 import Level3
from level4 import BossLevel 

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Based")
clock = pygame.time.Clock()

# --- Controle global de nível ---
# current_level_number = 1
# level = Level(current_level_number)

current_level_number = 4
level = BossLevel()



def load_level(level_number):
    if level_number == 1: 
        return Level()
    elif level_number == 2:
        return WaterLevel()
    elif level_number == 3:
        return Level3()
    elif level_number == 4:
        return BossLevel()
    else:
        return Level(1)


# --- Loop principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()


        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            action = level.handle_click(event.pos)

            if action == "restart":
                level = load_level(current_level_number)

            elif action == "next" or action == "next_level":
          
                current_level_number += 1
                level = load_level(current_level_number)

            elif action == "restart_level1":
          
                current_level_number = 1
                level = load_level(current_level_number)

            elif action == "quit_game":
               
                if pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()


    level.update()
    screen.fill((50, 50, 150))
    level.draw(screen)

    pygame.display.flip()
    clock.tick(60)
