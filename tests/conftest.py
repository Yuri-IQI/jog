import pytest
import sys
import os


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    pygame.init()
    pygame.display.set_mode((600, 672))
    yield
    pygame.quit()
