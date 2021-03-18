import config
import glob
from component import Component
import time
import balls


representation = [
            "  ____",
            " / \/ \\",
            "( |  | )",
            " \\    /",
            "  '__'"
        ]


def handle_ball_ufo_collision(ball):
    """
    For any given ball, determine if ball collides with any brick
    :param ball:
    :return:
    """
    if glob.boss.get_x() - 1 <= ball.get_x() <= glob.boss.get_x() + glob.boss.get_width() and \
            glob.boss.get_y() - 1 <= ball.get_y() <= glob.boss.get_y() + glob.boss.get_height():
        if balls.bounce_ball(glob.boss, ball):
            glob.boss.lose_health()
    glob.bricks = list(filter(lambda b: b.get_health(), glob.bricks))


class Boss(Component):
    def __init__(self, x, y):
        super().__init__(x, y, representation)
        self._bomb_interval = time.time()
        self._health = 10

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

    def get_health(self):
        return self._health

    def lose_health(self):
        self._health -= 1
