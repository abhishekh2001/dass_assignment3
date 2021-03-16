from component import Component
import config
import time
import glob

type_repr_map = ['-', ['E'], ['S'], ['B'], ['F'], ['T'], ['G']]


class PowerUp(Component):
    """
    self._type is one of the six power-up types
    The map is as follows:
    1: expand paddle
    2: shrink paddle
    3: ball multiplier
    4: fast ball
    5: thru-ball
    6: paddle grab


    _status determines current status of the powerup
    -1: missed
    0: spawned
    1: active
    2: disabled
    """

    def __init__(self, x, y, representation, p_type, deactivation_time=10):
        super().__init__(x, y, representation)
        self._type = p_type
        self._speed = 0.6
        self._status = 0
        self._deactivation_time = deactivation_time
        self._activation_time = time.time()
        self._xvel = xvel
        self._yvel = yvel

    def get_activation_time(self):
        return self._activation_time

    def set_activation_time(self):
        self._activation_time = time.time()

    def get_deactivation_time(self):
        return self._deactivation_time

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def get_type(self):
        return self._type

    def get_speed(self):
        return self._speed

    def is_caught_by_paddle(self, paddle):
        """
        Return true if caught by paddle and false otherwise
        :param paddle: The paddle instance
        :return: Boolean, true if caught and false otherwise
        """
        if paddle.get_x() <= self._x <= paddle.get_x() + paddle.get_width() and \
                self._y == paddle.get_y() - 1:
            return True
        return False

    def go_down(self, board):
        """
        Continue motion of powerup
        Returns true if powerup is lost
        :param board: matrix storing the board
        """
        self.clear(board)

        new_pos_y = self._y + 1
        if new_pos_y >= 0 and new_pos_y + self._height <= config.board_height:
            self.set_y(new_pos_y)

        if self._y >= config.paddle_row_restriction:
            return True
        return False

    def activate(self):
        pass

    def deactivate(self):
        pass


class ExpandPaddle(PowerUp):  # 1
    def __init__(self, x, y):
        super().__init__(x, y, ['E'], 1)

    def activate(self):
        glob.paddle.set_width(glob.paddle.get_width() + 2)
        return True

    def deactivate(self):
        glob.paddle.clear(glob.board.matrix)
        glob.paddle.set_width(glob.paddle.get_width() - 2)


class ShrinkPaddle(PowerUp):  # 2
    def __init__(self, x, y):
        super().__init__(x, y, ['S'], 2)

    def activate(self):
        glob.paddle.clear(glob.board.matrix)
        glob.paddle.set_width(glob.paddle.get_width() - 2)
        return True

    def deactivate(self):
        glob.paddle.set_width(glob.paddle.get_width() + 2)


class BallMultiplier(PowerUp):  # 3
    def __init__(self, x, y):
        super().__init__(x, y, ['B'], 3)

    def activate(self):
        to_append = False
        if glob.balls.get_number_balls() < 4:
            to_append = True
            for ball in list(glob.balls.get_balls()):
                if ball == glob.paddle.get_ball():
                    glob.balls.add_ball(ball.get_x(), ball.get_y(),
                                        -ball.get_xvel(), -1,
                                        free=True, speed=ball.get_speed())
                else:
                    glob.balls.add_ball(ball.get_x(), ball.get_y(),
                                        -ball.get_xvel(), -ball.get_yvel(),
                                        free=True, speed=ball.get_speed())
        return to_append

    def deactivate(self):
        glob.balls.clear_all(glob.board.matrix)
        glob.balls.remove_half()


class FastBall(PowerUp):  # 4
    def __init__(self, x, y):
        super().__init__(x, y, ['F'], 4)

    def activate(self):
        to_append = False
        for ball in glob.balls.get_balls():
            if 0.1 < ball.get_speed() <= 0.3:
                to_append = True
                ball.set_speed(ball.get_speed() - config.ball_speed_interval)
        return to_append

    def deactivate(self):
        for ball in glob.balls.get_balls():
            ball.set_speed(ball.get_speed() + config.ball_speed_interval)


class ThruBall(PowerUp):  # 5
    def __init__(self, x, y):
        super().__init__(x, y, ['T'], 5)

    def activate(self):
        return True


class PaddleGrab(PowerUp):  # 6
    def __init__(self, x, y):
        super().__init__(x, y, ['G'], 6)

    def activate(self):
        glob.paddle.set_grab(True)
        return True

    def deactivate(self):
        glob.paddle.set_grab(False)
