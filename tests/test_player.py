import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import pytest
from unittest.mock import patch, MagicMock

from ..player import Player, TILE_SIZE, MAX_SAFE_FALL_HEIGHT

@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def player():
    with patch("pygame.image.load") as mock_load:
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        mock_load.return_value = surf
        return Player((100, 100))

# TC001 — Pulo do jogador
def test_player_jump_sets_negative_y_velocity(player):
    player.on_ground = True
    player.jump()
    assert player.direction.y == player.jump_speed
    assert not player.on_ground

# TC002 — Aplicação da gravidade
def test_apply_gravity_increases_y_and_tracks_fall(player):
    start_y = player.rect.y
    player.on_ground = False
    player.direction.y = 5

    player.apply_gravity()
    assert player.rect.y > start_y
    assert player.is_falling is True

    previous_bottom = player.rect.bottom
    player.apply_gravity()
    assert player.rect.bottom > previous_bottom
    assert player.current_fall_distance > 0

# TC003 — Dano de queda
def test_fall_damage_when_exceeding_safe_height(player):
    player.on_ground = False
    player.is_falling = True
    player.fall_start_y = player.rect.bottom

    player.rect.y += int((MAX_SAFE_FALL_HEIGHT + 2) * TILE_SIZE)
    player.current_fall_distance = player.rect.bottom - player.fall_start_y

    player.on_ground = True
    player.apply_gravity()

    assert player.died is True

class MockBadItem:
    def __init__(self):
        self.type = "hamburguer"
        self.gravity_effect = 0.5

    def is_good_item(self):
        return False


class MockGoodItem:
    def __init__(self):
        self.type = "banana"
        self.gravity_effect = -0.3

    def is_good_item(self):
        return True


# TC004 — Coleta de item bom
def test_collect_good_item_increases_good_counter(player):
    i = MockGoodItem()
    initial = player.good_items_collected
    player.collect_item(i)

    assert player.good_items_collected == initial + 1
    assert player.bad_items_collected == 0

# TC005 — Coleta de item ruim ativa modo “gordo”
def test_collect_bad_item_enables_fat_mode_and_hint(player):
    i = MockBadItem()
    player.collect_item(i)

    assert player.fat_mode is True
    assert player.bad_items_collected == 1
    assert player.current_hint is not None
    assert player.gravity > player.min_gravity


# TC006 — Animação muda quando o jogador se move
def test_animation_switches_state_when_moving(player):
    player.on_ground = True
    player.direction.x = 1

    prev_image = player.image
    player.animate()

    assert player.animation_state == "run"
    assert player.image is not None

# TC007 — Animação de pulo
def test_animation_switches_state_when_jumping(player):
    player.on_ground = False
    player.direction.y = -5

    player.animate()
    assert player.animation_state == "jump"

# TC008 — Animação de queda
def test_animation_switches_state_when_falling(player):
    player.on_ground = False
    player.direction.y = 5

    player.animate()
    assert player.animation_state == "fall"
