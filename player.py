import pygame

# Constants
TILE_SIZE = 40  # Make sure this matches the TILE_SIZE in level.py

class Player(pygame.sprite.Sprite):
    MAX_SAFE_FALL_HEIGHT = 8  # Maximum tiles the player can safely fall
    
    def __init__(self, pos, size=(64, 64)):
        super().__init__()

        self.size = size
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
        self.import_character_assets()

        self.animation_speed = 0.15
        self.frame_index = 0
        self.animation_state = 'idle'

        self.image = self.animations['idle'][0]
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.base_gravity = 0.8
        self.gravity = self.base_gravity
        self.min_gravity = 0.4
        self.max_gravity = 2.0
        self.jump_speed = -16
        self.facing_right = True
        self.on_ground = False

        self.good_items_collected = 0
        self.bad_items_collected = 0
        
        # Altitude tracking
        self.fall_start_y = 0
        self.current_fall_distance = 0
        self.max_fall_distance = 0
        self.is_falling = False
        self.died = False

    def import_character_assets(self):
        """Load and scale animations."""
        path = 'assets/player/'
        self.animations['idle'] = [self.scale_image(pygame.image.load(f'{path}Boneco A1.png').convert_alpha())]
        self.animations['run'] = [
            self.scale_image(pygame.image.load(f'{path}Boneco A1.png').convert_alpha()),
            self.scale_image(pygame.image.load(f'{path}Boneco A2.png').convert_alpha())
        ]
        self.animations['jump'] = [self.scale_image(pygame.image.load(f'{path}Boneco A2.png').convert_alpha())]
        self.animations['fall'] = [self.scale_image(pygame.image.load(f'{path}Boneco A1.png').convert_alpha())]

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
        # Start tracking fall distance from the jump point
        self.is_falling = True
        self.fall_start_y = self.rect.y

    def apply_gravity(self):
        self.direction.y += self.gravity
        
        # Track falling only if we started falling from a jump
        if self.is_falling and not self.on_ground:
            # Only count the fall when moving downward (after reaching peak of jump)
            if self.direction.y > 0:
                self.current_fall_distance = (self.rect.y - self.fall_start_y) / TILE_SIZE
                self.max_fall_distance = max(self.max_fall_distance, self.current_fall_distance)
        elif self.on_ground:
            # Check if the fall was too high before resetting
            if self.is_falling and self.current_fall_distance > self.MAX_SAFE_FALL_HEIGHT:
                self.died = True
            self.is_falling = False
            self.current_fall_distance = 0
            
        self.rect.y += self.direction.y

    def animate(self):
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

    def collect_item(self, item):
        """Apply item effect to gravity."""
        if item.is_good_item():
            self.good_items_collected += 1
        else:
            self.bad_items_collected += 1

        self.gravity = max(self.min_gravity, min(self.gravity + item.gravity_effect, self.max_gravity))