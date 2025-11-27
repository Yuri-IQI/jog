import os
import sys
os.environ["SDL_VIDEODRIVER"] = "dummy"

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pygame
import pytest
from unittest.mock import patch

from ..level import Level
from ..level2 import WaterLevel, Shark
from ..level3 import Level3
from ..level4 import BossLevel

@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

@pytest.fixture
def fake_image():
    return pygame.Surface((50, 50))

@pytest.fixture(autouse=True)
def patch_images(monkeypatch, fake_image):
    monkeypatch.setattr(pygame.image, "load", lambda *_, **__: fake_image)
    return fake_image

@pytest.fixture(autouse=True)
def patch_mixer(monkeypatch):
    monkeypatch.setattr(pygame.mixer, "init", lambda *_, **__: None)
    monkeypatch.setattr(pygame.mixer.music, "load", lambda *_, **__: None)
    monkeypatch.setattr(pygame.mixer.music, "play", lambda *_, **__: None)
    monkeypatch.setattr(pygame.mixer.music, "stop", lambda *_, **__: None)
    monkeypatch.setattr(pygame.mixer.music, "set_volume", lambda *_, **__: None)

def test_level_initialization():
    level = Level()
    assert level.player.sprite is not None
    assert len(level.tiles) > 0
    assert len(level.houses) >= 5
    assert level.background_image is not None


def test_level_floor_collision():
    level = Level()
    player = level.player.sprite

    player.rect.bottom = level.floor_y + 50
    level.check_floor_collision(player)

    assert player.rect.bottom == level.floor_y
    assert player.on_ground is True

class FakeSprite(pygame.sprite.Sprite):
    def __init__(self, rect, **attrs):
        super().__init__()
        self.rect = rect
        for k, v in attrs.items():
            setattr(self, k, v)

def test_good_item_collision_increases_score():
    level = Level()
    player = level.player.sprite

    item = FakeSprite(player.rect.copy(), is_bad_rain=False)

    level.items.add(item)
    level.check_item_collisions()

    assert player.good_items_collected == 1

def test_deadly_obstacle_triggers_game_over():
    level = Level()
    player = level.player.sprite

    obs = FakeSprite(player.rect.copy(), is_deadly=True, type="pedra")

    level.obstacles.add(obs)
    level.check_obstacle_collisions()

    assert level.game_over is True

def test_win_condition_reaches_9_items():
    level = Level()
    player = level.player.sprite

    player.good_items_collected = 9
    level.update()

    assert level.game_won is True

def test_shark_initialization():
    s = Shark(10, 100, direction="right")
    assert s.direction in ("left", "right")
    assert 3 <= s.speed <= 5
    assert isinstance(s.rect, pygame.Rect)

def test_waterlevel_initialization():
    w = WaterLevel()
    assert w.player.sprite is not None
    assert len(w.sharks) >= 1
    assert w.overlay is not None

def test_waterlevel_shark_spawn():
    w = WaterLevel()
    start = len(w.sharks)
    w.spawn_shark()
    assert len(w.sharks) == start + 1