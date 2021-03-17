from component import Component
import config


class Paddle(Component):
    def __init__(self, x=config.board_width // 2, width=config.paddle_init_width, ball=None):
        representation = ['▄' * width]
        super().__init__(x, config.paddle_row_restriction, representation)
        self._ball = ball
        self._grab = False
        self._is_shooting = False

    def set_shooting(self, val):
        self._is_shooting = val
        if val:
            self._representation = ['^' + '▄'*(self._width-2) + '^']
        else:
            self._representation = ['▄' * self._width]

    def get_shooting(self):
        return self._is_shooting

    def set_grab(self, value):
        self._grab = value

    def get_grab(self):
        return self._grab

    def get_center_x_coordinate(self):
        return self._x + self._width // 2

    def hold_ball(self, ball):
        if self._ball:
            #  Handle if paddle already holds a ball
            self._ball.set_is_free(True)
        ball.set_is_free(False)
        self._ball = ball

    def get_ball(self):
        return self._ball

    def get_ball_rel_distance_from_p_center(self):
        """
        Returns the relative distance of the ball from the center
        :return: Integer value that signifies relative x-position from center
        """
        if not self._ball:
            return None

        return self._ball.get_x() - self.get_center_x_coordinate()

    def release_ball(self):
        """
        Release ball held by paddle
        :return:
        """
        if self._ball:
            if self._grab:
                self._grab = False
            else:
                self._ball.set_relative_velocity(x_vel_diff=self.get_ball_rel_distance_from_p_center())
                self._ball.set_yvel(-1)
            self._ball.set_is_free(True)
            self._ball = None

    def set_width(self, width=3):
        """
        Sets width of paddle
        :param width: width of paddle
        """
        width = max(3, min(7, width))
        representation = ['▄' * width]
        if self._is_shooting:
            representation = ['^' + '▄'*(width-2) + '^']
        self.set_representation(representation)

    def move_relative(self, board, x_diff=0):
        """
        Sets new position relative to current position of paddle
        :param board: matrix storing the board
        :param x_diff: delta by which the position of paddle changes in the x-axis
        """
        self.clear(board)
        new_pos = self._x + x_diff
        if new_pos >= 0 and new_pos + self._width < config.board_width:
            self.set_x(new_pos)
            if self._ball:
                self._ball.move_relative(board, x_diff)

