import glob
import time
from ball import Laser


def handle_laser_impact(brick):
    """
    Behavior of brick on successful impact with ball
    :param brick: brick instance
    """
    if brick.get_rainbow():
        brick.set_rainbow(False)
    if brick.get_brick_type() == 4:
        brick.chain_explosions()
    elif brick.got_hit(glob.board.matrix):  # Brick has zero health -> is destroyed
        glob.spawn_powerup(brick.get_x(), brick.get_y())
        glob.player.increment_points_by(brick.get_score())  # increase player points


def handle_ball_brick_collision(ball):
    """
    For any given laser, determine if laser collides with any brick
    :param ball: single laser instance
    :return: true if hit and false if not
    """
    hit = False
    for brick in glob.bricks:
        if brick.get_x() - 1 <= ball.get_x() <= brick.get_x() + brick.get_width() and \
                brick.get_y() - 1 <= ball.get_y() <= brick.get_y() + brick.get_height():
            handle_laser_impact(brick)
            hit = True
    glob.bricks = list(filter(lambda b: b.get_health(), glob.bricks))
    return hit


class Lasers:
    def __init__(self):
        self._lasers = []
        self._prev_laser_timestamp = time.time()

    def add_laser(self, x, y, representation=[['|']], speed=1):
        laser = Laser(x, y, 0, -1, representation, True, speed)
        self._lasers.append(laser)

    def remove_all(self):
        self._lasers = []

    def get_lasers(self):
        return self._lasers

    def move_all(self):
        pbt = self._prev_laser_timestamp
        flag = False
        for laser in list(self._lasers):
            if time.time() - pbt >= laser.get_speed():
                flag = True
                hit = handle_ball_brick_collision(laser)
                if hit:
                    self._lasers.remove(laser)
                laser.move_relative(glob.board.matrix, laser.get_xvel(), laser.get_yvel())

                if laser.get_y() <= 1:
                    self._lasers.remove(laser)
                # laser.move_relative(glob.board.matrix, 0, -1)
        if flag:
            pbt = time.time()
        self._prev_laser_timestamp = pbt

    def render_all(self, board):
        for ball in self._lasers:
            ball.render(board)

    def clear_all(self, board):
        for ball in self._lasers:
            ball.clear(board)
