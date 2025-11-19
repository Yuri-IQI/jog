import pygame

# Constants
TILE_SIZE = 40 
SCREEN_HEIGHT = 600 
MAX_SAFE_FALL_HEIGHT = 8  

class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, size=(64, 64)):
        super().__init__()

        self.size = size
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
        self.import_character_assets()

        self.animation_speed = 0.15
        self.frame_index = 0
        self.animation_state = 'idle'

        # Imagem inicial
        self.image = self.animations['idle'][0]
        self.rect = self.image.get_rect(topleft=pos)

        # Movimento e física
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.base_gravity = 0.8
        self.gravity = self.base_gravity
        self.min_gravity = 0.4
        self.max_gravity = 2.0
        self.jump_speed = -16
        self.facing_right = True
        self.on_ground = False

        # Contadores
        self.good_items_collected = 0
        self.bad_items_collected = 0
        
        # Queda
        self.fall_start_y = pos[1]
        self.current_fall_distance = 0.0
        self.max_fall_distance = 0.0
        self.is_falling = False
        self.died = False

        # Controle de sprite "gordo"
        self.fat_mode = False
        self.fat_mode_timer = 0
        self.fat_mode_duration = 2500  # 2,5s
        self.last_tick = pygame.time.get_ticks()

        # Sistema de hints educativos
        self.current_hint = None
        self.hint_timer = 0
        self.hint_duration = 3000  # 3 segundos
        self.hints = {
            'hamburguer': 'Hambúrgueres são ricos em gorduras saturadas!',
            'refrigerante': 'Refrigerantes têm muito açúcar e fazem mal!',
            'sorvete': 'Sorvete tem alto teor de açúcar e gordura!'
        }

    def import_character_assets(self):
        path = 'assets/player/'
        
        fallback_image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(fallback_image, (0, 100, 255), fallback_image.get_rect(), 0, 8) 

        asset_paths = {
            'idle': [f'{path}Boneco A1.png'],
            'run': [f'{path}Boneco A1.png', f'{path}Boneco A2.png'],
            'jump': [f'{path}Boneco A1.png'],
            'fall': [f'{path}Boneco A1.png'],
        }

        for state, paths in asset_paths.items():
            for p in paths:
                try:
                    image = pygame.image.load(p).convert_alpha()
                    self.animations[state].append(self.scale_image(image))
                except pygame.error:
                    if not self.animations[state]:
                        self.animations[state].append(fallback_image)
                    print(f"[AVISO] Falha ao carregar sprite: {p}")
            if not self.animations[state]:
                self.animations[state].append(fallback_image)

        # Sprite alternativo “gordo”
        try:
            fat_img = pygame.image.load(f'{path}gordo/Gordo.png').convert_alpha()
            self.fat_image = self.scale_image(fat_img)
        except Exception:
            self.fat_image = fallback_image

    def scale_image(self, image):
        return pygame.transform.scale(image, self.size)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        else:
            self.direction.x = 0

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.jump()

    def jump(self):
        self.direction.y = self.jump_speed
        self.on_ground = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
        # --- Lógica de rastreamento de queda ---
        if not self.on_ground and self.direction.y > 0:
            if not self.is_falling:
                self.is_falling = True
                self.fall_start_y = self.rect.bottom
                self.current_fall_distance = 0.0
            
            self.current_fall_distance = self.rect.bottom - self.fall_start_y
            self.max_fall_distance = max(self.max_fall_distance, self.current_fall_distance)

        elif self.on_ground:
            if self.is_falling:
                fall_tiles = self.current_fall_distance / TILE_SIZE
                if fall_tiles > MAX_SAFE_FALL_HEIGHT:
                    print(f"Dano de queda: {fall_tiles:.1f} tiles > {MAX_SAFE_FALL_HEIGHT}")
                    self.died = True
            
            self.is_falling = False
            self.current_fall_distance = 0.0
            self.fall_start_y = self.rect.bottom

    def animate(self):
        if self.fat_mode:
            # Quando em modo "gordo", fixa sprite
            self.image = self.fat_image if self.facing_right else pygame.transform.flip(self.fat_image, True, False)
            return

        if not self.on_ground:
            self.animation_state = 'jump' if self.direction.y < 0 else 'fall'
        else:
            self.animation_state = 'run' if self.direction.x != 0 else 'idle'

        animation = self.animations[self.animation_state]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        self.image = image if self.facing_right else pygame.transform.flip(image, True, False)

    def update(self):
        self.get_input()
        self.animate()

        # Atualiza timer do modo "gordo"
        now = pygame.time.get_ticks()
        if self.fat_mode and (now - self.fat_mode_timer >= self.fat_mode_duration):
            self.fat_mode = False

        # Atualiza timer do hint
        if self.current_hint and (now - self.hint_timer >= self.hint_duration):
            self.current_hint = None

        self.last_tick = now

    def collect_item(self, item):
        if item.is_good_item():
            self.good_items_collected += 1
        else:
            self.bad_items_collected += 1

            self.fat_mode = True
            self.fat_mode_timer = pygame.time.get_ticks()

            # Ativa hint educativo para comida ruim
            if item.type in self.hints:
                self.current_hint = self.hints[item.type]
                self.hint_timer = pygame.time.get_ticks()

        # Ajusta gravidade
        self.gravity = max(self.min_gravity, min(self.gravity + item.gravity_effect, self.max_gravity))
