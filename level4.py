import pygame
import random
import math
import json
from player import Player
from item import Item
from PIL import Image


SCREEN_WIDTH = 600
TILE_COLUMNS = 25
TILE_ROWS = 28
TILE_SIZE = SCREEN_WIDTH // TILE_COLUMNS
SCREEN_HEIGHT = TILE_ROWS * TILE_SIZE
ITEM_SIZE = TILE_SIZE * 0.8


class Cutscene:
    def __init__(self, dialogues):
        self.dialogues = dialogues  
        self.current_dialogue = 0
        self.finished = False
        self.font_large = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

    def update(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.current_dialogue += 1
            if self.current_dialogue >= len(self.dialogues):
                self.finished = True

    def draw(self, screen):
        if self.finished:
            return

      
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

       
        character, text = self.dialogues[self.current_dialogue]

        
        dialog_box_height = 150
        dialog_box_y = SCREEN_HEIGHT - dialog_box_height - 20
        dialog_box = pygame.Rect(20, dialog_box_y, SCREEN_WIDTH - 40, dialog_box_height)
        pygame.draw.rect(screen, (0, 0, 0, 220), dialog_box, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), dialog_box, 3, border_radius=10)

    
        name_surface = self.font_large.render(character, True, (255, 255, 0))
        screen.blit(name_surface, (40, dialog_box_y + 15))

       
        self.draw_text_wrapped(screen, text, (40, dialog_box_y + 55), SCREEN_WIDTH - 80)

        
        hint_text = self.font_small.render("Pressione qualquer tecla para continuar...", True, (100, 100, 100))
        screen.blit(hint_text, (SCREEN_WIDTH - hint_text.get_width() - 30, SCREEN_HEIGHT - 30))

    def draw_text_wrapped(self, screen, text, pos, max_width):
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if self.font_small.size(test_line)[0] > max_width:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(test_line)
                    current_line = []

        if current_line:
            lines.append(' '.join(current_line))

        y = pos[1]
        for line in lines:
            line_surface = self.font_small.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (pos[0], y))
            y += 30


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        try:
            image = pygame.image.load("assets/item/GarrafaDagua.png").convert_alpha()
            image2 = pygame.image.load("assets/item/Halteres.png").convert_alpha()
            self.image = pygame.transform.scale(image, (40, 40))
            self.image2 = pygame.transform.scale(image2, (40, 40))
        except Exception:
            self.image = pygame.Surface((40, 40))
            self.image2 = pygame.Surface((40, 40))
            self.image.fill((0, 200, 255))
            self.image2.fill((0, 200, 255))
        self.rect = self.image.get_rect(center=pos)
        self.rect = self.image2.get_rect(center=pos)
        self.velocity_y = 3

    def update(self):
        self.rect.y += self.velocity_y
        if self.rect.bottom > SCREEN_HEIGHT - TILE_SIZE:
            self.rect.bottom = SCREEN_HEIGHT - TILE_SIZE


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        try:
            self.image_right = pygame.image.load("assets/player/Boss.png").convert_alpha()
            self.image_left = pygame.image.load("assets/player/Boss2.png").convert_alpha()
            self.image_right = pygame.transform.scale(self.image_right, (120, 120))
            self.image_left = pygame.transform.scale(self.image_left, (120, 120))
            self.image = self.image_right
        except Exception:
            self.image = pygame.Surface((120, 120))
            self.image.fill((150, 0, 0))
            self.image_left = self.image
            self.image_right = self.image

        self.rect = self.image.get_rect(center=pos)
        self.health = 1800
        self.max_health = 1800
        self.last_shot_time = 0
        self.shoot_interval = 1000
        self.direction_x = 1
        self.direction_y = 1
        self.speed_x = 3
        self.speed_y = 2
        self.rage_mode = False
        self.damage_counter = 0
        self.dead = False

        self.explosion_frames = []
        self.explosion_index = 0
        self.explosion_timer = 0
        self.explosion_duration = 80
        self.load_explosion_gif("assets/backgrounds/effects/boom-explosion.gif")

    def load_explosion_gif(self, path):
        try:
            gif = Image.open(path)
            for frame in range(gif.n_frames):
                gif.seek(frame)
                frame_surface = pygame.image.fromstring(
                    gif.convert("RGBA").tobytes(), gif.size, "RGBA"
                )
                frame_surface = pygame.transform.scale(frame_surface, (150, 150))
                self.explosion_frames.append(frame_surface)
        except Exception as e:
            print(f"Erro ao carregar GIF de explosão: {e}")
            surf = pygame.Surface((120, 120), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 120, 0), (60, 60), 50)
            self.explosion_frames = [surf] * 6

    def move(self):
        if self.dead:
            return
        self.rect.x += self.direction_x * self.speed_x
        self.rect.y += self.direction_y * self.speed_y

        if self.rect.right >= SCREEN_WIDTH - 50 or self.rect.left <= 50:
            self.direction_x *= -1
            self.image = self.image_right if self.direction_x > 0 else self.image_left

        if self.rect.top <= 40 or self.rect.bottom >= SCREEN_HEIGHT - 120:
            self.direction_y *= -1

    def shoot(self, projectiles):
        if self.dead:
            return
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_interval:
            self.last_shot_time = now
            num_shots = random.randint(8, 12) if self.rage_mode else random.randint(5, 8)
            for _ in range(num_shots):
                bad_food = random.choice(['hamburguer', 'refrigerante', 'sorvete'])
                projectile = Item(
                    (self.rect.centerx, self.rect.centery),
                    (TILE_SIZE, TILE_SIZE),
                    bad_food
                )
                angle = random.uniform(0, 2 * math.pi)
                projectile.vx = math.cos(angle) * (6 if self.rage_mode else 5)
                projectile.vy = math.sin(angle) * (6 if self.rage_mode else 5)
                projectiles.add(projectile)

    def take_damage(self, amount):
        if self.dead:
            return None
        self.health = max(0, self.health - amount)
        self.damage_counter += 1
        drop_item = None
        if self.damage_counter >= 4:
            self.damage_counter = 0
            drop_item = PowerUp((self.rect.centerx, self.rect.bottom))
        if not self.rage_mode and self.health <= self.max_health / 2:
            self.activate_rage_mode()
        if self.health <= 0:
            self.dead = True
        return drop_item

    def activate_rage_mode(self):
        self.rage_mode = True
        self.speed_x = 7
        self.speed_y = 6
        self.shoot_interval = 800
        tinted = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        tinted.fill((255, 50, 50, 100))
        self.image.blit(tinted, (0, 0))
        self.rage_just_activated = True  

    def update_explosion(self):
        if not self.dead:
            return False
        now = pygame.time.get_ticks()
        if now - self.explosion_timer > 100:
            self.explosion_timer = now
            if self.explosion_index < len(self.explosion_frames):
                self.image = self.explosion_frames[self.explosion_index]
                self.explosion_index += 1
            else:
                return True
        return False



