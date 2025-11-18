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


class House(pygame.sprite.Sprite):
    def __init__(self, x, y, house_type='small'):
        super().__init__()
        if house_type == 'small':
            width, height = TILE_SIZE * 2, TILE_SIZE * 2
            color = (139, 69, 19)  
        else:
            width, height = TILE_SIZE * 3, TILE_SIZE * 3
            color = (160, 82, 45)  

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
 
        house_rect = pygame.Rect(0, height // 3, width, height * 2 // 3)
        pygame.draw.rect(self.image, color, house_rect)
 
        roof_points = [(0, height // 3), (width // 2, 0), (width, height // 3)]
        pygame.draw.polygon(self.image, (178, 34, 34), roof_points) 

        window_size = width // 4
        window_rect = pygame.Rect(width // 4, height // 2, window_size, window_size)
        pygame.draw.rect(self.image, (135, 206, 235), window_rect)  
      
        door_rect = pygame.Rect(width * 3 // 5, height * 2 // 3, width // 4, height // 3)
        pygame.draw.rect(self.image, (101, 67, 33), door_rect) 

        self.rect = self.image.get_rect(topleft=(x, y))
        self.original_x = x


class Level:
    def __init__(self):
        self.level_number = 1
        self.game_won = False
        self.game_over = False

        self.background_image = None
        self.victory_image = None
        self.gameover_image = None

        self.restart_button_rect = None
        self.next_level_button_rect = None
        self.restart_to_level1_button_rect = None

  
        self.scroll_speed = 3  

       
        self.background_x = 0
        self.background_width = SCREEN_WIDTH * 8 

       
        self.floor_y = SCREEN_HEIGHT - TILE_SIZE * 3
        self.tiles = pygame.sprite.Group()

      
        self.houses = pygame.sprite.Group()
        self.house_scroll_speed = self.scroll_speed * 0.3 

     
        self.items = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_interval = 60

     
        self.obstacles = pygame.sprite.Group()
        self.obstacle_timer = 0
        self.obstacle_interval = 90

        
        player_x = 100
        player_y = self.floor_y - TILE_SIZE
        self.player = pygame.sprite.GroupSingle(Player((player_x, player_y), size=(TILE_SIZE, TILE_SIZE)))

        self.load_images()
        self.build_floor()
        self.spawn_initial_houses()
        self.start_music()

    def load_images(self):
        try:
            raw_bg = pygame.image.load("assets/backgrounds/fase1.jpg").convert()
        
            self.background_image = pygame.transform.scale(raw_bg, (self.background_width, SCREEN_HEIGHT))
            print(f"Background carregado: {self.background_width}x{SCREEN_HEIGHT}")
        except Exception as e:
            print(f"Erro ao carregar background: {e}")
      
            self.background_image = pygame.Surface((self.background_width, SCREEN_HEIGHT))
            for y in range(SCREEN_HEIGHT):
                color_factor = y / SCREEN_HEIGHT
                r = int(135 + (200 - 135) * color_factor)
                g = int(206 + (220 - 206) * color_factor)
                b = int(235 + (255 - 235) * color_factor)
                pygame.draw.line(self.background_image, (r, g, b), (0, y), (self.background_width, y))

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
        self.tile_images = []
        for path in tile_paths:
            try:
                raw = pygame.image.load(path).convert_alpha()
                scaled = pygame.transform.scale(raw, (TILE_SIZE, TILE_SIZE))
                self.tile_images.append(scaled)
            except Exception:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill((34, 139, 34))  
                self.tile_images.append(surf)

    def start_music(self):
        # Carrega a música configurada pelo usuário
        path = self.get_music_path()
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
            pass

    def get_music_path(self):
        """Carrega o caminho da música do arquivo de configuração"""
        try:
            with open("music_config.json", "r") as f:
                config = json.load(f)
                return config.get("1", "assets/backgrounds/audio/Aquatic Ambience.mp3")
        except Exception:
            return "assets/backgrounds/audio/Aquatic Ambience.mp3"

    def build_floor(self):
      
        num_tiles = (SCREEN_WIDTH // TILE_SIZE) + 3
        for i in range(num_tiles):
            tile = pygame.sprite.Sprite()
            tile.image = random.choice(self.tile_images)
            tile.rect = tile.image.get_rect(topleft=(i * TILE_SIZE, self.floor_y))
            self.tiles.add(tile)

    def spawn_initial_houses(self):
  
        positions = [
            (100, self.floor_y - TILE_SIZE * 2, 'small'),
            (200, self.floor_y - TILE_SIZE * 3, 'big'),
            (350, self.floor_y - TILE_SIZE * 2, 'small'),
            (470, self.floor_y - TILE_SIZE * 3, 'big'),
            (600, self.floor_y - TILE_SIZE * 2, 'small'),
            (750, self.floor_y - TILE_SIZE * 3, 'big'),
            (900, self.floor_y - TILE_SIZE * 2, 'small'),
        ]
        for x, y, house_type in positions:
            house = House(x, y, house_type)
            self.houses.add(house)

    def spawn_house(self):
    
        house_type = random.choice(['small', 'big'])
        y = self.floor_y - (TILE_SIZE * 2 if house_type == 'small' else TILE_SIZE * 3)
        house = House(SCREEN_WIDTH + TILE_SIZE, y, house_type)
        self.houses.add(house)

    def spawn_good_item(self):
       
        good_foods = ['maca', 'banana', 'alface']
        item_type = random.choice(good_foods)
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = -TILE_SIZE
        item = Item((x, y), (TILE_SIZE, TILE_SIZE), item_type)
        item.fall_speed = random.uniform(4, 6)
        item.is_falling = True
        self.items.add(item)

    def spawn_bad_falling_item(self):
        """Spawna comida RUIM caindo do céu (chuva de junk food)"""
        bad_foods = ['hamburguer', 'refrigerante', 'sorvete']
        item_type = random.choice(bad_foods)
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = -TILE_SIZE
        item = Item((x, y), (TILE_SIZE, TILE_SIZE), item_type)
        item.fall_speed = random.uniform(5, 7) 
        item.is_falling = True
        item.is_bad_rain = True  
        self.items.add(item)

    def spawn_obstacle(self):
        bad_foods = ['hamburguer', 'refrigerante', 'sorvete']
        item_type = random.choice(bad_foods)
        x = SCREEN_WIDTH + TILE_SIZE
        y = random.choice([
            self.floor_y - TILE_SIZE,  
            self.floor_y - TILE_SIZE * 3,  
            self.floor_y - TILE_SIZE * 5   
        ])
        obstacle = Item((x, y), (TILE_SIZE, TILE_SIZE), item_type)
        obstacle.is_obstacle = True
        self.obstacles.add(obstacle)

    def update(self):
        if self.game_won or self.game_over:
            return

        player = self.player.sprite

       
        self.background_x -= 0.5 
     
        if self.background_x <= -(self.background_width - SCREEN_WIDTH):
            self.background_x = 0

     
        for house in self.houses:
            house.rect.x -= self.house_scroll_speed
            if house.rect.right < 0:
                house.kill()

        
        if random.randint(0, 100) < 5:  
            self.spawn_house()

 
        for tile in self.tiles:
            tile.rect.x -= self.scroll_speed
            if tile.rect.right < 0:
                max_x = max(t.rect.x for t in self.tiles)
                tile.rect.x = max_x + TILE_SIZE

       
        player.update()

      
        if player.on_ground and player.direction.x == 0:
            player.animation_state = 'run'

        player.rect.x += player.direction.x * player.speed

        if player.rect.left < 0:
            player.rect.left = 0
        elif player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        player.apply_gravity()
        self.check_floor_collision(player)

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
          
            if random.randint(0, 100) < 70:
                self.spawn_good_item()
            else:
                self.spawn_bad_falling_item()
            self.spawn_timer = 0
            self.spawn_interval = random.randint(40, 80)

   
        self.obstacle_timer += 1
        if self.obstacle_timer >= self.obstacle_interval:
            self.spawn_obstacle()
            self.obstacle_timer = 0
            self.obstacle_interval = random.randint(60, 120)

       
        for item in self.items:
            if hasattr(item, 'is_falling') and item.is_falling:
                item.rect.y += item.fall_speed
                # Remover se passar do chão
                if item.rect.top > SCREEN_HEIGHT:
                    item.kill()

        for obstacle in self.obstacles:
            obstacle.rect.x -= self.scroll_speed + 4 
            if obstacle.rect.right < 0:
                obstacle.kill()

   
        self.check_item_collisions()
        self.check_obstacle_collisions()

    
        if player.good_items_collected >= 10:
            self.game_won = True
            pygame.mixer.music.stop()

       
        if player.bad_items_collected >= 3:
            self.game_over = True
            pygame.mixer.music.stop()

    def check_floor_collision(self, player):
        if player.rect.bottom >= self.floor_y:
            player.rect.bottom = self.floor_y
            player.direction.y = 0
            player.on_ground = True
        else:
            player.on_ground = False

    def check_item_collisions(self):
        player = self.player.sprite
        collided_items = pygame.sprite.spritecollide(player, self.items, True)
        for item in collided_items:
            if hasattr(item, 'is_bad_rain') and item.is_bad_rain:
                player.bad_items_collected += 1
            else:
                player.good_items_collected += 1

    def check_obstacle_collisions(self):
        player = self.player.sprite
        collided_obstacles = pygame.sprite.spritecollide(player, self.obstacles, True)
        for obstacle in collided_obstacles:
            player.bad_items_collected += 1

    def draw(self, screen):

        if self.background_image:
            screen.blit(self.background_image, (self.background_x, 0))
            if self.background_x < 0:
                screen.blit(self.background_image, (self.background_x + self.background_width, 0))

  
        self.houses.draw(screen)

   
        self.tiles.draw(screen)

      
        self.items.draw(screen)
        self.obstacles.draw(screen)

      
        self.player.draw(screen)

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
            f"Fase: 1 - Runner",
            f"Boas: {player.good_items_collected}/10 | Ruins: {player.bad_items_collected}/3"
        ]
        font = pygame.font.Font(None, 32)
        line_height = 30
        padding = 10
        info_surface = pygame.Surface((450, 60), pygame.SRCALPHA)
        info_surface.fill((0, 0, 0, 150))
        for i, text in enumerate(info_texts):
            text_surface = font.render(text, True, (255, 255, 0))
            info_surface.blit(text_surface, (padding, padding + i * line_height))
        screen.blit(info_surface, (10, 10))

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
