import pygame
import random
import json
from player import Player
from item import Item

SCREEN_WIDTH = 600
TILE_COLUMNS = 25
TILE_ROWS = 28
TILE_SIZE = SCREEN_WIDTH // TILE_COLUMNS
SCREEN_HEIGHT = TILE_ROWS * TILE_SIZE
ITEM_SIZE = TILE_SIZE * 0.8



class Shark(pygame.sprite.Sprite):
    def __init__(self, x, y, direction="right"):
        super().__init__()
        self.direction = direction
        self.speed = random.randint(3, 5)

        if self.direction == "right":
            img_path = "assets/item/Tubarao1.png"
        else:
            img_path = "assets/item/Tubarao2.png"

        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE * 3, TILE_SIZE * 2))
        self.rect = self.image.get_rect(midleft=(x, y))

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
            if self.rect.left > SCREEN_WIDTH:
                self.direction = "left"
                self.image = pygame.image.load("assets/item/Tubarao2.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (TILE_SIZE * 3, TILE_SIZE * 2))
        else:
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.direction = "right"
                self.image = pygame.image.load("assets/item/Tubarao1.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (TILE_SIZE * 3, TILE_SIZE * 2))


class WaterLevel:
    def __init__(self):
        self.level_number = 2
        self.game_over = False
        self.game_won = False

        self.items = pygame.sprite.Group()
        self.sharks = pygame.sprite.Group()

        self.background_image = None
        self.overlay = None
        self.victory_image = None
        self.gameover_image = None

        self.load_images()
        self.load_extra_images()

        spawn_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.player = pygame.sprite.GroupSingle(Player(spawn_pos, size=(TILE_SIZE, TILE_SIZE)))
        self.player.sprite.gravity = 0.2

       
        self.swim_frames = []
        self.load_swimming_sprites()
        self.current_swim_frame = 0
        self.last_swim_update = 0
        self.swim_frame_interval = 300  

        self.spawn_timer = 0
        self.shark_timer = 0

        self.coqueiro_positions = [
            (SCREEN_WIDTH - 100, 20),
            (50, 40),
            (SCREEN_WIDTH // 2 - 70, 10)
        ]

        for _ in range(3):
            self.spawn_shark()

        self.start_music()

    
    def load_swimming_sprites(self):
        try:
            frame1 = pygame.image.load("assets/player/Nadando 01.png").convert_alpha()
            frame2 = pygame.image.load("assets/player/Nadando 02.png").convert_alpha()
            frame1 = pygame.transform.scale(frame1, (TILE_SIZE * 1.4, TILE_SIZE * 1.4))
            frame2 = pygame.transform.scale(frame2, (TILE_SIZE * 1.4, TILE_SIZE * 1.4))
            self.swim_frames = [frame1, frame2]
        except:
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surf.fill((0, 200, 255))
            self.swim_frames = [surf, surf.copy()]

    
    def load_images(self):
        def load_scaled(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            except:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill((0, 150, 200))
                return surf

        self.tile_general = load_scaled("assets/tiles/Água GERAL 001.png")
        self.tile_corner = load_scaled("assets/tiles/Água CANTO 001.png")
        self.tile_h1 = load_scaled("assets/tiles/Água H 001.png")
        self.tile_h2 = load_scaled("assets/tiles/Água H 002.png")
        self.tile_v1 = load_scaled("assets/tiles/Água V 001.png")
        self.tile_v2 = load_scaled("assets/tiles/Água V 002.png")

        try:
            self.coqueiro = pygame.image.load("assets/tiles/Coqueiro.png").convert_alpha()
            self.coqueiro = pygame.transform.scale(self.coqueiro, (TILE_SIZE * 3, TILE_SIZE * 3))
        except:
            self.coqueiro = pygame.Surface((TILE_SIZE * 3, TILE_SIZE * 3))
            self.coqueiro.fill((0, 255, 0))

        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 80, 180, 80))


    def load_extra_images(self):
        try:
            raw_victory = pygame.image.load("assets/backgrounds/victory.png").convert_alpha()
            self.victory_image = pygame.transform.scale(raw_victory, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.victory_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.victory_image.fill((0, 100, 0))

        try:
            raw_gameover = pygame.image.load("assets/backgrounds/gameover.jpg").convert_alpha()
            self.gameover_image = pygame.transform.scale(raw_gameover, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.gameover_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.gameover_image.fill((100, 0, 0))

 
    def start_music(self):
      
        path = self.get_music_path()
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
            pass

    def get_music_path(self):
        """Carrega o caminho da música do arquivo de configuração"""
        try:
            with open("music_config.json", "r") as f:
                config = json.load(f)
                return config.get("2", "assets/backgrounds/audio/Dreamscape.mp3")
        except Exception:
            return "assets/backgrounds/audio/Dreamscape.mp3"

 
    def update(self):
        if self.game_over or self.game_won:
            return

        player = self.player.sprite
        player.update()

    
        keys = pygame.key.get_pressed()
        swim_speed = 3
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.rect.y -= swim_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.rect.y += swim_speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.rect.x -= swim_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.rect.x += swim_speed

        player.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

       
        now = pygame.time.get_ticks()
        if now - self.last_swim_update > self.swim_frame_interval:
            self.current_swim_frame = (self.current_swim_frame + 1) % len(self.swim_frames)
            self.last_swim_update = now
        player.image = self.swim_frames[self.current_swim_frame]

     
        self.spawn_timer += 1
        if self.spawn_timer > 60:
            self.spawn_item()
            self.spawn_timer = 0

        for item in self.items:
            item.rect.y += 2
            if item.rect.top > SCREEN_HEIGHT:
                item.kill()

       
        self.sharks.update()
        self.shark_timer += 1
        if self.shark_timer > 120:
            self.spawn_shark()
            self.shark_timer = 0

        self.check_item_collisions()
        self.check_shark_collisions()

    
        if self.player.sprite.good_items_collected >= 9:
            self.game_won = True
            pygame.mixer.music.stop()

 
    def spawn_item(self):
        item_types = (
            ['hamburguer'] * 6 + ['refrigerante'] * 3 + ['sorvete'] * 7 +
            ['maca'] * 4 + ['banana'] * 3 + ['alface'] * 2
        )
        item_type = random.choice(item_types)
        pos_x = random.randint(0, SCREEN_WIDTH - TILE_SIZE)
        pos_y = -ITEM_SIZE
        size = (int(TILE_SIZE * 1.8), int(TILE_SIZE * 1.8))  # Maior
        item = Item((pos_x, pos_y), size, item_type)
        self.items.add(item)

    def spawn_shark(self):
        direction = random.choice(["left", "right"])
        y = random.randint(TILE_SIZE * 5, SCREEN_HEIGHT - TILE_SIZE * 5)
        x = 0 if direction == "right" else SCREEN_WIDTH
        shark = Shark(x, y, direction)
        self.sharks.add(shark)

  
    def check_item_collisions(self):
        player = self.player.sprite
        collided_items = pygame.sprite.spritecollide(player, self.items, True)
        for item in collided_items:
            player.collect_item(item)
            if item.type in ['hamburguer', 'refrigerante', 'sorvete']:
                player.bad_items_collected += 1
                if item.type in player.hints:
                    player.current_hint = player.hints[item.type]
                    player.hint_timer = pygame.time.get_ticks()
            else:
                player.good_items_collected += 1
            if player.bad_items_collected >= 8:
                self.game_over = True
                pygame.mixer.music.stop()
                break

    def check_shark_collisions(self):
        player = self.player.sprite
        if pygame.sprite.spritecollideany(player, self.sharks):
            self.game_over = True
            pygame.mixer.music.stop()

    
    def draw(self, screen):
        for row in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for col in range(0, SCREEN_WIDTH, TILE_SIZE):
                if row == 0 and col == 0:
                    screen.blit(self.tile_corner, (col, row))
                elif row == 0 and col + TILE_SIZE >= SCREEN_WIDTH:
                    screen.blit(self.tile_h2, (col, row))
                elif row + TILE_SIZE >= SCREEN_HEIGHT and col == 0:
                    screen.blit(self.tile_v2, (col, row))
                elif row + TILE_SIZE >= SCREEN_HEIGHT and col + TILE_SIZE >= SCREEN_WIDTH:
                    screen.blit(self.tile_corner, (col, row))
                elif row == 0:
                    screen.blit(self.tile_h1, (col, row))
                elif row + TILE_SIZE >= SCREEN_HEIGHT:
                    screen.blit(self.tile_h2, (col, row))
                elif col == 0:
                    screen.blit(self.tile_v1, (col, row))
                elif col + TILE_SIZE >= SCREEN_WIDTH:
                    screen.blit(self.tile_v2, (col, row))
                else:
                    screen.blit(self.tile_general, (col, row))

   
        for pos in self.coqueiro_positions:
            screen.blit(self.coqueiro, pos)

        self.items.draw(screen)
        self.sharks.draw(screen)
        self.player.draw(screen)
        screen.blit(self.overlay, (0, 0))

    
        font = pygame.font.Font(None, 36)
        player = self.player.sprite

        if self.game_won:
            screen.blit(self.victory_image, (0, 0))
            button_width, button_height = 200, 60
            start_x = (SCREEN_WIDTH - (button_width * 2 + 30)) // 2
            button_y = SCREEN_HEIGHT - 150

            self.restart_button_rect = pygame.Rect(start_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.restart_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.restart_button_rect, 3, border_radius=10)
            restart_text = font.render("Recomeçar", True, (255, 255, 255))
            screen.blit(restart_text, restart_text.get_rect(center=self.restart_button_rect.center))

            self.next_level_button_rect = pygame.Rect(start_x + button_width + 30, button_y, button_width, button_height)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.next_level_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.next_level_button_rect, 3, border_radius=10)
            next_text = font.render("Próximo Nível", True, (255, 255, 255))
            screen.blit(next_text, next_text.get_rect(center=self.next_level_button_rect.center))
            return

        if self.game_over:
            screen.blit(self.gameover_image, (0, 0))
            button_width, button_height = 260, 60
            button_x = (SCREEN_WIDTH - button_width) // 2
            button_y = SCREEN_HEIGHT - 150
            self.restart_to_level1_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.restart_to_level1_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.restart_to_level1_button_rect, 3, border_radius=10)
            restart_text = font.render("Recomeçar", True, (255, 255, 255))
            screen.blit(restart_text, restart_text.get_rect(center=self.restart_to_level1_button_rect.center))
            return


        info_texts = [
            f"Fase: 2",
            f"Itens: {player.good_items_collected} bons / {player.bad_items_collected} ruins"
        ]
        font = pygame.font.Font(None, 32)
        line_height = 30
        padding = 10
        info_surface = pygame.Surface((400, 60), pygame.SRCALPHA)
        info_surface.fill((0, 0, 0, 150))
        for i, text in enumerate(info_texts):
            text_surface = font.render(text, True, (255, 255, 0))
            info_surface.blit(text_surface, (padding, padding + i * line_height))
        screen.blit(info_surface, (10, 10))

       
        if player.current_hint:
            hint_font = pygame.font.Font(None, 28)
            hint_text = hint_font.render(player.current_hint, True, (255, 255, 255))
            hint_width = hint_text.get_width() + 30
            hint_height = 50
            hint_x = (SCREEN_WIDTH - hint_width) // 2
            hint_y = SCREEN_HEIGHT - 120
            hint_bg = pygame.Surface((hint_width, hint_height), pygame.SRCALPHA)
            hint_bg.fill((255, 100, 100, 200))
            screen.blit(hint_bg, (hint_x, hint_y))
            pygame.draw.rect(screen, (255, 255, 255), (hint_x, hint_y, hint_width, hint_height), 3, border_radius=10)
            screen.blit(hint_text, (hint_x + 15, hint_y + 15))

    def handle_click(self, pos):
        if self.game_won:
            if self.restart_button_rect and self.restart_button_rect.collidepoint(pos):
                return "restart_level1"
            if self.next_level_button_rect and self.next_level_button_rect.collidepoint(pos):
                return "next"
        elif self.game_over:
            if self.restart_to_level1_button_rect and self.restart_to_level1_button_rect.collidepoint(pos):
                return "restart_level1"
        return None
