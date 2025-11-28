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
ITEM_SIZE = TILE_SIZE * 1.0


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
        self.obstacle_count = 0  

        
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
                surf.fill((58, 139, 58))  
                self.tile_images.append(surf)

    def start_music(self):
     
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

        try:
            with open("music_config.json", "r") as f:
                config = json.load(f)
                return config.get("1", "assets/backgrounds/audio/Aquatic Ambience.mp3")
        except Exception:
            return "assets/backgrounds/audio/Aquatic Ambience.mp3"

    def build_floor(self):
        floor_width = SCREEN_WIDTH * 2  
        self.floor_surface = pygame.Surface((floor_width, TILE_SIZE))

        for i in range(floor_width // TILE_SIZE + 1):
            tile_img = random.choice(self.tile_images)
            self.floor_surface.blit(tile_img, (i * TILE_SIZE, 0))

        self.floor_x = 0.0  

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
        bad_foods = ['hamburguer', 'refrigerante', 'sorvete']
        item_type = random.choice(bad_foods)
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = -TILE_SIZE
        item = Item((x, y), (TILE_SIZE, TILE_SIZE), item_type)
        item.fall_speed = random.uniform(5, 7) 
        item.is_falling = True
        item.is_bad_rain = True
        self.items.add(item)

    def spawn_ground_good_item(self, count=1):
        good_foods = ['maca', 'banana', 'alface']
        size = (int(TILE_SIZE * 1.5), int(TILE_SIZE * 1.5))
        for i in range(count):
            item_type = random.choice(good_foods)
            x = SCREEN_WIDTH + TILE_SIZE * 6 + (i * TILE_SIZE * 4) 
            y = self.floor_y - TILE_SIZE * random.randint(3, 5)
            item = Item((x, y), size, item_type)
            item.is_ground_item = True
            self.items.add(item)

    def spawn_obstacle(self):
        obstacle_types = ['pedra', 'cacto', 'hamburguer', 'refrigerante', 'sorvete']
        item_type = random.choice(obstacle_types)
        x = SCREEN_WIDTH + TILE_SIZE
        if item_type in ['pedra', 'cacto']:
            size = (int(TILE_SIZE * 2.5), int(TILE_SIZE * 2.5))
        else:
            size = (int(TILE_SIZE * 1.5), int(TILE_SIZE * 1.5))
        y = self.floor_y - size[1]
        obstacle = Item((x, y), size, item_type)
        obstacle.is_obstacle = True
        obstacle.is_deadly = item_type in ['pedra', 'cacto']
        self.obstacles.add(obstacle)
        self.obstacle_count += 1

       
        if self.obstacle_count % 7 == 0:
            self.spawn_ground_good_item(2)

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


       
        scroll_amount = self.scroll_speed + 4
        self.floor_x -= scroll_amount

        if self.floor_x <= -SCREEN_WIDTH:
            self.floor_x += SCREEN_WIDTH

       
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

        
        self.difficulty_timer = getattr(self, 'difficulty_timer', 0) + 1
        if self.difficulty_timer % 300 == 0:  
            self.scroll_speed = min(self.scroll_speed + 0.5, 15)  

       
        base_interval = max(30, 90 - int(self.scroll_speed * 5))

        self.obstacle_timer += 1
        if self.obstacle_timer >= self.obstacle_interval:
            self.spawn_obstacle()
            self.obstacle_timer = 0
            self.obstacle_interval = random.randint(base_interval, base_interval + 30)


        for item in self.items:
            if hasattr(item, 'is_falling') and item.is_falling:
                item.rect.y += item.fall_speed
                if item.rect.top > SCREEN_HEIGHT:
                    item.kill()
            elif hasattr(item, 'is_ground_item') and item.is_ground_item:
             
                item.rect.x -= self.scroll_speed + 4
                if item.rect.right < 0:
                    item.kill()

        for obstacle in self.obstacles:
            obstacle.rect.x -= self.scroll_speed + 4 
            if obstacle.rect.right < 0:
                obstacle.kill()

   
        self.check_item_collisions()
        self.check_obstacle_collisions()

    
        if player.good_items_collected >= 9:
            self.game_won = True
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
                if item.type in player.hints:
                    player.current_hint = player.hints[item.type]
                    player.hint_timer = pygame.time.get_ticks()
                player.fat_mode = True
                player.fat_mode_timer = pygame.time.get_ticks()
            else:
                player.good_items_collected += 1

    def check_obstacle_collisions(self):
        player = self.player.sprite
        collided_obstacles = pygame.sprite.spritecollide(player, self.obstacles, True)
        for obstacle in collided_obstacles:
            if hasattr(obstacle, 'is_deadly') and obstacle.is_deadly:
                self.game_over = True
                pygame.mixer.music.stop()
                return
            
            player.bad_items_collected += 1
            if obstacle.type in player.hints:
                player.current_hint = player.hints[obstacle.type]
                player.hint_timer = pygame.time.get_ticks()
            player.fat_mode = True
            player.fat_mode_timer = pygame.time.get_ticks()

    def draw(self, screen):

        if self.background_image:
            screen.blit(self.background_image, (self.background_x, 0))
            if self.background_x < 0:
                screen.blit(self.background_image, (self.background_x + self.background_width, 0))


        self.houses.draw(screen)

        
        screen.blit(self.floor_surface, (int(self.floor_x), self.floor_y))

      
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
            f"Comidas: {player.good_items_collected}/9"
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
                return "restart"
            if self.next_level_button_rect and self.next_level_button_rect.collidepoint(pos):
                return "next"
        elif self.game_over:
            if self.restart_to_level1_button_rect and self.restart_to_level1_button_rect.collidepoint(pos):
                return "restart_level1"
        return None
