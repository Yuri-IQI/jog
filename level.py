import pygame
import random
from player import Player
from item import Item

# --- Constantes Globais ---
SCREEN_WIDTH = 600
TILE_COLUMNS = 25
TILE_ROWS = 28
TILE_SIZE = SCREEN_WIDTH // TILE_COLUMNS
SCREEN_HEIGHT = TILE_ROWS * TILE_SIZE
ITEM_SIZE = TILE_SIZE * 0.8


class Level:
    def __init__(self, level_number=1):
        self.level_number = level_number
        self.game_won = False
        self.game_over = False

        # Imagens
        self.background_image = None
        self.victory_image = None
        self.gameover_image = None

        # Botões
        self.restart_button_rect = None
        self.next_level_button_rect = None
        self.restart_to_level1_button_rect = None

        # Layout e grupos
        self.layout = self.get_layout(level_number)
        self.tiles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        # Cria jogador
        spawn_pos = self.find_spawn_point()
        self.player = pygame.sprite.GroupSingle(Player(spawn_pos, size=(TILE_SIZE, TILE_SIZE)))

        self.load_images()
        self.build_tiles()
        self.place_items()
        self.start_music()

    # --- Layouts dos níveis ---
    def get_layout(self, level_number):
        if level_number == 1:
            return [
                "                         ",
                "                         ",
                "        XXXXX            ",
                "                         ",
                "   XXXXXX   XXXXXX       ",
                "                         ",
                "  X      XXXXXXXXXXXXXX  ",
                "                         ",
                "   XXXXXXXXX             ",
                "                         ",
                "       X                 ",
                "                         ",
                "   XXXXXXXXXXX           ",
                "                         ",
                "   X       XXXXX         ",
                "                         ",
                "   XXXXXXXXXXXXXXXX      ",
                "                         ",
                "   XXXXXXXXXX            ",
                "                         ",
                "   XXXXXXXXXXXXXXXXX     ",
                "                         ",
                "XXXXXXXX   X   XXXXXXXXXX",
                "                         ",
                "                         ",
                "            P            ",
                "XXXXXXXXXXXXXXXXXXXXXXXXX",
            ]
        else:
            # Level 2 – mais difícil
            return [
                "                         ",
                "      XXXX               ",
                "            XX           ",
                "   XXXX   XXXX           ",
                "                         ",
                " XXXXXXX       XXXX      ",
                "                         ",
                " XX     XXXXX            ",
                "                         ",
                "   XXXXXXXX   XXXX       ",
                "                         ",
                "  XX    XX               ",
                "                         ",
                " XXXXXXXX   XXXX         ",
                "                         ",
                "       XX        XX      ",
                "                         ",
                " XXXX    XXXXXXXX        ",
                "                         ",
                " XXXXXXXXXXXXXXXX        ",
                "                         ",
                " XXX   X   X   XXX       ",
                "                         ",
                "                         ",
                "           P             ",
                "XXXXXXXXXXXXXXXXXXXXXXXXX",
            ]

    # --- Setup ---
    def find_spawn_point(self):
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                if cell == 'P':
                    return (col_index * TILE_SIZE, row_index * TILE_SIZE)
        return (50, SCREEN_HEIGHT - TILE_SIZE * 4)

    # --- Carrega imagens corretas para cada nível ---
    def load_images(self):
        # Imagens de fundo e vitória específicas por nível
        bg_paths = {
            1: "assets/backgrounds/fase1.jpg",
            2: "assets/backgrounds/fase2.jpg"
        }

        victory_paths = {
            1: "assets/backgrounds/victory.png",
            2: "assets/backgrounds/victory.png"
        }

        gameover_path = "assets/backgrounds/gameover.jpg"

        # --- Fundo ---
        try:
            raw_bg = pygame.image.load(bg_paths[self.level_number]).convert()
            self.background_image = pygame.transform.scale(raw_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            color = (20, 20, 50) if self.level_number == 1 else (40, 0, 60)
            self.background_image.fill(color)

        # --- Imagem de vitória ---
        try:
            raw_victory = pygame.image.load(victory_paths[self.level_number]).convert_alpha()
            self.victory_image = pygame.transform.scale(raw_victory, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.victory_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.victory_image.fill((0, 100, 0))

        # --- Game Over ---
        try:
            raw_gameover = pygame.image.load(gameover_path).convert_alpha()
            self.gameover_image = pygame.transform.scale(raw_gameover, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.gameover_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.gameover_image.fill((100, 0, 0))

        # --- Tiles ---
        tile_paths = [
            "assets/tiles/Terreno 01.png",
            "assets/tiles/Terreno 02.png",
            "assets/tiles/Terreno 03.png",
        ]
        fallback_tile_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        fallback_tile_image.fill((100, 50, 0))
        self.tile_images = [fallback_tile_image]
        loaded_images = []
        for p in tile_paths:
            try:
                raw_image = pygame.image.load(p).convert_alpha()
                scaled_image = pygame.transform.scale(raw_image, (TILE_SIZE, TILE_SIZE))
                loaded_images.append(scaled_image)
            except Exception:
                pass
        if loaded_images:
            self.tile_images = loaded_images

    # --- Música por nível ---
    def start_music(self):
        music_paths = {
            1: "assets/backgrounds/audio/hong-kong-97.mp3",
            2: "assets/backgrounds/audio/Dreamscape.mp3"
        }

        if not pygame.mixer.get_init():
            pygame.mixer.init()
        try:
            pygame.mixer.music.load(music_paths.get(self.level_number, music_paths[1]))
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except Exception:
            pass

    # --- Construção ---
    def build_tiles(self):
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                if cell == "X":
                    tile = pygame.sprite.Sprite()
                    tile.image = random.choice(self.tile_images)
                    tile.rect = tile.image.get_rect(topleft=(col_index * TILE_SIZE, row_index * TILE_SIZE))
                    self.tiles.add(tile)

    def place_items(self):
        if self.level_number == 1:
            item_types = (['hamburguer'] * 2 + ['refrigerante'] * 2 +
                          ['sorvete'] * 1 + ['maca'] * 8 +
                          ['alface'] * 3 + ['banana'] * 3)
        else:
            # Level 2 tem mais itens ruins
            item_types = (['hamburguer'] * 4 + ['refrigerante'] * 8 +
                          ['sorvete'] * 4 + ['maca'] * 5 +
                          ['alface'] * 2 + ['banana'] * 2 +
                          ['sorvete'] * 8)

        potential_positions = []
        VERTICAL_OFFSET = 5
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == 'X' and y > 0 and self.layout[y - 1][x] == ' ':
                    pos_x = x * TILE_SIZE
                    pos_y = y * TILE_SIZE - ITEM_SIZE - VERTICAL_OFFSET
                    if y * TILE_SIZE > TILE_SIZE * 3:
                        potential_positions.append((pos_x, pos_y))
        if potential_positions:
            random.shuffle(potential_positions)
            num_items_to_place = min(32, int(len(potential_positions) * 0.5))
            selected_positions = potential_positions[:num_items_to_place]
            selected_items = random.choices(item_types, k=len(selected_positions))
            for pos, item_type in zip(selected_positions, selected_items):
                item = Item(pos, (TILE_SIZE, TILE_SIZE), item_type)
                self.items.add(item)

    # --- Reinicia o nível ---
    def restart_game(self):
        self.__init__(self.level_number)

    # --- Atualização principal ---
    def update(self):
        if self.game_won or self.game_over:
            return

        player = self.player.sprite
        player.update()

        keys = pygame.key.get_pressed()
        if player.died or keys[pygame.K_r]:
            self.restart_game()
            return

        # Escapou pelo topo
        if player.rect.bottom < 0:
            self.game_won = True
            pygame.mixer.music.stop()
            return

        player.rect.x += player.direction.x * player.speed
        self.collision_horizontal(player)

        if player.rect.left < 0:
            player.rect.left = 0
        elif player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        player.apply_gravity()
        self.collision_vertical(player)

        self.items.update()
        self.check_item_collisions()

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

    # --- Colisão com itens ---
    def check_item_collisions(self):
        player = self.player.sprite
        collided_items = pygame.sprite.spritecollide(player, self.items, True)
        for item in collided_items:
            player.collect_item(item)
            if self.level_number == 2 and item.type in ['sorvete', 'refrigerante', 'hamburguer']:
                player.bad_items_collected += 1
            if player.bad_items_collected >= 8:
                self.game_over = True
                pygame.mixer.music.stop()
                break

    # --- Renderização ---
    def draw(self, screen):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        self.tiles.draw(screen)
        self.items.draw(screen)
        self.player.draw(screen)

        player = self.player.sprite
        font = pygame.font.Font(None, 36)

        # --- Tela de Vitória ---
        if self.game_won:
            screen.blit(self.victory_image, (0, 0))
            button_width, button_height = 200, 60
            spacing = 30
            total_width = button_width * 2 + spacing
            start_x = (SCREEN_WIDTH - total_width) // 2
            button_y = SCREEN_HEIGHT - 150

            # Recomeçar
            self.restart_button_rect = pygame.Rect(start_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.restart_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.restart_button_rect, 3, border_radius=10)
            restart_text = font.render("Recomeçar", True, (255, 255, 255))
            screen.blit(restart_text, restart_text.get_rect(center=self.restart_button_rect.center))

            # --- NOVO: botão de próximo nível para 1 e 2 ---
            if self.level_number in [1, 2]:
                self.next_level_button_rect = pygame.Rect(
                    start_x + button_width + spacing, button_y, button_width, button_height
                )
                pygame.draw.rect(screen, (0, 0, 0, 180), self.next_level_button_rect, border_radius=10)
                pygame.draw.rect(screen, (255, 255, 255), self.next_level_button_rect, 3, border_radius=10)
                next_label = "Próximo Nível" if self.level_number == 1 else "Fase Final"
                next_text = font.render(next_label, True, (255, 255, 255))
                screen.blit(next_text, next_text.get_rect(center=self.next_level_button_rect.center))
            return

        # --- Tela de Game Over ---
        if self.game_over:
            screen.blit(self.gameover_image, (0, 0))
            button_width, button_height = 260, 60
            button_x = (SCREEN_WIDTH - button_width) // 2
            button_y = SCREEN_HEIGHT - 150

            self.restart_to_level1_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.restart_to_level1_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.restart_to_level1_button_rect, 3, border_radius=10)
            restart_text = font.render("Recomeçar do Nível 1", True, (255, 255, 255))
            screen.blit(restart_text, restart_text.get_rect(center=self.restart_to_level1_button_rect.center))
            return

        # --- HUD padrão ---
        info_texts = [
            f"Fase: {self.level_number}",
            f"Gravidade: {player.gravity:.2f} (Itens: {player.good_items_collected} G / {player.bad_items_collected} B)",
        ]
        font = pygame.font.Font(None, 32)
        line_height = 30
        padding = 10
        bg_color = (0, 0, 0, 150)
        text_color = (255, 255, 0)
        bg_width = 430
        bg_height = line_height * len(info_texts) + padding * 2
        info_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        pygame.draw.rect(info_surface, bg_color, (0, 0, bg_width, bg_height), border_radius=8)
        for i, text in enumerate(info_texts):
            text_surface = font.render(text, True, text_color)
            info_surface.blit(text_surface, (padding, padding + i * line_height))
        screen.blit(info_surface, (10, 10))

    # --- Clique nos botões ---
    def handle_click(self, pos):
        if self.game_won:
            if self.restart_button_rect and self.restart_button_rect.collidepoint(pos):
                return "restart"
            if self.next_level_button_rect and self.next_level_button_rect.collidepoint(pos):
                return "next"
        elif self.game_over:
            if self.restart_to_level1_button_rect and self.restart_to_level1_button_rect.collidepoint(pos):
                return "restart_level1"
        return None
