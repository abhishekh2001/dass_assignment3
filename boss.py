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

    def move_with_paddle(self):
        self.clear(glob.board.matrix)
        if glob.paddle.get_x() + self.get_width() < config.board_width:
            self.set_x((glob.paddle.get_x()))

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
