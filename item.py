import pygame
import math

class Item(pygame.sprite.Sprite):
    """Floating collectible item that affects player's gravity."""

    ITEMS = {
        'hamburguer': {'image': 'Hamburguer.png', 'effect': 0.25},
        'refrigerante': {'image': 'Refrigerante.png', 'effect': 0.5},
        'sorvete': {'image': 'Sorvete.png', 'effect': 0.15},
   
        'maca': {'image': 'Maçã.png', 'effect': -0.25},
        'alface': {'image': 'Alface.png', 'effect': -0.18},
        'banana': {'image': 'Banana.png', 'effect': -0.12}
    }

    def __init__(self, pos, size, item_type):
        super().__init__()

        # Validate item type
        if item_type not in self.ITEMS:
            
            print(f"AVISO: Tipo de item desconhecido ('{item_type}'). Usando hambúrguer como fallback.")
            item_type = 'hamburguer' 

        self.type = item_type
        self.gravity_effect = self.ITEMS[item_type]['effect']
        
        # --- Configuração do Fallback (Placeholder) ---
        is_good = self.gravity_effect < 0
        fallback_color = (0, 200, 50) if is_good else (255, 100, 100) # Verde para bom, Vermelho para ruim
        
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        # Desenha um círculo colorido
        pygame.draw.circle(self.image, fallback_color, (size[0] // 2, size[1] // 2), size[0] // 3)
        # Adiciona uma borda para distinção
        pygame.draw.circle(self.image, (255, 255, 255), (size[0] // 2, size[1] // 2), size[0] // 3, 2)
        # ----------------------------------------------
        
        # Load and scale image safely
        image_path = f'assets/item/{self.ITEMS[item_type]["image"]}'
        
        try:

            raw_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(raw_image, size)
        except pygame.error as e:

            print(f"ERRO DE CARREGAMENTO: Não foi possível carregar o asset '{image_path}'. Usando placeholder. Motivo: {e}")

        self.rect = self.image.get_rect(topleft=pos)

        # Floating animation setup
        self.base_y = float(pos[1])
        self.float_y = float(pos[1])
        self.float_speed = 0.5
        self.float_range = 10
        self.float_direction = 1

    def is_good_item(self):
        return self.gravity_effect < 0

    def update(self):
     
    
        self.float_y += self.float_speed * self.float_direction

        if abs(self.float_y - self.base_y) >= self.float_range:
            self.float_direction *= -1

        self.rect.y = int(self.float_y)
