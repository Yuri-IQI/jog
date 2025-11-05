import pygame
import random
from player import Player
from item import Item

# --- Constantes Globais ---
SCREEN_WIDTH = 600
TILE_COLUMNS = 29
TILE_ROWS = 28
TILE_SIZE = SCREEN_WIDTH // TILE_COLUMNS
SCREEN_HEIGHT = TILE_ROWS * TILE_SIZE
ITEM_SIZE = TILE_SIZE * 0.8


class FinalLevel:
    def __init__(self):
        self.level_number = 3
        self.game_won = False
        self.game_over = False

        # Sprites
        self.tiles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.cannons = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        # Imagens
        self.background_image = None
        self.victory_image = None
        self.gameover_image = None
        self.tile_images = []
        self.cannon_image = None

        # Botões
        self.restart_to_level1_button_rect = None
        self.quit_button_rect = None

        # Layout e jogador
        self.layout = self.get_layout()
        spawn_pos = self.find_spawn_point()
        self.player = pygame.sprite.GroupSingle(Player(spawn_pos, size=(TILE_SIZE, TILE_SIZE)))

        self.load_images()
        self.build_tiles()
        self.place_items()
        self.place_cannons()
        self.start_music()

        # Controle de tempo dos tiros
        self.last_shot_time = 0
        self.shot_interval = 1500  # milissegundos

    # --- Layout ---
    def get_layout(self):
        return [
            "   X    XXXXXXX  XXXX x X   XXXXXX ",
            "    XX  X   X  x     x       X     ",
            "    X   X   XXXXX   XXXXX   XXXXX  ",
            " X  XXXXX x   x   XXXXX  X   x X   ",
            "   X       XXXXX   XXXXX   XXXXX  X",
            "   X   X    x   X      x X       X ",
            "   XXXXX   XXXXX   XXXXX   XXXXX   ",
            "       X       X       X       X   ",
            "XXXX   XXXXX x  XXXXX   XXXXX   XXX",
            "X  X    X   X  X   x   X  X X   XXX",
            "X   XXXXXXX   XXXXX   XXXXX   XXXXX",
            "X       X  X     X  X     X       X",
            "XXXXXX   XXXXX   XXXXX   XXXXX   X ",
            "X       X X   X   X       X       X",
            "X   XXXXX   XXXXX   XXXXX   XXXXXX ",
            "X       X       X       X         X",
            "XXXX   XXXXX   XXXXX   XXXXX   XXXX",
            "   X       X X      X  X     X   X ",
            "   XXXXX   XXXXX   XXXXX   XXXXX   ",
            "   X       X       X       X       ",
            "   XXXXX   XXXXX   XXXXX   XXXXX   ",
            "   X       X       X       X       ",
            "   XXXXX   XXXXX   XXXXX   XXXXX   ",
            "       P                       X   ",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        ]


    # --- Spawn do jogador ---
    def find_spawn_point(self):
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                if cell == 'P':
                    return (col_index * TILE_SIZE, row_index * TILE_SIZE)
        return (50, SCREEN_HEIGHT - TILE_SIZE * 4)

    # --- Carrega imagens ---
    def load_images(self):
        # Fundo
        try:
            raw_bg = pygame.image.load("assets/backgrounds/kim.jpeg").convert()
            self.background_image = pygame.transform.scale(raw_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background_image.fill((30, 0, 40))

        # Vitória
        try:
            raw_victory = pygame.image.load("assets/backgrounds/final_victory.jpg").convert_alpha()
            self.victory_image = pygame.transform.scale(raw_victory, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.victory_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.victory_image.fill((0, 100, 0))

        # Game Over
        try:
            raw_gameover = pygame.image.load("assets/backgrounds/final_gameover.jpg").convert_alpha()
            self.gameover_image = pygame.transform.scale(raw_gameover, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.gameover_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.gameover_image.fill((100, 0, 0))

        # Tiles
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

        # Canhões
        try:
            cannon_img = pygame.image.load("assets/item/canhao.png").convert_alpha()
            self.cannon_image = pygame.transform.scale(cannon_img, (TILE_SIZE, TILE_SIZE))
        except Exception:
            self.cannon_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.cannon_image.fill((200, 0, 0))

    # --- Música ---
    def start_music(self):
        music_path = "assets/backgrounds/Korea.mp3"
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.6)
        except Exception:
            pass

    # --- Tiles ---
    def build_tiles(self):
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                if cell == "X":
                    tile = pygame.sprite.Sprite()
                    tile.image = random.choice(self.tile_images)
                    tile.rect = tile.image.get_rect(topleft=(col_index * TILE_SIZE, row_index * TILE_SIZE))
                    self.tiles.add(tile)

    # --- Itens ---
    def place_items(self):
        item_types = (['maca'] * 5 + ['alface'] * 4 + ['banana'] * 4 + ['sorvete'] * 3 + ['hamburguer'] * 7 + ['refrigerante'] * 5)
        potential_positions = []
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == 'X' and y > 0 and self.layout[y - 1][x] == ' ':
                    pos_x = x * TILE_SIZE
                    pos_y = y * TILE_SIZE - ITEM_SIZE - 5
                    if y * TILE_SIZE > TILE_SIZE * 3:
                        potential_positions.append((pos_x, pos_y))
        if potential_positions:
            random.shuffle(potential_positions)
            selected_positions = potential_positions[:15]
            for pos in selected_positions:
                item_type = random.choice(item_types)
                item = Item(pos, (TILE_SIZE, TILE_SIZE), item_type)
                self.items.add(item)

    # --- Canhões ---
    def place_cannons(self):
        positions = [
            (50, 500), (150, 400), (250, 300),
            (350, 200), (450, 100),
            (500, 450), (400, 350), (200, 500),
            (550, 250), (100, 250)
        ]
        for pos in positions:
            cannon = pygame.sprite.Sprite()
            cannon.image = self.cannon_image
            cannon.rect = cannon.image.get_rect(topleft=pos)
            self.cannons.add(cannon)

    def shoot_from_cannons(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shot_interval:
            self.last_shot_time = now
            cannon = random.choice(self.cannons.sprites())
            bad_food = random.choice(['hamburguer', 'refrigerante', 'sorvete'])
            projectile = Item((cannon.rect.centerx, cannon.rect.centery),
                              (TILE_SIZE, TILE_SIZE), bad_food)
            projectile.direction = random.choice([-1, 1])
            projectile.speed = 6
            self.projectiles.add(projectile)

    def update_projectiles(self):
        for projectile in self.projectiles:
            projectile.rect.x += projectile.direction * projectile.speed
            if projectile.rect.right < 0 or projectile.rect.left > SCREEN_WIDTH:
                projectile.kill()

    # --- Atualização ---
    def update(self):
        if self.game_won or self.game_over:
            return

        player = self.player.sprite
        player.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.direction.x = -1
        elif keys[pygame.K_RIGHT]:
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

    # --- Colisões ---
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

    # --- Colisões com itens/projéteis ---
    def check_item_collisions(self):
        player = self.player.sprite
        for item in pygame.sprite.spritecollide(player, self.items, True):
            player.collect_item(item)

    def check_projectile_collisions(self):
        player = self.player.sprite
        collided = pygame.sprite.spritecollide(player, self.projectiles, True)
        for _ in collided:
            player.bad_items_collected += 1
            if player.bad_items_collected >= 3:
                self.game_over = True
                pygame.mixer.music.stop()
                break

    # --- Renderização ---
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

        # --- Vitória ---
        if self.game_won:
            screen.blit(self.victory_image, (0, 0))
            button_width, button_height = 260, 60
            spacing = 30
            total_width = button_width * 2 + spacing
            start_x = (SCREEN_WIDTH - total_width) // 2
            button_y = SCREEN_HEIGHT - 150

            # Recomeçar
            self.restart_to_level1_button_rect = pygame.Rect(start_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.restart_to_level1_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.restart_to_level1_button_rect, 3, border_radius=10)
            restart_text = font.render("Recomeçar", True, (255, 255, 255))
            screen.blit(restart_text, restart_text.get_rect(center=self.restart_to_level1_button_rect.center))

            # Fechar Jogo
            self.quit_button_rect = pygame.Rect(start_x + button_width + spacing, button_y, button_width, button_height)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.quit_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.quit_button_rect, 3, border_radius=10)
            quit_text = font.render("Fechar Jogo", True, (255, 255, 255))
            screen.blit(quit_text, quit_text.get_rect(center=self.quit_button_rect.center))
            return

        # --- Game Over ---
        if self.game_over:
            screen.blit(self.gameover_image, (0, 0))
            button_width, button_height = 280, 60
            button_x = (SCREEN_WIDTH - button_width) // 2
            button_y = SCREEN_HEIGHT - 150
            self.restart_to_level1_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.restart_to_level1_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.restart_to_level1_button_rect, 3, border_radius=10)
            restart_text = font.render("Recomeçar do Nível 1", True, (255, 255, 255))
            screen.blit(restart_text, restart_text.get_rect(center=self.restart_to_level1_button_rect.center))
            return

        # --- HUD ---
        info_text = f"Vidas: {max(0, 3 - player.bad_items_collected)} | Fase Final"
        hud_bg = pygame.Surface((260, 40), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 160))
        screen.blit(hud_bg, (5, 5))
        info_surface = font.render(info_text, True, (255, 255, 0))
        screen.blit(info_surface, (15, 15))

    # --- Clique nos botões ---
    def handle_click(self, pos):
        if self.game_won:
            if self.restart_to_level1_button_rect and self.restart_to_level1_button_rect.collidepoint(pos):
                return "restart_level1"
            if self.quit_button_rect and self.quit_button_rect.collidepoint(pos):
                return "quit_game"
        elif self.game_over and self.restart_to_level1_button_rect and self.restart_to_level1_button_rect.collidepoint(pos):
            return "restart_level1"
        return None
