import pytest
import sys
import os


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
pygame.init()
pygame.display.set_mode((600, 672))

from level import Level, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from level2 import WaterLevel
from level3 import Level3
from level4 import BossLevel, Boss, Laser, Cutscene


class TestLevel1:
 

    def test_level_creation(self):
   
        level = Level()
        assert level.level_number == 1
        assert level.game_won == False
        assert level.game_over == False

    def test_level_has_player(self):
        level = Level()
        assert level.player is not None
        assert level.player.sprite is not None

    def test_level_has_floor(self):
        level = Level()
        assert level.floor_surface is not None

    def test_level_scroll_speed(self):
        level = Level()
        assert level.scroll_speed == 3

    def test_level_obstacle_count(self):
        level = Level()
        assert level.obstacle_count == 0

    def test_spawn_obstacle(self):
        level = Level()
        initial_count = len(level.obstacles)
        level.spawn_obstacle()
        assert len(level.obstacles) == initial_count + 1

    def test_spawn_ground_good_item(self):
        level = Level()
        initial_count = len(level.items)
        level.spawn_ground_good_item(2)
        assert len(level.items) == initial_count + 2

    def test_victory_condition(self):
        level = Level()
        level.player.sprite.good_items_collected = 9
        level.update()
        assert level.game_won == True


class TestLevel2:


    def test_level_creation(self):
        level = WaterLevel()
        assert level.level_number == 2
        assert level.game_won == False
        assert level.game_over == False

    def test_level_has_sharks(self):
        level = WaterLevel()
        assert len(level.sharks) > 0

    def test_spawn_shark(self):
        level = WaterLevel()
        initial_count = len(level.sharks)
        level.spawn_shark()
        assert len(level.sharks) == initial_count + 1

    def test_spawn_item(self):
        level = WaterLevel()
        initial_count = len(level.items)
        level.spawn_item()
        assert len(level.items) == initial_count + 1


class TestLevel3:

    def test_level_creation(self):
        level = Level3()
        assert level.level_number == 3
        assert level.game_won == False
        assert level.game_over == False

    def test_level_has_cannons(self):
        level = Level3()
        assert len(level.cannons) > 0

    def test_level_has_layout(self):
        level = Level3()
        assert level.layout is not None
        assert len(level.layout) > 0

    def test_find_spawn_point(self):
        level = Level3()
        spawn = level.find_spawn_point()
        assert spawn is not None
        assert len(spawn) == 2


class TestLevel4:

    def test_level_creation(self):
        level = BossLevel()
        assert level.level_number == 4
        assert level.game_won == False
        assert level.game_over == False

    def test_level_has_boss(self):
        level = BossLevel()
        assert level.boss is not None
        assert level.boss.sprite is not None

    def test_boss_health(self):
        level = BossLevel()
        boss = level.boss.sprite
        assert boss.health == 1800
        assert boss.max_health == 1800

    def test_boss_take_damage(self):
        level = BossLevel()
        boss = level.boss.sprite
        initial_health = boss.health
        boss.take_damage(100)
        assert boss.health == initial_health - 100

    def test_boss_rage_mode(self):
        level = BossLevel()
        boss = level.boss.sprite
        assert boss.rage_mode == False

        boss.activate_rage_mode()
        assert boss.rage_mode == True
        assert boss.speed_x == 7
        assert boss.speed_y == 6

    def test_player_lives(self):
        level = BossLevel()
        assert level.player_lives == level.max_lives
        assert level.max_lives == 5

    def test_cutscene_active(self):
        level = BossLevel()
        assert level.cutscene_active == True


class TestLaser:

    def test_laser_creation(self):
        laser = Laser((100, 100), direction=1)
        assert laser.rect.x >= 100
        assert laser.damage == 20

    def test_laser_strong(self):
        laser = Laser((100, 100), direction=1, strong=True)
        assert laser.damage == 40

    def test_laser_direction(self):
        laser_right = Laser((100, 100), direction=1)
        laser_left = Laser((100, 100), direction=-1)
        assert laser_right.speed > 0
        assert laser_left.speed < 0


class TestCutscene:

    def test_cutscene_creation(self):
        dialogues = [
            ("Personagem 1", "Ola!"),
            ("Personagem 2", "Oi!")
        ]
        cutscene = Cutscene(dialogues)
        assert cutscene.current_dialogue == 0
        assert cutscene.finished == False

    def test_cutscene_dialogues(self):
        dialogues = [
            ("Personagem 1", "Ola!"),
            ("Personagem 2", "Oi!")
        ]
        cutscene = Cutscene(dialogues)
        assert len(cutscene.dialogues) == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
