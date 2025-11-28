import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import pytest
from unittest.mock import patch, MagicMock

from ..menu import MainMenu

@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

# TC001 — Navegação do menu
def test_screen_changes_when_option_selected():
    menu = MainMenu()
    assert menu.current_screen == "main"

    menu.current_screen = "options"
    assert menu.current_screen == "options"

# TC002 — Botão de iniciar
@patch("pygame.mixer.music")
def test_main_click_start(mock_music):
    menu = MainMenu()
    start_button = menu.buttons["main"]["start"]
    result = menu.handle_main_click(start_button.center)
    assert result == "start_game"

# TC003 — Iniciar fase selecionada
@patch("pygame.mixer.music.stop")
def test_select_level_3(mock_stop):
    menu = MainMenu()
    menu.current_screen = "level_select"
    btn = menu.buttons["level_select"]["level3"]
    result = menu.handle_level_select_click(btn.center)

    assert menu.selected_level == 3
    assert result == "start_level_3"

# TC004 — Voltar para menu principal
def test_level_select_back():
    menu = MainMenu()
    menu.current_screen = "level_select"

    back = menu.buttons["level_select"]["back"]
    menu.handle_level_select_click(back.center)

    assert menu.current_screen == "main"

# TC005 — Configurar seleção de música para fase
def test_music_config_next_changes_selection():
    menu = MainMenu()
    menu.current_screen = "music_config"

    old = menu.current_music_selection[1]
    btn_next = menu.buttons["music_config"]["next_1"]

    menu.handle_music_config_click(btn_next.center)

    assert menu.current_music_selection[1] == (old + 1) % len(menu.available_musics)

# TC006 — Tocar música no player de música
@patch("pygame.mixer.music")
def test_music_player_play(mock_music):
    menu = MainMenu()
    menu.current_screen = "music_player"

    play = menu.buttons["music_player"]["play_pause"]
    menu.handle_music_player_click(play.center)

    assert menu.music_player_playing is True

# TC007 — Parar música no player de música
@patch("pygame.mixer.music")
def test_music_player_stop(mock_music):
    menu = MainMenu()
    menu.current_screen = "music_player"
    menu.music_player_playing = True

    stop = menu.buttons["music_player"]["stop"]
    menu.handle_music_player_click(stop.center)

    assert menu.music_player_playing is False
    mock_music.stop.assert_called_once()
    
# TC008 — Sair do jogo pelo menu
def test_main_click_quit():
    menu = MainMenu()
    btn = menu.buttons["main"]["quit"]
    result = menu.handle_main_click(btn.center)

    assert result == "quit"