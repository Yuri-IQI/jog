import pygame
import random
from player import Player
from item import Item

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
TILE_COLUMNS = 25
TILE_ROWS = 16
TILE_SIZE = SCREEN_WIDTH // TILE_COLUMNS
ITEM_SIZE = TILE_SIZE * 0.8


class Level:
    def __init__(self):
        self.game_won = False
        self.layout = [
            "                         ",
            "                         ",
            "                         ",
            "            XXXX         ",
            "                         ",
            "                         ",
            "       X                 ",
            "                   XXX   ",
            "                   XXX   ",
            "                         ",
            "          XX             ",
            "                         ",
            "                         ",
            "   XXXX                  ",
            "                  XXX    ",
            "                   XX    ",
            "                    X    ",
            "                    XX   ",
            "          XXX            ",
            "                         ",
            "                         ",
            "    XXX                  ",
            "                   XXX   ",
            "        XXX    XXX       ",
            "                         ",
            "    P                    ",
            "XXXXXXXXXXXXXXXXXXXXXXXXX",
        ]

        self.tiles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        
        # Find spawn point coordinates from layout
        spawn_pos = self.find_spawn_point()
        self.player = pygame.sprite.GroupSingle(
            Player(spawn_pos, size=(TILE_SIZE, TILE_SIZE))
        )

        self.load_images()
        self.build_tiles()
        self.place_items()

    def find_spawn_point(self):
        """Find the spawn point marked with 'P' in the layout."""
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                if cell == 'P':
                    return (col_index * TILE_SIZE, row_index * TILE_SIZE)
        # Default spawn point if no 'P' is found
        return (50, SCREEN_HEIGHT - TILE_SIZE * 4)

    def load_images(self):
        """Preload and scale all images for tiles and items."""
        tile_paths = [
            "assets/tiles/Terreno 01.png",
            "assets/tiles/Terreno 02.png",
            "assets/tiles/Terreno 03.png",
        ]
        self.tile_images = [
            pygame.transform.scale(pygame.image.load(p).convert_alpha(), (TILE_SIZE, TILE_SIZE))
            for p in tile_paths
        ]

    def build_tiles(self):
        """Build level terrain tiles."""
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                if cell == "X":
                    tile = pygame.sprite.Sprite()
                    tile.image = random.choice(self.tile_images)
                    tile.rect = tile.image.get_rect(
                        topleft=(col_index * TILE_SIZE, row_index * TILE_SIZE)
                    )
                    self.tiles.add(tile)

    def place_items(self):
        """Place items near tiles and platforms."""
        item_types = (
            ['hamburguer'] * 6 +     # Increased from 2 to 6
            ['refrigerante'] * 6 +   # Increased from 2 to 6
            ['sorvete'] * 6 +        # Increased from 3 to 6
            ['maca'] * 8 +           # Increased from 5 to 8
            ['alface'] * 3 +         # Increased from 1 to 3
            ['banana'] * 3           # Increased from 1 to 3
        )

        near_tile_positions = []
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == ' ':
                    # Check if there's a tile nearby (above, below, left, right, and diagonals)
                    has_tile_nearby = False
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                        check_y = y + dy
                        check_x = x + dx
                        if (0 <= check_y < len(self.layout) and 
                            0 <= check_x < len(self.layout[0]) and 
                            self.layout[check_y][check_x] == 'X'):
                            has_tile_nearby = True
                            break
                    
                    if has_tile_nearby:
                        # Add multiple positions with different offsets for more variety
                        offsets = [(TILE_SIZE // 4, TILE_SIZE // 4),
                                 (TILE_SIZE // 2, TILE_SIZE // 4),
                                 (TILE_SIZE // 4, TILE_SIZE // 2)]
                        for offset_x, offset_y in offsets:
                            pos_x = x * TILE_SIZE + offset_x
                            pos_y = y * TILE_SIZE + offset_y
                            near_tile_positions.append((pos_x, pos_y))

        num_items = 32  # Increased from 12 to 32
        if near_tile_positions:
            selected_positions = random.sample(near_tile_positions, min(num_items, len(near_tile_positions)))
            selected_items = random.choices(item_types, k=len(selected_positions))

            for pos, item_type in zip(selected_positions, selected_items):
                item = Item(pos, (TILE_SIZE, TILE_SIZE), item_type)
                self.items.add(item)

    def restart_game(self):
        """Restart the game by reinitializing level components."""
        spawn_pos = self.find_spawn_point()
        self.player = pygame.sprite.GroupSingle(
            Player(spawn_pos, size=(TILE_SIZE, TILE_SIZE))
        )
        self.items = pygame.sprite.Group()
        self.place_items()

    def update(self):
        player = self.player.sprite
        player.update()

        # Check if player died from falling
        keys = pygame.key.get_pressed()
        if player.died or keys[pygame.K_r]:
            self.restart_game()
            return

        # Check if player escaped through the top
        if player.rect.bottom < 0:
            # Player has escaped! End the game with victory
            self.game_won = True
            return

        # Horizontal movement
        player.rect.x += player.direction.x * player.speed
        self.collision_horizontal(player)
        
        # Keep player within horizontal screen bounds
        if player.rect.left < 0:
            player.rect.left = 0
        elif player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        # Gravity and vertical movement
        player.apply_gravity()
        self.collision_vertical(player)

        # Items
        self.items.update()
        self.check_item_collisions()

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
        for item in self.items:
            if player.rect.colliderect(item.rect):
                item.kill()
                player.collect_item(item)

    def draw(self, screen):
        self.tiles.draw(screen)
        self.items.draw(screen)
        self.player.draw(screen)
        
        # Draw game state information
        font = pygame.font.Font(None, 36)
        player = self.player.sprite
        
        # Draw victory message if game is won
        if self.game_won:
            win_text = "You Escaped! Victory!"
            win_surface = font.render(win_text, True, (0, 255, 0))
            text_rect = win_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(win_surface, text_rect)
        
        if player.is_falling:
            fall_text = f"Fall Height: {int(player.current_fall_distance)} tiles"
            fall_surface = font.render(fall_text, True, (255, 0, 0))
            screen.blit(fall_surface, (10, 10))
            
        max_fall_text = f"Max Fall: {int(player.max_fall_distance)} tiles"
        max_fall_surface = font.render(max_fall_text, True, (255, 255, 255))
        screen.blit(max_fall_surface, (10, 50))