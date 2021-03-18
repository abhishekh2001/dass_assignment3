import config
import glob
from component import Component
import time


class Bomb(Component):
    def __init__(self, x, y):
        super(Bomb, self).__init__(x, y, [['V']])
        self._move_timestamp = time.time()

    def move_down(self):
        """
        Returns true if bomb is to disappear
        false otherwise
        """
        if time.time() - self._move_timestamp >= config.bomb_speed:
            self.clear(glob.board.matrix)
            self._y = self._y + 1
            if self._y == config.board_height - 2 and \
                    (glob.paddle.get_x() <= self._x <= glob.paddle.get_x()+glob.paddle.get_width()):
                glob.player.lose_life()
            self._move_timestamp = time.time()
        return self._y >= config.board_height - 1
