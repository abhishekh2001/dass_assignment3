import config
import glob
from component import Component
import time


representation = [
            "  ____",
            " / \/ \\",
            "( |  | )",
            " \\    /",
            "  '__'"
        ]





class Boss(Component):
    def __init__(self, x, y):
        super().__init__(x, y, representation)
        self._bomb_interval = time.time()
        self._health = 10
        self._is_def_1 = False
        self._is_def_2 = False

    def move_with_paddle(self):
        self.clear(glob.board.matrix)
        if glob.paddle.get_x() + self.get_width() < config.board_width:
            old = self._x
            self.set_x((glob.paddle.get_x()))
            new = self._x
            delta = new - old
            for brick in glob.boss_bricks:
                brick.clear(glob.board.matrix)
                brick.set_x(brick.get_x() + delta)
            

    def clear(self, board):
        for row in range(self._height):
            for col in range(len(self._representation[row])):
                board[self._y + row][self._x + col] = ' '

    def render(self, board):
        for row in range(self._height):
            for col in range(len(self._representation[row])):
                board[self._y + row][self._x + col] = self._representation[row][col]

    def drop_bomb(self):
        if time.time() - self._bomb_interval >= config.bomb_interval:
            self._bomb_interval = time.time()
            glob.spawn_bomb(self._x, self._y + self._height + 1)

    def get_health(self):
        return self._health

    def lose_health(self):
        self._health -= 1

        if self._health == 9 and not self._is_def_1:
            self._is_def_1 = True            
            for col in range(0, self._width, 4):
                glob.boss_bricks.append(glob.Brick(self._x + col, self._y + self._height, 1, ['BBBB']))
        
        if self._health == 3 and not self._is_def_2:
            self._is_def_2 = True
            
            for brick in glob.boss_bricks:
                brick.clear(glob.board.matrix)
            glob.boss_bricks = []

            for col in range(0, self._width, 4):
                glob.boss_bricks.append(glob.Brick(self._x + col, self._y + self._height, 1, ['BBBB']))

