import pygame
import sys
from final_level import FinalLevel
from level import Level, SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()

current_level_number = 1
level = Level(current_level_number)

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
                # Reinicia o nível atual
                level = Level(current_level_number)

            elif action == "next":
                # Vai para o próximo nível
                if current_level_number == 1:
                    current_level_number = 2
                    level = Level(current_level_number)
                elif current_level_number == 2:
                      current_level_number = 3
                      level = FinalLevel()


            elif action == "restart_level1":
                # 👇 CORREÇÃO: reinicia completamente o jogo no NÍVEL 1
                current_level_number = 1
                level = Level(1)

    level.update()
    screen.fill((50, 50, 150))
    level.draw(screen)

    pygame.display.flip()
    clock.tick(60)
