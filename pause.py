import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 672


class PauseMenu:


    def __init__(self):
        self.paused = False
        self.buttons = {}
        self.setup_buttons()

    def setup_buttons(self):
    
        button_width = 300
        button_height = 60
        spacing = 20

   
        start_y = (SCREEN_HEIGHT - (button_height * 3 + spacing * 2)) // 2
        center_x = (SCREEN_WIDTH - button_width) // 2

       
        self.buttons['continue'] = pygame.Rect(
            center_x,
            start_y,
            button_width,
            button_height
        )

      
        self.buttons['main_menu'] = pygame.Rect(
            center_x,
            start_y + button_height + spacing,
            button_width,
            button_height
        )

       
        self.buttons['quit'] = pygame.Rect(
            center_x,
            start_y + (button_height + spacing) * 2,
            button_width,
            button_height
        )

    def toggle_pause(self):
        self.paused = not self.paused

        if self.paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def handle_key(self, event):
 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.toggle_pause()
            return True
        return False

    def handle_click(self, pos):
        if not self.paused:
            return None

        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                if button_name in ['main_menu', 'quit']:
                    pygame.mixer.music.unpause()
                elif button_name == 'continue':
                    self.toggle_pause()
                return button_name
        return None

    def draw(self, screen):
        if not self.paused:
            return

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title_font = pygame.font.Font(None, 80)
        title_text = title_font.render("PAUSA", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)


        button_font = pygame.font.Font(None, 40)

   
        button_data = {
            'continue': ('Continuar', (0, 200, 0)),
            'main_menu': ('Menu Principal', (0, 100, 200)),
            'quit': ('Sair do Jogo', (200, 0, 0))
        }

   
        mouse_pos = pygame.mouse.get_pos()

        for button_name, (text, color) in button_data.items():
            rect = self.buttons[button_name]

     
            is_hovered = rect.collidepoint(mouse_pos)

            
            bg_color = color if not is_hovered else tuple(min(c + 30, 255) for c in color)
            border_color = (255, 255, 255)

          
            pygame.draw.rect(screen, bg_color, rect, border_radius=10)

           
            border_width = 4 if is_hovered else 3
            pygame.draw.rect(screen, border_color, rect, border_width, border_radius=10)

            text_surface = button_font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

      
        hint_font = pygame.font.Font(None, 28)
        hint_text = hint_font.render("Pressione P para continuar", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(hint_text, hint_rect)
