import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import pytest
from unittest.mock import patch

from ..level import Level
from ..level2 import WaterLevel, Shark
from ..level3 import Level3
from ..level4 import BossLevel, Cutscene, Boss, PowerUp, SCREEN_HEIGHT, TILE_SIZE, Laser

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

# TC001 — Inicialização da fase principal (Level)
def test_level_initialization():
    level = Level()
    assert level.player.sprite is not None
    assert len(level.tiles) > 0
    assert len(level.houses) >= 5
    assert level.background_image is not None

# TC002 — Colisão com o piso
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

# TC003 — Coleta de item bom aumenta pontuação
def test_good_item_collision_increases_score():
    level = Level()
    player = level.player.sprite

    item = FakeSprite(player.rect.copy(), is_bad_rain=False)

    level.items.add(item)
    level.check_item_collisions()

    assert player.good_items_collected == 1

# TC004 — Colisão com obstáculo mortal termina o jogo
def test_deadly_obstacle_triggers_game_over():
    level = Level()
    player = level.player.sprite

    obs = FakeSprite(player.rect.copy(), is_deadly=True, type="pedra")

    level.obstacles.add(obs)
    level.check_obstacle_collisions()

    assert level.game_over is True

# TC005 — Condição de vitória ao alcançar 9 itens bons
def test_win_condition_reaches_9_items():
    level = Level()
    player = level.player.sprite

    player.good_items_collected = 9
    level.update()

    assert level.game_won is True

# TC006 — Inicialização do Shark
def test_shark_initialization():
    s = Shark(10, 100, direction="right")
    assert s.direction in ("left", "right")
    assert 3 <= s.speed <= 5
    assert isinstance(s.rect, pygame.Rect)

# TC007 — Inicialização de WaterLevel
def test_waterlevel_initialization():
    w = WaterLevel()
    assert w.player.sprite is not None
    assert len(w.sharks) >= 1
    assert w.overlay is not None

# TC008 — Spawn de tubarões
def test_waterlevel_shark_spawn():
    w = WaterLevel()
    start = len(w.sharks)
    w.spawn_shark()
    assert len(w.sharks) == start + 1

# TC009 — Jogador atingido por projétil
def test_level3_player_hit_by_projectile():
    l3 = Level3()
    player = l3.player.sprite
    projectile = FakeSprite(
        rect=player.rect.copy(),
        damage=10,
        type="hamburguer",
        speed=7,
        direction=1
    )

    l3.projectiles.add(projectile)

    if hasattr(l3, "check_projectile_collisions"):
        l3.check_projectile_collisions()
    else:
        l3.update()

    assert len(l3.projectiles) == 0
    assert getattr(player, "was_hit", True)

# TC010 — Spawn point deve coincidir com o 'P' do layout
def test_level3_spawn_point():
    l3 = Level3()
    spawn = l3.find_spawn_point()

    player = l3.player.sprite
    assert (player.rect.x, player.rect.y) == spawn

# TC011 — Posicionamento de itens no mapa
def test_level3_items_are_placed():
    l3 = Level3()

    assert len(l3.items) > 0

    for item in l3.items:
        assert hasattr(item, "type")
        assert isinstance(item.rect, pygame.Rect)

# TC012 — Canhões conseguem disparar projéteis
def test_level3_cannons_fire_projectiles(monkeypatch):
    l3 = Level3()

    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 999999)

    before = len(l3.projectiles)

    l3.shoot_from_cannons()

    after = len(l3.projectiles)

    assert after == before + 1
    projectile = list(l3.projectiles)[0]

    assert hasattr(projectile, "direction")
    assert projectile.speed == 7
    assert projectile.type in ("hamburguer", "refrigerante", "sorvete")

# TC013 — Cutscene começa e termina
def test_bosslevel_cutscene_progression():
    c = Cutscene([
        ("A", "fala 1"),
        ("B", "fala 2"),
    ])

    fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)

    assert c.current_dialogue == 0
    assert not c.finished

    c.update(fake_event)
    assert c.current_dialogue == 1
    assert not c.finished

    c.update(fake_event)
    assert c.finished

# TC014 — Boss entra em Rage Mode corretamente
def test_bosslevel_boss_rage_mode_activation():
    boss = Boss((300, 300))

    boss.take_damage(boss.max_health // 2 + 10)
    
    assert boss.rage_mode is True
    assert boss.speed_x == 7
    assert boss.speed_y == 6
    assert boss.shoot_interval == 800

# TC015 — PowerUp cai e para no chão
def test_bosslevel_powerup_falls_and_stops():
    p = PowerUp((100, 50))
    start_y = p.rect.y

    for _ in range(200):
        p.update()

    assert p.rect.y > start_y
    assert p.rect.bottom == SCREEN_HEIGHT - TILE_SIZE

# TC016 — Batalha final
def test_bosslevel_laser_hits_boss():
    level = BossLevel()
    boss = level.boss.sprite
    initial_hp = boss.health

    laser = Laser(
        pos=(boss.rect.left, boss.rect.centery),
        direction=1,
        strong=False
    )

    level.lasers.add(laser)

    level.check_laser_hits()

    assert boss.health == initial_hp - 20
    assert len(level.lasers) == 0