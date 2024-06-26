from board import Board
from candy import Candy
import pygame


class Game:
    def __init__(self):
        self.board = Board()
        self.candy = Candy()
        self.next_candy = Candy()
        self.game_over = False
        self.score = 0
        self.sound = True
        self.best_score = self.get_best_socre()
        self.clear_sound = pygame.mixer.Sound("sound/Sounds_clear.ogg")
        self.game_over_sound = pygame.mixer.Sound("sound/game-over-39-199830.mp3")
        self.level = self.get_level()

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared >= 1:
            self.score += 100
        self.score += move_down_points

    def move_left(self):
        self.candy.move(0, -1)
        if self.block_inside() == 0 or self.block_fits() == 0:
            self.candy.move(0, 1)

    def move_right(self):
        self.candy.move(0, 1)
        if self.block_inside() == 0 or self.block_fits() == 0:
            self.candy.move(0, -1)

    def move_down(self):
        self.candy.move(1, 0)
        if self.block_inside() == 0 or self.block_fits() == 0:
            self.candy.move(-1, 0)
            self.lock_block()

    def block_inside(self):
        tile = self.candy.get_cell_position()
        if self.board.is_inside(tile.row, tile.col) == 0:
            return False
        return True

    def reset(self):
        self.board.reset()
        self.candy = Candy()
        self.next_candy = Candy()
        self.score = 0

    def lock_block(self):
        position = self.candy.get_cell_position()
        self.board.insert_new_node(position.row, position.col, self.candy.id)
        self.candy = self.next_candy
        self.next_candy = Candy()
        row_cleared = self.board.clear_three_candy_row()
        col_cleared = self.board.clear_three_candy_col()
        if row_cleared > 0 or col_cleared > 0:
            if self.sound:
                self.clear_sound.play()
            self.update_score(row_cleared or col_cleared, 0)
        if self.block_fits() == 0:
            self.game_over = True
            self.game_over_sound.play()

    def get_best_socre(self):
        try:
            with open("score.txt", "r") as rfp:
                best_score = int(rfp.read())
        except FileNotFoundError:
            with open("score.txt", "w") as wfp:
                wfp.write("0")
                best_score = 0
        return best_score

    def get_level(self):
        try:
            with open("level.txt", "r") as rfp:
                level = int(rfp.read())
        except FileNotFoundError:
            with open("level.txt", "w") as wfp:
                wfp.write("1")
                level = 1
        return level

    def block_fits(self):
        tile = self.candy.get_cell_position()
        if self.board.is_empty(tile.row, tile.col) == 0:
            return False
        return True

    def get_speed_for_each_level(self):
        return 250 - self.level * 50

    def draw(self, screen):
        self.board.draw(screen)
        self.candy.draw(screen, 50, 100)
        self.next_candy.draw(screen, 422, 325)