class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, direction=1, sound=None, strong=False):
        super().__init__()
        self.direction = direction  
        self.image = pygame.Surface((12 if strong else 8, 4))
        color = (255, 255, 0) if strong else (0, 255, 0)
        self.image.fill(color)
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(midleft=pos)
        self.speed = 10 * self.direction
        self.damage = 40 if strong else 20
        if sound:
            sound.play()

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


class BossLevel:
    def __init__(self):
        self.level_number = 4
        self.game_over = False
        self.game_won = False

        self.player = pygame.sprite.GroupSingle(Player((80, SCREEN_HEIGHT - 180), size=(TILE_SIZE, TILE_SIZE)))
        self.tiles = pygame.sprite.Group()
        self.boss = pygame.sprite.GroupSingle(Boss((SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300)))
        self.projectiles = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self.background_image = None
        self.victory_image = None
        self.gameover_image = None
        self.tile_images = []
        self.load_images()
        self.start_music()

        self.restart_button_rect = None
        self.quit_button_rect = None

        self.max_lives = 5
        self.player_lives = self.max_lives
        self.armor_hits = 0
        self.power_end_time = 0
        self.strong_laser = False

        self.last_direction = 1  

        try:
            self.laser_sound = pygame.mixer.Sound("assets/backgrounds/sounds/laser-fire.mp3")
            self.laser_sound.set_volume(0.4)
        except Exception:
            self.laser_sound = None

        self.build_floor()

        # Sistema de cutscene
        self.cutscene = Cutscene([
            ("Farmador de Aura", "Finalmente cheguei até você! Seu reinado de junk food acaba aqui!"),
            ("Pepsi", "Você ousa me desafiar? Vou te enterrar em hambúrgueres e refrigerantes!")
        ])
        self.cutscene_active = True
        self.rage_cutscene_shown = False

    def build_floor(self):
        floor_y = SCREEN_HEIGHT - TILE_SIZE
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            tile = pygame.sprite.Sprite()
            tile.image = random.choice(self.tile_images)
            tile.rect = tile.image.get_rect(topleft=(x, floor_y))
            self.tiles.add(tile)

    def load_images(self):
        try:
            bg = pygame.image.load("assets/backgrounds/fase4.jpg").convert()
            self.background_image = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background_image.fill((20, 0, 40))

        try:
            victory = pygame.image.load("assets/backgrounds/victory.png").convert_alpha()
            self.victory_image = pygame.transform.scale(victory, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.victory_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.victory_image.fill((0, 120, 0))

        try:
            over = pygame.image.load("assets/backgrounds/gameover.jpg").convert_alpha()
            self.gameover_image = pygame.transform.scale(over, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.gameover_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.gameover_image.fill((120, 0, 0))

        tile_paths = [
            "assets/tiles/Terreno 01.png",
            "assets/tiles/Terreno 02.png",
            "assets/tiles/Terreno 03.png",
        ]
        for path in tile_paths:
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                self.tile_images.append(img)
            except Exception:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill((80, 40, 0))
                self.tile_images.append(surf)

    def start_music(self):
        path = self.get_music_path()
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.6)
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
            pass

    def get_music_path(self):
        try:
            with open("music_config.json", "r") as f:
                config = json.load(f)
                return config.get("4", "assets/backgrounds/audio/TrilhaSonora4.mp3")
        except Exception:
            return "assets/backgrounds/audio/TrilhaSonora4.mp3"

    def update(self):
        if self.cutscene_active:
            return

        if self.game_over or self.game_won:
            return

        player = self.player.sprite
        boss = self.boss.sprite

     
        if hasattr(boss, 'rage_just_activated') and boss.rage_just_activated and not self.rage_cutscene_shown:
            boss.rage_just_activated = False
            self.rage_cutscene_shown = True
            self.cutscene = Cutscene([
                ("Pepsi", "Ainda não acabou!")
            ])
            self.cutscene_active = True
            return

        player.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.direction.x = 1
        else:
            player.direction.x = 0


        if player.direction.x != 0:
            self.last_direction = player.direction.x

        if keys[pygame.K_SPACE] and player.on_ground:
            player.jump()
        if keys[pygame.K_f] or keys[pygame.K_j]:
            self.shoot_laser()

        player.rect.x += player.direction.x * player.speed

        if player.rect.left < 0:
            player.rect.left = 0
        elif player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        player.apply_gravity()
        self.check_floor_collision(player)

        boss.move()
        boss.shoot(self.projectiles)

        for proj in self.projectiles:
            proj.rect.x += getattr(proj, "vx", 0)
            proj.rect.y += getattr(proj, "vy", 0)
        self.lasers.update()
        self.powerups.update()

        self.check_projectile_collisions()
        self.check_laser_hits()
        self.check_powerup_collect()

        if pygame.time.get_ticks() > self.power_end_time:
            self.armor_hits = 0
            self.strong_laser = False

        if boss.dead:
            finished = boss.update_explosion()
            if finished:
                self.game_won = True
                pygame.mixer.music.stop()
        if self.player_lives <= 0:
            self.game_over = True
            pygame.mixer.music.stop()

    def check_floor_collision(self, player):
        for tile in self.tiles:
            if player.rect.colliderect(tile.rect):
                player.rect.bottom = tile.rect.top
                player.direction.y = 0
                player.on_ground = True
                return
        player.on_ground = False


    def shoot_laser(self):
        player = self.player.sprite
        if len(self.lasers) < 3:
            direction = self.last_direction if hasattr(self, "last_direction") else 1
            start_pos = (
                player.rect.left if direction == -1 else player.rect.right,
                player.rect.centery
            )
            laser = Laser(start_pos, direction=direction, sound=self.laser_sound, strong=self.strong_laser)
            self.lasers.add(laser)

    def check_projectile_collisions(self):
        player = self.player.sprite
        collided = pygame.sprite.spritecollide(player, self.projectiles, True)
        for _ in collided:
            if self.armor_hits > 0:
                self.armor_hits -= 1
            else:
                self.player_lives -= 1
                if self.player_lives < 0:
                    self.player_lives = 0

    def check_laser_hits(self):
        boss = self.boss.sprite
        hits = pygame.sprite.spritecollide(boss, self.lasers, True)
        for _ in hits:
            dropped = boss.take_damage(40 if self.strong_laser else 20)
            if dropped:
                self.powerups.add(dropped)

    def check_powerup_collect(self):
        player = self.player.sprite
        collected = pygame.sprite.spritecollide(player, self.powerups, True)
        for _ in collected:
            self.armor_hits = 2
            self.strong_laser = True
            self.power_end_time = pygame.time.get_ticks() + 8000

    def draw(self, screen):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))

        self.tiles.draw(screen)
        self.player.draw(screen)
        self.projectiles.draw(screen)
        self.lasers.draw(screen)
        self.powerups.draw(screen)
        self.boss.draw(screen)

        font = pygame.font.Font(None, 36)
        boss = self.boss.sprite

    
        if self.cutscene_active:
            self.cutscene.draw(screen)
            return

        pygame.draw.rect(screen, (255, 0, 0), (10, 10, boss.health / boss.max_health * 580, 25))
        hp_text = font.render(f"Boss HP: {boss.health}", True, (255, 255, 255))
        screen.blit(hp_text, (15, 12))

        life_text = font.render(
            f"Vidas: {self.player_lives}/{self.max_lives} | Armadura: {self.armor_hits} | Laser Forte: {'Sim' if self.strong_laser else 'Não'}",
            True, (255, 255, 0)
        )
        screen.blit(life_text, (10, 45))

        if self.game_won:
            screen.blit(self.victory_image, (0, 0))
            self.draw_buttons(screen, font)
        elif self.game_over:
            screen.blit(self.gameover_image, (0, 0))
            self.draw_buttons(screen, font)

    def draw_buttons(self, screen, font):
        button_w, button_h = 260, 60
        spacing = 30
        total_w = button_w * 2 + spacing
        start_x = (SCREEN_WIDTH - total_w) // 2
        y = SCREEN_HEIGHT - 150

        self.restart_button_rect = pygame.Rect(start_x, y, button_w, button_h)
        self.quit_button_rect = pygame.Rect(start_x + button_w + spacing, y, button_w, button_h)

        pygame.draw.rect(screen, (0, 0, 0, 180), self.restart_button_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.restart_button_rect, 3, border_radius=10)
        screen.blit(font.render("Recomeçar", True, (255, 255, 255)), self.restart_button_rect.move(45, 15))

        pygame.draw.rect(screen, (0, 0, 0, 180), self.quit_button_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.quit_button_rect, 3, border_radius=10)
        screen.blit(font.render("Sair do Jogo", True, (255, 255, 255)), self.quit_button_rect.move(45, 15))

    def handle_click(self, pos):
        if self.cutscene_active:
            return None

        if self.restart_button_rect and self.restart_button_rect.collidepoint(pos):
            return "restart_level1"
        if self.quit_button_rect and self.quit_button_rect.collidepoint(pos):
            return "quit_game"
        return None

    def handle_cutscene_event(self, event):
        if self.cutscene_active and not self.cutscene.finished:
            self.cutscene.update(event)
            if self.cutscene.finished:
                self.cutscene_active = False
