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


class Level3:
    def __init__(self):
        self.level_number = 3
        self.game_won = False
        self.game_over = False

 
        self.tiles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.cannons = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

      
        self.background_image = None
        self.victory_image = None
        self.gameover_image = None
        self.tile_images = []
        self.cannon_image = None

        self.restart_to_level1_button_rect = None
        self.quit_button_rect = None

      
        self.layout = self.get_layout()
        self.normalize_layout()  
        spawn_pos = self.find_spawn_point()
        self.player = pygame.sprite.GroupSingle(Player(spawn_pos, size=(TILE_SIZE, TILE_SIZE)))

        self.load_images()
        self.build_tiles()
        self.place_items()
        self.place_cannons()
        self.start_music()

      
        self.last_shot_time = 0
        self.shot_interval = 1500  
    
    
    def get_layout(self):
     return [
        "XXXXXXXXX          XXXXXX",
        "X   X   X     X   X     X",
        "X X X X X XXX X X X XXX X",
        "X X   X X   X   X     X X",
        "X X         XXXXX XXXXX X",
        "X   X X   X     X     X X",
        "XXX X           X XXX X X",
        "X   X   X X   X X   X   X",
        "X XXXXX X X X X XXX XXX X",
        "X     X   X X   X   X   X",
        "XXXXX             X XXX X",
        "X   X     X     X X   X X",
        "X X XXXXX XXX X X XXX X X",
        "X X X   X   X   X   X X X",
        "X X X X XXX X X XXX XXX X",
        "X   X X   X   X   X   X X",
        "XXX X XXX XXXXX X XXX X X",
        "X   X   X     X X   X   X",
        "X XX       XX X XXX XXXXX",
        "X X   X     X     X     X",
        "X X X XXXXX XXX   XXXXX X",
        "X   X           X       X",
        "XXX XXXXX XXX X XXXXX X X",
        "X         X   X         X",
        "X XXX X      XX XXXXXXX X",
        "X                       X",
        "X P  XXX XXX XXX XXX XX X",
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
     ]


    def normalize_layout(self):
        max_length = max(len(row) for row in self.layout)
        normalized = []
        for row in self.layout:
            if len(row) < max_length:
                row += " " * (max_length - len(row))
            elif len(row) > max_length:
                row = row[:max_length]
            normalized.append(row)
        self.layout = normalized


    def find_spawn_point(self):
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                if cell == 'P':
                    return (col_index * TILE_SIZE, row_index * TILE_SIZE)
        return (50, SCREEN_HEIGHT - TILE_SIZE * 4)

    def load_images(self):
       
        try:
            raw_bg = pygame.image.load("assets/backgrounds/fase3.jpg").convert()
            self.background_image = pygame.transform.scale(raw_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background_image.fill((30, 0, 40))

     
        try:
            raw_victory = pygame.image.load("assets/backgrounds/victory.png").convert_alpha()
            self.victory_image = pygame.transform.scale(raw_victory, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.victory_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.victory_image.fill((0, 100, 0))

      
        try:
            raw_gameover = pygame.image.load("assets/backgrounds/gameover.jpg").convert_alpha()
            self.gameover_image = pygame.transform.scale(raw_gameover, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.gameover_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.gameover_image.fill((100, 0, 0))

        tile_paths = [
            "assets/tiles/Terreno 01.png",
            "assets/tiles/Terreno 02.png",
            "assets/tiles/Terreno 03.png",
        ]
        loaded_tiles = []
        for path in tile_paths:
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                loaded_tiles.append(img)
            except Exception:
                pass
        if loaded_tiles:
            self.tile_images = loaded_tiles
        else:
            fallback = pygame.Surface((TILE_SIZE, TILE_SIZE))
            fallback.fill((80, 40, 0))
            self.tile_images = [fallback]

      
        try:
            cannon_img = pygame.image.load("assets/item/canhao.png").convert_alpha()
            self.cannon_image = pygame.transform.scale(cannon_img, (TILE_SIZE, TILE_SIZE))
        except Exception:
            self.cannon_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.cannon_image.fill((200, 0, 0))


    def start_music(self):
     
        music_path = self.get_music_path()
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.6)
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
            pass

    def get_music_path(self):
        try:
            with open("music_config.json", "r") as f:
                config = json.load(f)
                return config.get("3", "assets/backgrounds/audio/trilha sonora3.mp3")
        except Exception:
            return "assets/backgrounds/audio/trilha sonora3.mp3"


    def build_tiles(self):
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                if cell == "X":
                    tile = pygame.sprite.Sprite()
                    tile.image = random.choice(self.tile_images)
                    tile.rect = tile.image.get_rect(topleft=(col_index * TILE_SIZE, row_index * TILE_SIZE))
                    self.tiles.add(tile)

    def place_items(self):
        item_types = (['maca'] * 12 + ['alface'] * 10 + ['banana'] * 8 +
                      ['sorvete'] * 8 + ['hamburguer'] * 10 + ['refrigerante'] * 8)
        potential_positions = []
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if (
                    cell == 'X' and y > 0 and
                    x < len(self.layout[y - 1]) and
                    self.layout[y - 1][x] == ' '
                ):
                    pos_x = x * TILE_SIZE
                    pos_y = y * TILE_SIZE - ITEM_SIZE - 5
                    if y * TILE_SIZE > TILE_SIZE * 3:
                        potential_positions.append((pos_x, pos_y))
        if potential_positions:
            random.shuffle(potential_positions)
            selected_positions = potential_positions[:35]  
            size = (int(TILE_SIZE * 1.3), int(TILE_SIZE * 1.3))  
            for pos in selected_positions:
                item_type = random.choice(item_types)
                item = Item(pos, size, item_type)
                self.items.add(item)

    def place_cannons(self):
        positions = [
            (60, 520, 1), (180, 500, -1), (300, 520, 1),
            (420, 500, -1), (540, 520, 1),
            (80, 400, 1), (240, 380, -1), (360, 400, 1),
            (500, 380, -1), (140, 260, 1), (380, 240, -1),
            (50, 180, 1), (280, 160, -1), (480, 180, 1),
            (120, 100, -1), (340, 80, 1), (560, 100, -1),
            (200, 320, 1), (440, 300, -1), (320, 460, -1),
            (20, 450, 1), (580, 450, -1), (160, 200, 1),
            (400, 140, -1), (260, 280, 1), (520, 280, -1),
            (100, 340, 1), (460, 360, -1), (300, 60, 1)
        ]
        cannon_size = (int(TILE_SIZE * 1.5), int(TILE_SIZE * 1.5))  
        for pos_x, pos_y, direction in positions:
            cannon = pygame.sprite.Sprite()
            image = pygame.transform.scale(self.cannon_image, cannon_size)
            if direction == -1:
                image = pygame.transform.flip(image, True, False)
            cannon.image = image
            cannon.rect = cannon.image.get_rect(topleft=(pos_x, pos_y))
            cannon.direction = direction
            self.cannons.add(cannon)

    def shoot_from_cannons(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shot_interval:
            self.last_shot_time = now
            cannon = random.choice(self.cannons.sprites())
            bad_food = random.choice(['hamburguer', 'refrigerante', 'sorvete'])
            projectile = Item((cannon.rect.centerx, cannon.rect.centery),
                              (TILE_SIZE, TILE_SIZE), bad_food)
            projectile.direction = cannon.direction
            projectile.speed = 7
            self.projectiles.add(projectile)

    def update_projectiles(self):
        for projectile in self.projectiles:
            projectile.rect.x += projectile.direction * projectile.speed
            if projectile.rect.right < 0 or projectile.rect.left > SCREEN_WIDTH:
                projectile.kill()

    def update(self):
        if self.game_won or self.game_over:
            return
        player = self.player.sprite
        player.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.direction.x = 1
        else:
            player.direction.x = 0
        self.shoot_from_cannons()
        self.update_projectiles()
        player.rect.x += player.direction.x * player.speed
        self.collision_horizontal(player)
        player.apply_gravity()
        self.collision_vertical(player)
        self.items.update()
        self.check_item_collisions()
        self.check_projectile_collisions()
        if player.rect.bottom < 0:
            self.game_won = True
            pygame.mixer.music.stop()

    def collision_horizontal(self, player):
        for tile in self.tiles:
            if player.rect.colliderect(tile.rect):
                if player.direction.x > 0:
                    player.rect.right = tile.rect.left
                elif player.direction.x < 0:
                    player.rect.left = tile.rect.right

    def collision_vertical(self, player):
        player.on_ground = False
        for tile in self.tiles:
            if player.rect.colliderect(tile.rect):
                if player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0

    def check_item_collisions(self):
        player = self.player.sprite
        for item in pygame.sprite.spritecollide(player, self.items, True):
            player.collect_item(item)

    def check_projectile_collisions(self):
        player = self.player.sprite
        collided = pygame.sprite.spritecollide(player, self.projectiles, True)
        for projectile in collided:
            player.bad_items_collected += 1
            if projectile.type in player.hints:
                player.current_hint = player.hints[projectile.type]
                player.hint_timer = pygame.time.get_ticks()
            player.fat_mode = True
            player.fat_mode_timer = pygame.time.get_ticks()
            if player.bad_items_collected >= 3:
                self.game_over = True
                pygame.mixer.music.stop()
                break

    def draw(self, screen):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))

        self.tiles.draw(screen)
        self.items.draw(screen)
        self.cannons.draw(screen)
        self.projectiles.draw(screen)
        self.player.draw(screen)

        font = pygame.font.Font(None, 36)
        player = self.player.sprite

        if self.game_won:
            screen.blit(self.victory_image, (0, 0))
            button_width, button_height = 260, 60
            spacing = 30
            total_width = button_width * 2 + spacing
            start_x = (SCREEN_WIDTH - total_width) // 2
            button_y = SCREEN_HEIGHT - 150

        
            self.restart_to_level1_button_rect = pygame.Rect(start_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.restart_to_level1_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.restart_to_level1_button_rect, 3, border_radius=10)
            restart_text = font.render("Recomeçar", True, (255, 255, 255))
            screen.blit(restart_text, restart_text.get_rect(center=self.restart_to_level1_button_rect.center))

        
            self.next_level_button_rect = pygame.Rect(start_x + button_width + spacing, button_y, button_width, button_height)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.next_level_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.next_level_button_rect, 3, border_radius=10)
            next_text = font.render("Fase 4 (Boss)", True, (255, 255, 255))
            screen.blit(next_text, next_text.get_rect(center=self.next_level_button_rect.center))
            return

        if self.game_over:
            screen.blit(self.gameover_image, (0, 0))
            button_width, button_height = 280, 60
            button_x = (SCREEN_WIDTH - button_width) // 2
            button_y = SCREEN_HEIGHT - 150
            self.restart_to_level1_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.restart_to_level1_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.restart_to_level1_button_rect, 3, border_radius=10)
            restart_text = font.render("Recomeçar", True, (255, 255, 255))
            screen.blit(restart_text, restart_text.get_rect(center=self.restart_to_level1_button_rect.center))
            return

        info_text = f"Vidas: {max(0, 3 - player.bad_items_collected)} | Fase 3"
        hud_bg = pygame.Surface((260, 40), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 160))
        screen.blit(hud_bg, (5, 5))
        info_surface = font.render(info_text, True, (255, 255, 0))
        screen.blit(info_surface, (15, 15))

 
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
            if self.restart_to_level1_button_rect and self.restart_to_level1_button_rect.collidepoint(pos):
                return "restart_level1"
            if hasattr(self, 'next_level_button_rect') and self.next_level_button_rect.collidepoint(pos):
                return "next_level"  
        elif self.game_over and self.restart_to_level1_button_rect and self.restart_to_level1_button_rect.collidepoint(pos):
            return "restart_level1"
        return None

