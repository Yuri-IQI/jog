import pygame
import math

class Item(pygame.sprite.Sprite):

    ITEMS = {
        'hamburguer': {'image': 'Hamburguer.png', 'effect': 0.25},
        'refrigerante': {'image': 'Refrigerante.png', 'effect': 0.5},
        'sorvete': {'image': 'Sorvete.png', 'effect': 0.15},

        'maca': {'image': 'Maçã.png', 'effect': -0.25},
        'alface': {'image': 'Alface.png', 'effect': -0.18},
        'banana': {'image': 'Banana.png', 'effect': -0.12},

        
        'pedra': {'image': 'Pedra.png', 'effect': 0},
        'cacto': {'image': 'Cacto.png', 'effect': 0}
    }

    def __init__(self, pos, size, item_type):
        super().__init__()

   
        if item_type not in self.ITEMS:
            
            print(f"AVISO: Tipo de item desconhecido ('{item_type}'). Usando hambúrguer como fallback.")
            item_type = 'hamburguer' 

        self.type = item_type
        self.gravity_effect = self.ITEMS[item_type]['effect']
        
      
        is_good = self.gravity_effect < 0
        fallback_color = (0, 200, 50) if is_good else (255, 100, 100) 
        
        self.image = pygame.Surface(size, pygame.SRCALPHA)

     
        if item_type == 'pedra':
            self._draw_rock(size)
        elif item_type == 'cacto':
            self._draw_cactus(size)
        else:
            pygame.draw.circle(self.image, fallback_color, (size[0] // 2, size[1] // 2), size[0] // 3)
            pygame.draw.circle(self.image, (255, 255, 255), (size[0] // 2, size[1] // 2), size[0] // 3, 2)
            image_path = f'assets/item/{self.ITEMS[item_type]["image"]}'
            try:
                raw_image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(raw_image, size)
            except pygame.error as e:
                print(f"ERRO DE CARREGAMENTO: Não foi possível carregar o asset '{image_path}'. Usando placeholder. Motivo: {e}")

        self.rect = self.image.get_rect(topleft=pos)

   
        self.base_y = float(pos[1])
        self.float_y = float(pos[1])
        self.float_speed = 0.5
        self.float_range = 10
        self.float_direction = 1

    def is_good_item(self):
        return self.gravity_effect < 0

    def _draw_rock(self, size):
        w, h = size
        points = [
            (w * 0.2, h * 0.9), (w * 0.1, h * 0.6), (w * 0.25, h * 0.3),
            (w * 0.5, h * 0.15), (w * 0.75, h * 0.25), (w * 0.9, h * 0.5),
            (w * 0.85, h * 0.85), (w * 0.5, h * 0.95)
        ]
        pygame.draw.polygon(self.image, (100, 100, 100), points)
        pygame.draw.polygon(self.image, (70, 70, 70), points, 2)
        # Detalhes
        pygame.draw.line(self.image, (130, 130, 130), (w * 0.3, h * 0.5), (w * 0.5, h * 0.4), 2)
        pygame.draw.line(self.image, (130, 130, 130), (w * 0.6, h * 0.6), (w * 0.7, h * 0.5), 2)

    def _draw_cactus(self, size):
       
        w, h = size
  
        body_rect = pygame.Rect(w * 0.35, h * 0.2, w * 0.3, h * 0.75)
        pygame.draw.rect(self.image, (34, 139, 34), body_rect, border_radius=5)
      
        pygame.draw.rect(self.image, (34, 139, 34), (w * 0.1, h * 0.35, w * 0.25, h * 0.12), border_radius=3)
        pygame.draw.rect(self.image, (34, 139, 34), (w * 0.1, h * 0.25, w * 0.12, h * 0.22), border_radius=3)
      
        pygame.draw.rect(self.image, (34, 139, 34), (w * 0.65, h * 0.5, w * 0.25, h * 0.12), border_radius=3)
        pygame.draw.rect(self.image, (34, 139, 34), (w * 0.78, h * 0.35, w * 0.12, h * 0.27), border_radius=3)
    
        for i in range(3):
            pygame.draw.line(self.image, (255, 255, 200), (w * 0.4, h * (0.3 + i * 0.2)), (w * 0.35, h * (0.28 + i * 0.2)), 1)
            pygame.draw.line(self.image, (255, 255, 200), (w * 0.6, h * (0.35 + i * 0.18)), (w * 0.65, h * (0.33 + i * 0.18)), 1)

    def update(self):
        self.float_y += self.float_speed * self.float_direction

        if abs(self.float_y - self.base_y) >= self.float_range:
            self.float_direction *= -1

        dy = self.float_y - self.rect.y
        if abs(dy) < 1:
            self.rect.y += 1 * self.float_direction
        else:
            self.rect.y = int(self.float_y)