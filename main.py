import pygame
import sys
from level import Level, SCREEN_WIDTH, SCREEN_HEIGHT
from level2 import WaterLevel
from level3 import Level3
from level4 import BossLevel
from pause import PauseMenu
from menu import MainMenu

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BASED")
clock = pygame.time.Clock()


main_menu = MainMenu()
pause_menu = PauseMenu()


game_state = "menu"  
current_level_number = 1
level = None



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



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

       
        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                menu_action = main_menu.handle_click(event.pos)

                if menu_action == "start_game":
                    game_state = "playing"
                    current_level_number = 1
                    level = load_level(current_level_number)

                elif menu_action and menu_action.startswith("start_level_"):
                    game_state = "playing"
                    level_num = int(menu_action.split("_")[-1])
                    current_level_number = level_num
                    level = load_level(current_level_number)

                elif menu_action == "quit":
                    if pygame.mixer.get_init():
                        pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

      
        elif game_state == "playing":
         
            pause_menu.handle_key(event)
            if pause_menu.paused and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pause_action = pause_menu.handle_click(event.pos)

                if pause_action == "continue":
                    pass

                elif pause_action == "main_menu":
                    pause_menu.paused = False
                    game_state = "menu"
                    level = None
                    main_menu.start_menu_music()

                elif pause_action == "quit":
                    if pygame.mixer.get_init():
                        pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
            if not pause_menu.paused and level:
                if hasattr(level, 'handle_cutscene_event'):
                    level.handle_cutscene_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

    if game_state == "menu":
        main_menu.draw(screen)

    elif game_state == "playing" and level:
        if not pause_menu.paused:
            level.update()
        screen.fill((50, 50, 150))
        level.draw(screen)

        pause_menu.draw(screen)

    pygame.display.flip()
    clock.tick(60)
