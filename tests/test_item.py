import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import pytest
from unittest.mock import patch, MagicMock

from ..item import Item

@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def basic_item():
    with patch("pygame.image.load") as mock_load:
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        mock_load.return_value = surf
        return Item((100, 100), (32, 32), "banana")

# TC001 — Item inicializa com tipo e efeito corretos
def test_item_initializes_with_correct_type_and_effect(basic_item):
    assert basic_item.type == "banana"
    assert basic_item.gravity_effect == Item.ITEMS["banana"]["effect"]

# TC002 — Item bom é reconhecido como bom
def test_item_is_good_item(basic_item):
    assert basic_item.is_good_item() is True

# TC003 — Item inicia na posição correta
def test_item_rect_position(basic_item):
    assert basic_item.rect.topleft == (100, 100)

# TC004 — Imagem do item é um pygame.Surface
def test_item_has_image_surface(basic_item):
    assert isinstance(basic_item.image, pygame.Surface)

# TC005 — Item bom possui efeito negativo (flutua)
def test_good_item_effect():
    with patch("pygame.image.load") as mock_load:
        surf = pygame.Surface((32, 32))
        mock_load.return_value = surf
        item = Item((0, 0), (32, 32), "banana")

    assert item.gravity_effect < 0
    assert item.is_good_item() is True

# TC006 — Item ruim possui efeito positivo (cai)
def test_bad_item_effect():
    with patch("pygame.image.load") as mock_load:
        surf = pygame.Surface((32, 32))
        mock_load.return_value = surf
        item = Item((0, 0), (32, 32), "hamburguer")

    assert item.gravity_effect > 0
    assert item.is_good_item() is False

# TC007 — Tipo desconhecido usa fallback e emite aviso
def test_unknown_item_uses_fallback_and_prints_warning(capsys):
    with patch("pygame.image.load") as mock_load:
        surf = pygame.Surface((32, 32))
        mock_load.return_value = surf
        item = Item((0, 0), (32, 32), "xxxxx")

    captured = capsys.readouterr()
    assert "AVISO" in captured.out
    assert item.type == "hamburguer"

# TC008 — Falha ao carregar imagem usa placeholder e emite erro
def test_image_load_failure_uses_placeholder(capsys):
    with patch("pygame.image.load", side_effect=pygame.error("fail")):
        item = Item((0, 0), (32, 32), "banana")

    captured = capsys.readouterr()
    assert "ERRO DE CARREGAMENTO" in captured.out
    assert isinstance(item.image, pygame.Surface)

# TC009 — Item tipo pedra desenha polígono
def test_rock_item_has_polygon_drawing():
    item = Item((0,0), (40,40), "pedra")
    px = item.image.get_at((10, 35))
    assert px.a > 0

# TC010 — Item tipo cacto possui pixels verdes
def test_cactus_item_has_green_pixels():
    item = Item((0,0), (40,40), "cacto")
    found_green = False

    for x in range(40):
        for y in range(40):
            r, g, b, a = item.image.get_at((x, y))
            if g > r and g > b and a > 0:
                found_green = True
                break
    assert found_green is True

# TC011 — Movimento de flutuação altera Y
def test_item_float_movement():
    item = Item((100, 100), (32, 32), "banana")
    y0 = item.rect.y

    item.update()
    assert item.rect.y != y0

# TC012 — Direção da flutuação alterna ao atingir limite
def test_float_direction_reverses_after_range():
    item = Item((0, 100), (32, 32), "banana")
    item.float_y = item.base_y + item.float_range

    old_dir = item.float_direction
    item.update()

    assert item.float_direction == -old_dir