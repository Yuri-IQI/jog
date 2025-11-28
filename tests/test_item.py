import pytest
import sys
import os


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
pygame.init()
pygame.display.set_mode((100, 100))

from item import Item


class TestItem:

    def test_item_creation_good_food(self):
        item = Item((100, 100), (24, 24), 'maca')
        assert item.type == 'maca'
        assert item.gravity_effect < 0  
        assert item.is_good_item() == True

    def test_item_creation_bad_food(self):
        item = Item((100, 100), (24, 24), 'hamburguer')
        assert item.type == 'hamburguer'
        assert item.gravity_effect > 0  
        assert item.is_good_item() == False

    def test_item_creation_obstacle(self):
        """Testa criacao de obstaculos"""
        pedra = Item((100, 100), (24, 24), 'pedra')
        cacto = Item((100, 100), (24, 24), 'cacto')

        assert pedra.type == 'pedra'
        assert cacto.type == 'cacto'
        assert pedra.gravity_effect == 0
        assert cacto.gravity_effect == 0

    def test_item_fallback_unknown_type(self):
        item = Item((100, 100), (24, 24), 'tipo_invalido')
        assert item.type == 'hamburguer'  

    def test_item_has_rect(self):
        item = Item((50, 75), (24, 24), 'banana')
        assert item.rect is not None
        assert item.rect.x == 50
        assert item.rect.y == 75

    def test_item_has_image(self):
        item = Item((100, 100), (24, 24), 'alface')
        assert item.image is not None
        assert item.image.get_width() == 24
        assert item.image.get_height() == 24

    def test_item_float_properties(self):
        item = Item((100, 200), (24, 24), 'maca')
        assert item.base_y == 200.0
        assert item.float_y == 200.0
        assert item.float_speed == 0.5
        assert item.float_range == 10

    def test_all_good_items(self):
        good_foods = ['maca', 'banana', 'alface']
        for food in good_foods:
            item = Item((0, 0), (24, 24), food)
            assert item.is_good_item() == True, f"{food} deveria ser comida boa"

    def test_all_bad_items(self):
        bad_foods = ['hamburguer', 'refrigerante', 'sorvete']
        for food in bad_foods:
            item = Item((0, 0), (24, 24), food)
            assert item.is_good_item() == False, f"{food} deveria ser comida ruim"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
