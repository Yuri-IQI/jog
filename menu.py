import pygame
import os
import json

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 672


class MainMenu:


    def __init__(self):
        self.current_screen = "main"
        self.selected_level = 1


        self.music_config = self.load_music_config()
        self.available_musics = self.scan_music_folder()
        self.current_music_selection = {1: 0, 2: 0, 3: 0, 4: 0}


        self.buttons = {}
        self.setup_buttons()


        self.menu_music_playing = False
        self.start_menu_music()

        # Player de músicas
        self.music_player_index = 0
        self.music_player_playing = False

    def scan_music_folder(self):
        music_folder = "assets/backgrounds/audio"
        musics = []

        try:
            for file in os.listdir(music_folder):
                if file.endswith('.mp3'):
                    musics.append(file)
        except Exception as e:
            print(f"Erro ao escanear musicas: {e}")
            musics = ["fase1.mp3", "Dreamscape.mp3", "trilha sonora3.mp3", "TrilhaSonora4.mp3"]

        return sorted(musics)

    def load_music_config(self):
        try:
            with open("music_config.json", "r") as f:
                return json.load(f)
        except:
            return {
                "1": "assets/backgrounds/audio/fase1.mp3",
                "2": "assets/backgrounds/audio/Dreamscape.mp3",
                "3": "assets/backgrounds/audio/trilha sonora3.mp3",
                "4": "assets/backgrounds/audio/TrilhaSonora4.mp3"
            }

    def save_music_config(self):
        try:
            with open("music_config.json", "w") as f:
                json.dump(self.music_config, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar config: {e}")

    def start_menu_music(self):
        if not self.menu_music_playing:
            try:
                pygame.mixer.music.load("assets/backgrounds/audio/Aquatic Ambience.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)
                self.menu_music_playing = True
            except:
                pass

    def stop_menu_music(self):
        if self.menu_music_playing:
            pygame.mixer.music.stop()
            self.menu_music_playing = False

    def setup_buttons(self):
    
        self.setup_main_buttons()
     
        self.setup_level_select_buttons()
      
        self.setup_music_config_buttons()
    
        self.setup_music_player_buttons()

    def setup_main_buttons(self):

        button_width = 350
        button_height = 60
        spacing = 20
        start_y = 150
        center_x = (SCREEN_WIDTH - button_width) // 2

        self.buttons['main'] = {
            'start': pygame.Rect(center_x, start_y, button_width, button_height),
            'level_select': pygame.Rect(center_x, start_y + (button_height + spacing), button_width, button_height),
            'music_config': pygame.Rect(center_x, start_y + (button_height + spacing) * 2, button_width, button_height),
            'music_player': pygame.Rect(center_x, start_y + (button_height + spacing) * 3, button_width, button_height),
            'credits': pygame.Rect(center_x, start_y + (button_height + spacing) * 4, button_width, button_height),
            'quit': pygame.Rect(center_x, start_y + (button_height + spacing) * 5, button_width, button_height)
        }

    def setup_level_select_buttons(self):
   
        button_size = 100
        spacing = 30
        start_x = (SCREEN_WIDTH - (button_size * 4 + spacing * 3)) // 2
        y = 250

        self.buttons['level_select'] = {
            'level1': pygame.Rect(start_x, y, button_size, button_size),
            'level2': pygame.Rect(start_x + (button_size + spacing), y, button_size, button_size),
            'level3': pygame.Rect(start_x + (button_size + spacing) * 2, y, button_size, button_size),
            'level4': pygame.Rect(start_x + (button_size + spacing) * 3, y, button_size, button_size),
            'back': pygame.Rect(SCREEN_WIDTH // 2 - 100, 450, 200, 50)
        }

    def setup_music_config_buttons(self):
     
        self.buttons['music_config'] = {
            'back': pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50),
            'save': pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 170, 200, 50)
        }


        for i in range(1, 5):
            y_pos = 150 + (i - 1) * 100
            self.buttons['music_config'][f'prev_{i}'] = pygame.Rect(50, y_pos, 40, 40)
            self.buttons['music_config'][f'next_{i}'] = pygame.Rect(SCREEN_WIDTH - 90, y_pos, 40, 40)

    def setup_music_player_buttons(self):
        center_x = SCREEN_WIDTH // 2
        self.buttons['music_player'] = {
            'prev': pygame.Rect(center_x - 180, 350, 80, 60),
            'play_pause': pygame.Rect(center_x - 50, 350, 100, 60),
            'next': pygame.Rect(center_x + 100, 350, 80, 60),
            'stop': pygame.Rect(center_x - 60, 430, 120, 50),
            'back': pygame.Rect(center_x - 100, SCREEN_HEIGHT - 80, 200, 50)
        }

    def handle_click(self, pos):

        if self.current_screen == "main":
            return self.handle_main_click(pos)
        elif self.current_screen == "level_select":
            return self.handle_level_select_click(pos)
        elif self.current_screen == "music_config":
            return self.handle_music_config_click(pos)
        elif self.current_screen == "music_player":
            return self.handle_music_player_click(pos)
        elif self.current_screen == "credits":
            return self.handle_credits_click(pos)
        return None

    def handle_main_click(self, pos):

        buttons = self.buttons['main']

        if buttons['start'].collidepoint(pos):
            self.stop_menu_music()
            return "start_game"
        elif buttons['level_select'].collidepoint(pos):
            self.current_screen = "level_select"
        elif buttons['music_config'].collidepoint(pos):
            self.current_screen = "music_config"
        elif buttons['music_player'].collidepoint(pos):
            self.current_screen = "music_player"
            self.stop_menu_music()
        elif buttons['credits'].collidepoint(pos):
            self.current_screen = "credits"
        elif buttons['quit'].collidepoint(pos):
            return "quit"
        return None

    def handle_level_select_click(self, pos):
   
        buttons = self.buttons['level_select']

        if buttons['level1'].collidepoint(pos):
            self.selected_level = 1
            self.stop_menu_music()
            return "start_level_1"
        elif buttons['level2'].collidepoint(pos):
            self.selected_level = 2
            self.stop_menu_music()
            return "start_level_2"
        elif buttons['level3'].collidepoint(pos):
            self.selected_level = 3
            self.stop_menu_music()
            return "start_level_3"
        elif buttons['level4'].collidepoint(pos):
            self.selected_level = 4
            self.stop_menu_music()
            return "start_level_4"
        elif buttons['back'].collidepoint(pos):
            self.current_screen = "main"
        return None

    def handle_music_config_click(self, pos):

        buttons = self.buttons['music_config']

    
        for i in range(1, 5):
            if buttons[f'prev_{i}'].collidepoint(pos):
                self.current_music_selection[i] = (self.current_music_selection[i] - 1) % len(self.available_musics)
                self.music_config[str(i)] = f"assets/backgrounds/audio/{self.available_musics[self.current_music_selection[i]]}"
            elif buttons[f'next_{i}'].collidepoint(pos):
                self.current_music_selection[i] = (self.current_music_selection[i] + 1) % len(self.available_musics)
                self.music_config[str(i)] = f"assets/backgrounds/audio/{self.available_musics[self.current_music_selection[i]]}"

        if buttons['save'].collidepoint(pos):
            self.save_music_config()
        elif buttons['back'].collidepoint(pos):
            self.current_screen = "main"
        return None

    def handle_music_player_click(self, pos):
        buttons = self.buttons['music_player']

        if buttons['prev'].collidepoint(pos):
            self.music_player_index = (self.music_player_index - 1) % len(self.available_musics)
            if self.music_player_playing:
                self.play_selected_music()
        elif buttons['play_pause'].collidepoint(pos):
            if self.music_player_playing:
                pygame.mixer.music.pause()
                self.music_player_playing = False
            else:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.unpause()
                else:
                    self.play_selected_music()
                self.music_player_playing = True
        elif buttons['next'].collidepoint(pos):
            self.music_player_index = (self.music_player_index + 1) % len(self.available_musics)
            if self.music_player_playing:
                self.play_selected_music()
        elif buttons['stop'].collidepoint(pos):
            pygame.mixer.music.stop()
            self.music_player_playing = False
        elif buttons['back'].collidepoint(pos):
            pygame.mixer.music.stop()
            self.music_player_playing = False
            self.current_screen = "main"
            self.start_menu_music()
        return None

    def play_selected_music(self):
        try:
            music_path = f"assets/backgrounds/audio/{self.available_musics[self.music_player_index]}"
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print(f"Erro ao tocar música: {e}")

    def handle_credits_click(self, pos):

        self.current_screen = "main"
        return None

    def draw(self, screen):
        """Desenha a tela atual"""
        if self.current_screen == "main":
            self.draw_main_menu(screen)
        elif self.current_screen == "level_select":
            self.draw_level_select(screen)
        elif self.current_screen == "music_config":
            self.draw_music_config(screen)
        elif self.current_screen == "music_player":
            self.draw_music_player(screen)
        elif self.current_screen == "credits":
            self.draw_credits(screen)

    def draw_main_menu(self, screen):
     
        for y in range(SCREEN_HEIGHT):
            color_factor = y / SCREEN_HEIGHT
            r = int(20 + (50 - 20) * color_factor)
            g = int(20 + (50 - 20) * color_factor)
            b = int(80 + (150 - 80) * color_factor)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

      
        title_font = pygame.font.Font(None, 90)
        title_text = title_font.render("BASED", True, (255, 255, 100))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)


        button_font = pygame.font.Font(None, 40)
        button_data = {
            'start': ('Iniciar Jogo', (0, 200, 0)),
            'level_select': ('Escolher Fase', (0, 100, 200)),
            'music_config': ('Configurar Música', (150, 0, 200)),
            'music_player': ('Escutar Músicas', (200, 100, 0)),
            'credits': ('Créditos', (200, 150, 0)),
            'quit': ('Sair', (200, 0, 0))
        }

        mouse_pos = pygame.mouse.get_pos()
        buttons = self.buttons['main']

        for button_name, (text, color) in button_data.items():
            rect = buttons[button_name]
            is_hovered = rect.collidepoint(mouse_pos)

            bg_color = color if not is_hovered else tuple(min(c + 40, 255) for c in color)
            pygame.draw.rect(screen, bg_color, rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 4 if is_hovered else 3, border_radius=10)

            text_surface = button_font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

    def draw_level_select(self, screen):

        screen.fill((30, 30, 60))

     
        title_font = pygame.font.Font(None, 70)
        title_text = title_font.render("ESCOLHER FASE", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

      
        level_font = pygame.font.Font(None, 50)
        level_names = ["Runner", "Água", "Labirinto", "Boss"]
        level_colors = [(100, 200, 100), (50, 150, 255), (200, 100, 200), (255, 100, 100)]

        mouse_pos = pygame.mouse.get_pos()
        buttons = self.buttons['level_select']

        for i, (name, color) in enumerate(zip(level_names, level_colors), 1):
            button_key = f'level{i}'
            rect = buttons[button_key]
            is_hovered = rect.collidepoint(mouse_pos)

            bg_color = color if not is_hovered else tuple(min(c + 30, 255) for c in color)
            pygame.draw.rect(screen, bg_color, rect, border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255), rect, 5 if is_hovered else 3, border_radius=15)

          
            num_text = level_font.render(str(i), True, (255, 255, 255))
            num_rect = num_text.get_rect(center=(rect.centerx, rect.centery - 15))
            screen.blit(num_text, num_rect)

            
            name_font = pygame.font.Font(None, 25)
            name_text = name_font.render(name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(rect.centerx, rect.centery + 25))
            screen.blit(name_text, name_rect)

 
        rect = buttons['back']
        is_hovered = rect.collidepoint(mouse_pos)
        bg_color = (100, 100, 100) if not is_hovered else (150, 150, 150)
        pygame.draw.rect(screen, bg_color, rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=10)

        back_font = pygame.font.Font(None, 35)
        back_text = back_font.render("Voltar", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=rect.center)
        screen.blit(back_text, back_rect)

    def draw_music_config(self, screen):
        screen.fill((40, 20, 60))

        title_font = pygame.font.Font(None, 60)
        title_text = title_font.render("CONFIGURAR MÚSICAS", True, (255, 255, 100))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

    
        hint_font = pygame.font.Font(None, 25)
        hint_text = hint_font.render("Use as setas para escolher a música de cada fase", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(hint_text, hint_rect)

   
        label_font = pygame.font.Font(None, 35)
        music_font = pygame.font.Font(None, 28)

        buttons = self.buttons['music_config']
        mouse_pos = pygame.mouse.get_pos()

        for i in range(1, 5):
            y_pos = 150 + (i - 1) * 100

          
            label_text = label_font.render(f"Fase {i}:", True, (255, 255, 255))
            screen.blit(label_text, (120, y_pos - 5))

        
            prev_rect = buttons[f'prev_{i}']
            prev_hovered = prev_rect.collidepoint(mouse_pos)
            pygame.draw.rect(screen, (150, 150, 150) if prev_hovered else (100, 100, 100), prev_rect, border_radius=5)
            arrow_font = pygame.font.Font(None, 40)
            arrow_text = arrow_font.render("<", True, (255, 255, 255))
            screen.blit(arrow_text, (prev_rect.centerx - 10, prev_rect.centery - 15))

           
            music_name = self.available_musics[self.current_music_selection[i]].replace('.mp3', '')
            music_text = music_font.render(music_name, True, (200, 255, 200))
            music_rect = music_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 15))

         
            bg_rect = pygame.Rect(music_rect.x - 10, music_rect.y - 5, music_rect.width + 20, music_rect.height + 10)
            pygame.draw.rect(screen, (50, 50, 80), bg_rect, border_radius=5)
            screen.blit(music_text, music_rect)

         
            next_rect = buttons[f'next_{i}']
            next_hovered = next_rect.collidepoint(mouse_pos)
            pygame.draw.rect(screen, (150, 150, 150) if next_hovered else (100, 100, 100), next_rect, border_radius=5)
            arrow_text = arrow_font.render(">", True, (255, 255, 255))
            screen.blit(arrow_text, (next_rect.centerx - 10, next_rect.centery - 15))

    
        for button_name, (text, color) in [('save', ('Salvar', (0, 150, 0))), ('back', ('Voltar', (100, 100, 100)))]:
            rect = buttons[button_name]
            is_hovered = rect.collidepoint(mouse_pos)
            bg_color = color if not is_hovered else tuple(min(c + 50, 255) for c in color)

            pygame.draw.rect(screen, bg_color, rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=10)

            button_font = pygame.font.Font(None, 35)
            button_text = button_font.render(text, True, (255, 255, 255))
            button_rect = button_text.get_rect(center=rect.center)
            screen.blit(button_text, button_rect)

    def draw_music_player(self, screen):
        screen.fill((30, 20, 50))

  
        title_font = pygame.font.Font(None, 60)
        title_text = title_font.render("PLAYER DE MÚSICAS", True, (255, 200, 100))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
        screen.blit(title_text, title_rect)

 
        current_music = self.available_musics[self.music_player_index].replace('.mp3', '')
        music_font = pygame.font.Font(None, 35)
        music_text = music_font.render(current_music, True, (255, 255, 255))
        music_rect = music_text.get_rect(center=(SCREEN_WIDTH // 2, 150))

      
        bg_rect = pygame.Rect(music_rect.x - 20, music_rect.y - 10, music_rect.width + 40, music_rect.height + 20)
        pygame.draw.rect(screen, (60, 40, 80), bg_rect, border_radius=10)
        pygame.draw.rect(screen, (150, 100, 200), bg_rect, 3, border_radius=10)
        screen.blit(music_text, music_rect)

      
        info_font = pygame.font.Font(None, 28)
        info_text = info_font.render(f"Música {self.music_player_index + 1} de {len(self.available_musics)}", True, (180, 180, 180))
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(info_text, info_rect)

    
        status_text = "Tocando..." if self.music_player_playing else "Pausado"
        status_color = (100, 255, 100) if self.music_player_playing else (255, 100, 100)
        status_surface = music_font.render(status_text, True, status_color)
        status_rect = status_surface.get_rect(center=(SCREEN_WIDTH // 2, 260))
        screen.blit(status_surface, status_rect)

     
        buttons = self.buttons['music_player']
        mouse_pos = pygame.mouse.get_pos()

       
        prev_rect = buttons['prev']
        prev_hovered = prev_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, (100, 100, 150) if prev_hovered else (70, 70, 120), prev_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 200, 255), prev_rect, 3, border_radius=10)
        prev_font = pygame.font.Font(None, 50)
        prev_text = prev_font.render("<", True, (255, 255, 255))
        screen.blit(prev_text, (prev_rect.centerx - 15, prev_rect.centery - 20))

        play_pause_rect = buttons['play_pause']
        play_pause_hovered = play_pause_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, (100, 200, 100) if play_pause_hovered else (70, 150, 70), play_pause_rect, border_radius=10)
        pygame.draw.rect(screen, (150, 255, 150), play_pause_rect, 3, border_radius=10)
        play_pause_symbol = "❚❚" if self.music_player_playing else ">"
        pp_font = pygame.font.Font(None, 45)
        pp_text = pp_font.render(play_pause_symbol, True, (255, 255, 255))
        screen.blit(pp_text, (play_pause_rect.centerx - 20, play_pause_rect.centery - 15))

        
        next_rect = buttons['next']
        next_hovered = next_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, (100, 100, 150) if next_hovered else (70, 70, 120), next_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 200, 255), next_rect, 3, border_radius=10)
        next_font = pygame.font.Font(None, 50)
        next_text = next_font.render(">", True, (255, 255, 255))
        screen.blit(next_text, (next_rect.centerx - 15, next_rect.centery - 20))

      
        stop_rect = buttons['stop']
        stop_hovered = stop_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, (200, 100, 100) if stop_hovered else (150, 70, 70), stop_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 150, 150), stop_rect, 3, border_radius=10)
        stop_font = pygame.font.Font(None, 35)
        stop_text = stop_font.render("STOP", True, (255, 255, 255))
        stop_text_rect = stop_text.get_rect(center=stop_rect.center)
        screen.blit(stop_text, stop_text_rect)

       
        back_rect = buttons['back']
        back_hovered = back_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, (150, 150, 150) if back_hovered else (100, 100, 100), back_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), back_rect, 3, border_radius=10)
        back_font = pygame.font.Font(None, 35)
        back_text = back_font.render("Voltar", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

  
        list_font = pygame.font.Font(None, 22)
        list_title = list_font.render("Músicas disponíveis:", True, (200, 200, 200))
        screen.blit(list_title, (50, 520))

       
        visible_start = max(0, self.music_player_index - 2)
        visible_end = min(len(self.available_musics), visible_start + 5)

        for i in range(visible_start, visible_end):
            y_pos = 545 + (i - visible_start) * 20
            music_name = self.available_musics[i].replace('.mp3', '')
            if len(music_name) > 40:
                music_name = music_name[:37] + "..."

            color = (255, 255, 100) if i == self.music_player_index else (150, 150, 150)
            list_text = list_font.render(f"{i + 1}. {music_name}", True, color)
            screen.blit(list_text, (60, y_pos))

    def draw_credits(self, screen):
        screen.fill((20, 20, 40))


        title_font = pygame.font.Font(None, 70)
        title_text = title_font.render("CRÉDITOS", True, (255, 255, 100))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title_text, title_rect)


        credits_font = pygame.font.Font(None, 35)
        credits_data = [
            ("Desenvolvido por:", (255, 255, 255), 180),
            ("Siensia de Notebuqui", (100, 255, 100), 220),
            ("", (0, 0, 0), 260),
            ("Programação: Rafael Menezes", (255, 255, 255), 300),
            ("Assets & Design: Manoel Macedo", (255, 255, 255), 420),
            ("Equipe Criativa: Murilo Pedral, Anthony Yuri", (255, 200, 100), 460),
            ("Product Owner: Franck Patrick ", (255, 100, 90), 500),
            ("Scrum Master: Rene Marinho ", (255, 100, 90), 540),
            ("", (0, 0, 0), 400),
        ]

        for text, color, y_pos in credits_data:
            if text:
                text_surface = credits_font.render(text, True, color)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                screen.blit(text_surface, text_rect)

       
        hint_font = pygame.font.Font(None, 30)
        hint_text = hint_font.render("Clique para voltar", True, (150, 150, 150))
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(hint_text, hint_rect)

    def get_level_music_path(self, level_number):

        return self.music_config.get(str(level_number), f"assets/backgrounds/audio/fase{level_number}.mp3")