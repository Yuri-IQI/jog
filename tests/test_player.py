import pytest
import sys
import os


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
pygame.init()
pygame.display.set_mode((100, 100))

from player import Player
from item import Item


class TestPlayer:
    """Testes para a classe Player"""

    def test_player_creation(self):
        """Testa criacao do jogador"""
        player = Player((100, 200), size=(24, 24))
        assert player.rect.x == 100
        assert player.rect.y == 200

    def test_player_initial_counters(self):
        """Testa contadores iniciais"""
        player = Player((0, 0), size=(24, 24))
        assert player.good_items_collected == 0
        assert player.bad_items_collected == 0

    def test_player_initial_state(self):
        """Testa estado inicial do jogador"""
        player = Player((0, 0), size=(24, 24))
        assert player.on_ground == False
        assert player.died == False
        assert player.fat_mode == False

    def test_player_direction(self):
        """Testa vetor de direcao"""
        player = Player((0, 0), size=(24, 24))
        assert player.direction.x == 0
        assert player.direction.y == 0

    def test_player_speed(self):
        """Testa velocidade do jogador"""
        player = Player((0, 0), size=(24, 24))
        assert player.speed == 6

    def test_player_gravity(self):
        """Testa gravidade do jogador"""
        player = Player((0, 0), size=(24, 24))
        assert player.gravity == player.base_gravity
        assert player.min_gravity == 0.4
        assert player.max_gravity == 2.0

    def test_player_jump(self):
        """Testa pulo do jogador"""
        player = Player((0, 0), size=(24, 24))
        player.on_ground = True
        player.jump()
        assert player.direction.y == player.jump_speed
        assert player.on_ground == False

    def test_player_apply_gravity(self):
        """Testa aplicacao de gravidade"""
        player = Player((0, 100), size=(24, 24))
        initial_y = player.rect.y
        player.apply_gravity()
        # Gravidade deve mover o jogador para baixo
        assert player.direction.y > 0

    def test_player_collect_good_item(self):
        """Testa coleta de item bom"""
        player = Player((0, 0), size=(24, 24))
        item = Item((0, 0), (24, 24), 'maca')

        player.collect_item(item)

        assert player.good_items_collected == 1
        assert player.bad_items_collected == 0
        assert player.fat_mode == False

    def test_player_collect_bad_item(self):
        """Testa coleta de item ruim"""
        player = Player((0, 0), size=(24, 24))
        item = Item((0, 0), (24, 24), 'hamburguer')

        player.collect_item(item)

        assert player.good_items_collected == 0
        assert player.bad_items_collected == 1
        assert player.fat_mode == True

    def test_player_hints(self):
        """Testa sistema de hints educativos"""
        player = Player((0, 0), size=(24, 24))

        assert 'hamburguer' in player.hints
        assert 'refrigerante' in player.hints
        assert 'sorvete' in player.hints

    def test_player_collect_bad_item_shows_hint(self):
        """Testa se coleta de item ruim mostra hint"""
        player = Player((0, 0), size=(24, 24))
        item = Item((0, 0), (24, 24), 'hamburguer')

        player.collect_item(item)

        assert player.current_hint is not None
        assert 'gorduras' in player.current_hint.lower() or 'hamburguer' in player.current_hint.lower()

    def test_player_gravity_affected_by_items(self):
        """Testa se gravidade e afetada por itens"""
        player = Player((0, 0), size=(24, 24))
        initial_gravity = player.gravity

        bad_item = Item((0, 0), (24, 24), 'hamburguer')
        player.collect_item(bad_item)

        # Comida ruim aumenta gravidade
        assert player.gravity > initial_gravity or player.gravity == player.max_gravity

    def test_player_has_image(self):
        """Testa se jogador tem imagem"""
        player = Player((0, 0), size=(24, 24))
        assert player.image is not None

    def test_player_animation_states(self):
        """Testa estados de animacao"""
        player = Player((0, 0), size=(24, 24))
        assert 'idle' in player.animations
        assert 'run' in player.animations
        assert 'jump' in player.animations
        assert 'fall' in player.animations


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
