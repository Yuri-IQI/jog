import pygame

class Item(pygame.sprite.Sprite):
    """Floating collectible item that affects player's gravity."""

    ITEMS = {
        # Bad items (increase gravity)
        'hamburguer': {'image': 'Hamburguer.png', 'effect': 0.25},
        'refrigerante': {'image': 'Refrigerante.png', 'effect': 0.5},
        'sorvete': {'image': 'Sorvete.png', 'effect': 0.15},
        # Good items (decrease gravity)
        'maca': {'image': 'Maçã.png', 'effect': -0.25},
        'alface': {'image': 'Alface.png', 'effect': -0.18},
        'banana': {'image': 'Banana.png', 'effect': -0.12}
    }

    def __init__(self, pos, size, item_type):
        super().__init__()

        # Validate item type
        if item_type not in self.ITEMS:
            raise ValueError(f"Unknown item type: {item_type}")

        self.type = item_type
        self.gravity_effect = self.ITEMS[item_type]['effect']

        # Load and scale image
        image_path = f'assets/item/{self.ITEMS[item_type]["image"]}'
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=pos)

        # Floating animation setup
        self.base_y = float(pos[1])
        self.float_y = float(pos[1])
        self.float_speed = 0.5
        self.float_range = 10
        self.float_direction = 1

    def is_good_item(self):
        """Return True if this is a good item (reduces gravity)."""
        return self.gravity_effect < 0

    def update(self):
        """Animate floating movement."""
        self.float_y += self.float_speed * self.float_direction

        if abs(self.float_y - self.base_y) >= self.float_range:
            self.float_direction *= -1

        self.rect.y = int(self.float_y)