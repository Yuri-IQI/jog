import pygame
import random
from player import Player
from item import Item

# --- Constantes Globais ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TILE_SIZE = 40


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        try:
            image = pygame.image.load("assets/item/boss.png").convert_alpha()
            self.image = pygame.transform.scale(image, (120, 120))
        except Exception:
            self.image = pygame.Surface((120, 120))
            self.image.fill((150, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        self.health = 300
        self.max_health = 300
        self.last_shot_time = 0
        self.shoot_interval = 4000  # 4 segundos

    def shoot(self, projectiles):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_interval:
            self.last_shot_time = now
            bad_food = random.choice(['hamburguer', 'refrigerante', 'sorvete'])
            projectile = Item(
                (self.rect.centerx, self.rect.centery + 20),
                (TILE_SIZE, TILE_SIZE),
                bad_food
            )
            projectile.direction = -1  # sempre em direção ao jogador
            projectile.speed = 6
            projectiles.add(projectile)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def is_dead(self):
        return self.health <= 0


class Laser(pygame.sprite.Sprite):
    """Tiro do jogador (laser F)."""
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(midleft=pos)
        self.speed = 8

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class BossLevel:
    def __init__(self):
        self.level_number = 4
        self.game_over = False
        self.game_won = False

        # Sprites
        self.player = pygame.sprite.GroupSingle(Player((80, SCREEN_HEIGHT - 100), size=(TILE_SIZE, TILE_SIZE)))
        self.tiles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.boss = pygame.sprite.GroupSingle(Boss((SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150)))
        self.projectiles = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()

        # Fundo e música
        self.background_image = None
        self.victory_image = None
        self.gameover_image = None
        self.load_images()
        self.start_music()

        # Botões
        self.restart_button_rect = None
        self.quit_button_rect = None

        # Vidas do jogador
        self.max_lives = 5
        self.player_lives = self.max_lives

    # --- Imagens ---
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

    # --- Música ---
    def start_music(self):
        path = "assets/backgrounds/boss_theme.mp3"
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.6)
        except Exception:
            pass

    # --- Atualização ---
    def update(self):
        if self.game_over or self.game_won:
            return

        player = self.player.sprite
        boss = self.boss.sprite

        # Movimento do jogador
        player.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            player.direction.x = 1
        else:
            player.direction.x = 0
        if keys[pygame.K_f]:
            self.shoot_laser()

        # Atualizações gerais
        player.rect.x += player.direction.x * player.speed
        player.apply_gravity()
        self.projectiles.update()
        self.lasers.update()
        boss.shoot(self.projectiles)

        # Colisões
        self.check_projectile_collisions()
        self.check_laser_hits()

        # Fim de jogo
        if self.player_lives <= 0:
            self.game_over = True
            pygame.mixer.music.stop()
        if boss.is_dead():
            self.game_won = True
            pygame.mixer.music.stop()

    # --- Dispara laser ---
    def shoot_laser(self):
        player = self.player.sprite
        if len(self.lasers) < 3:  # limita spam
            laser = Laser((player.rect.right, player.rect.centery))
            self.lasers.add(laser)

    # --- Colisões ---
    def check_projectile_collisions(self):
        player = self.player.sprite
        collided = pygame.sprite.spritecollide(player, self.projectiles, True)
        for _ in collided:
            self.player_lives -= 1
            if self.player_lives < 0:
                self.player_lives = 0

    def check_laser_hits(self):
        boss = self.boss.sprite
        hits = pygame.sprite.spritecollide(boss, self.lasers, True)
        for _ in hits:
            boss.take_damage(20)

    # --- Renderização ---
    def draw(self, screen):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))

        self.player.draw(screen)
        self.boss.draw(screen)
        self.projectiles.draw(screen)
        self.lasers.draw(screen)

        font = pygame.font.Font(None, 36)
        boss = self.boss.sprite

        # --- Barra de Vida do Boss ---
        pygame.draw.rect(screen, (0, 0, 0, 150), (10, 10, 580, 25))
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, boss.health / boss.max_health * 580, 25))
        hp_text = font.render(f"Boss HP: {boss.health}", True, (255, 255, 255))
        screen.blit(hp_text, (15, 12))

        # --- Vidas do Jogador ---
        life_text = font.render(f"Vidas: {self.player_lives}/{self.max_lives}", True, (255, 255, 0))
        screen.blit(life_text, (10, 45))

        # --- Vitória ---
        if self.game_won:
            screen.blit(self.victory_image, (0, 0))
            button_width, button_height = 260, 60
            spacing = 30
            total_width = button_width * 2 + spacing
            start_x = (SCREEN_WIDTH - total_width) // 2
            y = SCREEN_HEIGHT - 150
            self.restart_button_rect = pygame.Rect(start_x, y, button_width, button_height)
            self.quit_button_rect = pygame.Rect(start_x + button_width + spacing, y, button_width, button_height)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.restart_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.restart_button_rect, 3, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.quit_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.quit_button_rect, 3, border_radius=10)
            screen.blit(font.render("Recomeçar", True, (255, 255, 255)),
                        self.restart_button_rect.move(40, 15))
            screen.blit(font.render("Sair do Jogo", True, (255, 255, 255)),
                        self.quit_button_rect.move(35, 15))
            return

        # --- Game Over ---
        if self.game_over:
            screen.blit(self.gameover_image, (0, 0))
            button_w, button_h = 280, 60
            x = (SCREEN_WIDTH - button_w) // 2
            y = SCREEN_HEIGHT - 150
            self.restart_button_rect = pygame.Rect(x, y, button_w, button_h)
            pygame.draw.rect(screen, (0, 0, 0, 180), self.restart_button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), self.restart_button_rect, 3, border_radius=10)
            screen.blit(font.render("Recomeçar do Nível 1", True, (255, 255, 255)),
                        self.restart_button_rect.move(20, 15))
            return

    # --- Clique nos botões ---
    def handle_click(self, pos):
        if self.game_won:
            if self.restart_button_rect and self.restart_button_rect.collidepoint(pos):
                return "restart_level1"
            if self.quit_button_rect and self.quit_button_rect.collidepoint(pos):
                return "quit_game"
        elif self.game_over and self.restart_button_rect and self.restart_button_rect.collidepoint(pos):
            return "restart_level1"
        return None
